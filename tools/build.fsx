// Echelon due diligence knowledge base: validate canonical records and generate registers.
// Usage: dotnet fsi tools/build.fsx [--check]
//   --check  validate only; do not write generated registers.
// Exit code 0 when no errors; 1 when any error is found. Warnings never fail the build.
#r "nuget: JsonSchema.Net, 7.3.4"

open System
open System.IO
open System.Text.Json
open System.Text.Json.Nodes
open System.Text.RegularExpressions
open Json.Schema

// ---------- Domain ----------

type Severity =
    | Error
    | Warning

type Finding =
    { Severity: Severity
      Code: string
      Location: string
      Message: string }

type Record =
    { Kind: string
      File: string
      Line: int
      Node: JsonObject }

let root =
    Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, ".."))

let rel (p: string) = Path.GetRelativePath(root, p)

let finding sev code loc msg =
    { Severity = sev
      Code = code
      Location = loc
      Message = msg }

let locOf (r: Record) = sprintf "%s:%d" (rel r.File) r.Line

// ---------- JSON helpers (pure) ----------

let tryProp (key: string) (o: JsonObject) : JsonNode =
    let mutable n: JsonNode = null
    if o.TryGetPropertyValue(key, &n) then n else null

let str (key: string) (o: JsonObject) =
    match tryProp key o with
    | v when not (isNull v) && v.GetValueKind() = JsonValueKind.String -> Some(v.GetValue<string>())
    | _ -> None

let strOr key d o = str key o |> Option.defaultValue d

let strList (key: string) (o: JsonObject) =
    match tryProp key o with
    | :? JsonArray as a ->
        a
        |> Seq.choose (fun n ->
            if not (isNull n) && n.GetValueKind() = JsonValueKind.String then
                Some(n.GetValue<string>())
            else
                None)
        |> List.ofSeq
    | _ -> []

let objList (key: string) (o: JsonObject) =
    match tryProp key o with
    | :? JsonArray as a -> a |> Seq.choose (fun n -> match n with :? JsonObject as x -> Some x | _ -> None) |> List.ofSeq
    | _ -> []

let rec allStrings (n: JsonNode) : string seq =
    match n with
    | null -> Seq.empty
    | :? JsonObject as o -> o |> Seq.collect (fun kv -> allStrings kv.Value)
    | :? JsonArray as a -> a |> Seq.collect allStrings
    | v when v.GetValueKind() = JsonValueKind.String -> Seq.singleton (v.GetValue<string>())
    | _ -> Seq.empty

// ---------- Loading ----------

let kindFiles: (string * string list) list =
    [ "source", [ "sources" ]
      "question", [ "questions" ]
      "answer-unit", [ "answers" ]
      "control", [ "controls" ]
      "evidence-requirement", [ "evidence-requirements" ]
      "proposed-requirement", [ "product-profiles" ]
      "objection", [ "validation" ]
      "recommendation", [ "recommendations" ] ]

let jsonlFiles dir =
    let d = Path.Combine(root, dir)
    if Directory.Exists d then
        Directory.GetFiles(d, "*.jsonl", SearchOption.AllDirectories) |> Array.sort |> List.ofArray
    else
        []

let kindForFile kind (file: string) =
    match kind with
    | "proposed-requirement" -> Path.GetFileName(file).StartsWith "proposed-requirements"
    | "objection" -> Path.GetFileName(file).StartsWith "objections"
    | _ -> true

let parseFile kind file : Result<Record, Finding> list =
    File.ReadAllLines file
    |> Array.mapi (fun i line -> i + 1, line)
    |> Array.filter (fun (_, l) -> not (String.IsNullOrWhiteSpace l))
    |> Array.map (fun (n, line) ->
        try
            match JsonNode.Parse line with
            | :? JsonObject as o -> Ok { Kind = kind; File = file; Line = n; Node = o }
            | _ -> Result.Error(finding Error "PARSE" (sprintf "%s:%d" (rel file) n) "line is not a JSON object")
        with ex ->
            Result.Error(finding Error "PARSE" (sprintf "%s:%d" (rel file) n) ex.Message))
    |> List.ofArray

let loaded =
    kindFiles
    |> List.collect (fun (kind, dirs) ->
        dirs
        |> List.collect jsonlFiles
        |> List.filter (kindForFile kind)
        |> List.collect (parseFile kind))

let records =
    loaded |> List.choose (function Ok r -> Some r | _ -> None)

let parseFindings =
    loaded |> List.choose (function Result.Error f -> Some f | _ -> None)

let byKind k = records |> List.filter (fun r -> r.Kind = k)

// ---------- Schema validation ----------

let schemaFor =
    let cache =
        kindFiles
        |> List.map fst
        |> List.choose (fun k ->
            let p = Path.Combine(root, "schemas", "dd", k + ".schema.json")
            if File.Exists p then Some(k, JsonSchema.FromFile p) else None)
        |> Map.ofList
    fun k -> Map.tryFind k cache

let schemaFindings =
    let opts = EvaluationOptions(OutputFormat = OutputFormat.List)
    records
    |> List.collect (fun r ->
        match schemaFor r.Kind with
        | None -> [ finding Warning "NO-SCHEMA" (locOf r) (sprintf "no schema for kind %s" r.Kind) ]
        | Some s ->
            let res = s.Evaluate(JsonDocument.Parse(r.Node.ToJsonString()).RootElement, opts)
            if res.IsValid then
                []
            else
                let details =
                    res.Details
                    |> Seq.filter (fun d -> not (isNull d.Errors) && d.Errors.Count > 0)
                    |> Seq.collect (fun d -> d.Errors |> Seq.map (fun e -> sprintf "%s %s" (string d.InstanceLocation) e.Value))
                    |> Seq.truncate 3
                    |> String.concat "; "
                [ finding Error "SCHEMA" (locOf r) (sprintf "%s: %s" (strOr "id" "?" r.Node) details) ])

// ---------- Identity and referential integrity ----------

let idsOf k =
    byKind k |> List.choose (fun r -> str "id" r.Node) |> Set.ofList

let duplicateIdFindings =
    records
    |> List.choose (fun r -> str "id" r.Node |> Option.map (fun id -> id, r))
    |> List.groupBy fst
    |> List.filter (fun (_, rs) -> List.length rs > 1)
    |> List.map (fun (id, rs) ->
        finding Error "DUP-ID" (rs |> List.map (snd >> locOf) |> String.concat ", ") (sprintf "duplicate id %s" id))

let sourceIds = idsOf "source"
let answerIds = idsOf "answer-unit"
let controlIds = idsOf "control"
let evidenceIds = idsOf "evidence-requirement"
let questionIds = idsOf "question"

let refCheck (r: Record) (field: string) (prefix: string) (known: Set<string>) (ids: string list) =
    ids
    |> List.filter (fun i -> i.StartsWith prefix && not (Set.contains i known))
    |> List.map (fun i -> finding Error "DANGLING" (locOf r) (sprintf "%s %s references unknown %s" (strOr "id" "?" r.Node) field i))

let sourceRefIds (o: JsonObject) =
    [ "source_refs"; "framework_refs" ] |> List.collect (fun k -> objList k o |> List.choose (str "source_id"))

let referenceFindings =
    records
    |> List.collect (fun r ->
        let o = r.Node
        let srcs = refCheck r "source_ref" "SRC-" sourceIds (sourceRefIds o)
        let ctl = refCheck r "controls" "ECTL-" controlIds (strList "controls" o)
        let evr = refCheck r "evidence_requirements" "EVR-" evidenceIds (strList "evidence_requirements" o)
        let ans =
            match r.Kind, str "answer_unit" o with
            | "question", Some a when not (Set.contains a answerIds) ->
                [ finding Error "DANGLING" (locOf r) (sprintf "%s answer_unit %s not found" (strOr "id" "?" o) a) ]
            | _ -> []
        let origin =
            refCheck r "originating_questions" "DDQ-" questionIds (strList "originating_questions" o)
        srcs @ ctl @ evr @ ans @ origin)

// ---------- Honesty rules ----------

let currentStatuses =
    set [ "verified-operational"; "implemented-not-independently-verified" ]

let honestyFindings =
    byKind "answer-unit"
    |> List.collect (fun r ->
        let status = strOr "status" "" r.Node
        let kind = strOr "customer_statement_kind" "" r.Node
        let indep = strOr "assurance_independence" "" r.Node
        [ if kind = "current-fact" && not (Set.contains status currentStatuses) then
              finding Error "ASPIRATIONAL-AS-CURRENT" (locOf r)
                  (sprintf "%s states a current fact but status is %s" (strOr "id" "?" r.Node) status)
          if kind = "qualified-current-fact" && not (Set.contains status (Set.add "partially-implemented" currentStatuses)) then
              finding Error "ASPIRATIONAL-AS-CURRENT" (locOf r)
                  (sprintf "%s states a qualified current fact but status is %s" (strOr "id" "?" r.Node) status)
          if indep = "independent-third-party" && status <> "verified-operational" then
              finding Warning "INDEPENDENCE" (locOf r)
                  (sprintf "%s claims independent assurance with status %s" (strOr "id" "?" r.Node) status) ])

// Text-level lint: a planned or not-available statement must read as such. This is a
// heuristic, not proof; it catches statements whose wording asserts a present capability
// while the structured fields say it does not exist.
let futureOrNegativeMarkers =
    [ "plan"; "will "; "intend"; "target"; "not "; "no "; "does not"; "do not"; "has not"; "have not"
      "future"; "roadmap"; "yet"; "proposed"; "designed to"; "under development"; "unavailable"
      "cannot"; "unknown"; "not available"; "upon request" ]

let statementTextFindings =
    byKind "answer-unit"
    |> List.choose (fun r ->
        let kind = strOr "customer_statement_kind" "" r.Node
        let text = (strOr "customer_statement" "" r.Node).ToLowerInvariant()
        let hedged = futureOrNegativeMarkers |> List.exists (fun m -> text.Contains m)
        if (kind = "planned" || kind = "not-available") && not hedged && text <> "" then
            Some(finding Warning "STATEMENT-TEXT" (locOf r)
                     (sprintf "%s is %s but its statement text does not read as planned or unavailable" (strOr "id" "?" r.Node) kind))
        else
            None)

// Review gate: agents may draft, only named humans approve. Unreviewed answer units are
// research records, not customer-releasable statements.
let reviewFindings =
    let units = byKind "answer-unit"
    let state (r: Record) =
        match tryProp "review" r.Node with
        | :? JsonObject as v -> strOr "state" "unreviewed" v
        | _ -> "unreviewed"
    let approvedWithoutHuman =
        units
        |> List.filter (fun r ->
            match tryProp "review" r.Node with
            | :? JsonObject as v -> strOr "state" "" v = "approved" && (strOr "reviewer_kind" "" v <> "human" || strOr "reviewer" "" v = "")
            | _ -> false)
        |> List.map (fun r -> finding Error "REVIEW-NO-HUMAN" (locOf r) (sprintf "%s approved without a named human reviewer" (strOr "id" "?" r.Node)))
    let currentFactUnapproved =
        units
        |> List.filter (fun r ->
            let k = strOr "customer_statement_kind" "" r.Node
            (k = "current-fact" || k = "qualified-current-fact") && state r <> "approved")
        |> List.map (fun r -> finding Warning "CURRENT-FACT-UNAPPROVED" (locOf r) (strOr "id" "?" r.Node))
    let unreviewed = units |> List.filter (fun r -> state r <> "approved") |> List.length
    approvedWithoutHuman
    @ currentFactUnapproved
    @ (if unreviewed > 0 then
           [ finding Warning "UNREVIEWED" "answers/" (sprintf "%d of %d answer units lack human approval; none may be released to customers" unreviewed units.Length) ]
       else
           [])

let emDash = '—'

let emDashFindings =
    let inRecords =
        records
        |> List.filter (fun r -> allStrings r.Node |> Seq.exists (fun s -> s.Contains emDash))
        |> List.map (fun r -> finding Error "EM-DASH" (locOf r) (strOr "id" "?" r.Node))
    let ownedDirs =
        [ "sources"; "questions"; "answers"; "controls"; "evidence-requirements"; "framework-mappings"
          "security-by-construction"; "scanner-validation"; "external-assurance"; "cost-avoidance"
          "industry-profiles"; "product-profiles"; "gap-analysis"; "questionnaires"; "trust-center"
          "architecture"; "recommendations"; "decisions"; "reports"; "validation"; "research/sources" ]
    let inDocs =
        ownedDirs
        |> List.map (fun d -> Path.Combine(root, d))
        |> List.filter Directory.Exists
        |> List.collect (fun d -> Directory.GetFiles(d, "*.md", SearchOption.AllDirectories) |> List.ofArray)
        |> List.filter (fun f -> File.ReadAllText(f).Contains emDash)
        |> List.map (fun f -> finding Error "EM-DASH" (rel f) "document contains an em dash")
    inRecords @ inDocs

// ---------- Near-duplicate questions ----------

let stop =
    set [ "the"; "a"; "an"; "of"; "to"; "and"; "or"; "for"; "in"; "on"; "is"; "are"; "do"; "does"; "you"; "your"
          "with"; "how"; "what"; "which"; "by"; "be"; "that"; "this"; "any"; "all"; "it"; "its"; "as"; "at"; "from" ]

let tokens (s: string) =
    Regex.Matches(s.ToLowerInvariant(), "[a-z0-9]+")
    |> Seq.map (fun m -> m.Value)
    |> Seq.filter (fun t -> not (Set.contains t stop))
    |> Set.ofSeq

let jaccard (a: Set<string>) (b: Set<string>) =
    let u = Set.union a b |> Set.count
    if u = 0 then 0.0 else float (Set.intersect a b |> Set.count) / float u

let duplicateQuestionFindings =
    let qs =
        byKind "question"
        |> List.map (fun r -> strOr "id" "?" r.Node, tokens (strOr "question" "" r.Node), r)
        |> Array.ofList
    [ for i in 0 .. qs.Length - 1 do
          for j in i + 1 .. qs.Length - 1 do
              let (ia, ta, _) = qs.[i]
              let (ib, tb, rb) = qs.[j]
              let sim = jaccard ta tb
              if sim >= 0.8 then
                  yield finding Warning "NEAR-DUP" (locOf rb) (sprintf "%s ~ %s (jaccard %.2f)" ib ia sim) ]

// ---------- Coverage warnings ----------

let orphanFindings =
    let usedAnswers = byKind "question" |> List.choose (fun r -> str "answer_unit" r.Node) |> Set.ofList
    let usedControls =
        records |> List.collect (fun r -> if r.Kind = "control" then [] else strList "controls" r.Node) |> Set.ofList
    let ctlNoEvidence =
        byKind "control"
        |> List.filter (fun r -> strList "evidence_requirements" r.Node |> List.isEmpty)
        |> List.map (fun r -> finding Warning "CONTROL-NO-EVIDENCE" (locOf r) (strOr "id" "?" r.Node))
    let unusedAnswers =
        byKind "answer-unit"
        |> List.filter (fun r -> not (Set.contains (strOr "id" "" r.Node) usedAnswers))
        |> List.map (fun r -> finding Warning "ORPHAN-ANSWER" (locOf r) (strOr "id" "?" r.Node))
    let unusedControls =
        byKind "control"
        |> List.filter (fun r -> not (Set.contains (strOr "id" "" r.Node) usedControls))
        |> List.map (fun r -> finding Warning "ORPHAN-CONTROL" (locOf r) (strOr "id" "?" r.Node))
    ctlNoEvidence @ unusedAnswers @ unusedControls

// ---------- Generated registers ----------

let csvCell (s: string) =
    let t = s.Replace("\r", " ").Replace("\n", " ")
    if t.IndexOfAny([| ','; '"' |]) >= 0 then "\"" + t.Replace("\"", "\"\"") + "\"" else t

let csv (header: string list) (rows: string list list) =
    (header :: rows) |> List.map (List.map csvCell >> String.concat ",") |> String.concat "\n"

let joined key o = strList key o |> String.concat "; "

let answerById =
    byKind "answer-unit" |> List.map (fun r -> strOr "id" "" r.Node, r.Node) |> Map.ofList

let registers =
    let q = byKind "question" |> List.map (fun r -> r.Node)
    let a = byKind "answer-unit" |> List.map (fun r -> r.Node)
    let c = byKind "control" |> List.map (fun r -> r.Node)
    let e = byKind "evidence-requirement" |> List.map (fun r -> r.Node)
    let s = byKind "source" |> List.map (fun r -> r.Node)
    let ansField f o =
        str "answer_unit" o |> Option.bind (fun id -> Map.tryFind id answerById) |> Option.bind (str f) |> Option.defaultValue ""
    [ "canonical-question-register.csv",
      csv [ "id"; "category"; "subcategory"; "question"; "requirement_classification"; "customer_importance"; "answer_unit"; "answer_status"; "industries"; "jurisdictions"; "products"; "sources" ]
          (q |> List.map (fun o ->
              [ strOr "id" "" o; strOr "category" "" o; strOr "subcategory" "" o; strOr "question" "" o
                strOr "requirement_classification" "" o; strOr "customer_importance" "" o; strOr "answer_unit" "" o
                ansField "status" o; joined "industries" o; joined "jurisdictions" o; joined "products" o
                sourceRefIds o |> List.distinct |> String.concat "; " ]))
      "target-answer-register.csv",
      csv [ "id"; "title"; "status"; "target_answer"; "intended_practice"; "owner"; "implementation_cost"; "recurring_cost" ]
          (a |> List.map (fun o ->
              [ strOr "id" "" o; strOr "title" "" o; strOr "status" "" o; strOr "target_answer" "" o
                strOr "intended_practice" "" o; strOr "owner" "" o; strOr "implementation_cost" "" o; strOr "recurring_cost" "" o ]))
      "verified-current-answer-register.csv",
      csv [ "id"; "title"; "status"; "status_rationale"; "current_practice"; "provable"; "customer_statement"; "customer_statement_kind"; "assurance_independence"; "disclosure_classification" ]
          (a |> List.map (fun o ->
              [ strOr "id" "" o; strOr "title" "" o; strOr "status" "" o; strOr "status_rationale" "" o
                strOr "current_practice" "" o; strOr "provable" "" o; strOr "customer_statement" "" o
                strOr "customer_statement_kind" "" o; strOr "assurance_independence" "" o; strOr "disclosure_classification" "" o ]))
      "control-register.csv",
      csv [ "id"; "title"; "control_type"; "assurance_level"; "status"; "implementing_systems"; "policies"; "related_external_controls"; "cwe"; "evidence_requirements"; "owner" ]
          (c |> List.map (fun o ->
              [ strOr "id" "" o; strOr "title" "" o; strOr "control_type" "" o; strOr "assurance_level" "" o; strOr "status" "" o
                joined "implementing_systems" o; joined "policies" o; joined "related_external_controls" o; joined "cwe" o
                joined "evidence_requirements" o; strOr "owner" "" o ]))
      "evidence-requirements-register.csv",
      csv [ "id"; "title"; "producer"; "mechanism"; "freshness"; "independence"; "disclosure_classification"; "status" ]
          (e |> List.map (fun o ->
              [ strOr "id" "" o; strOr "title" "" o; strOr "producer" "" o; strOr "mechanism" "" o; strOr "freshness" "" o
                strOr "independence" "" o; strOr "disclosure_classification" "" o; strOr "status" "" o ]))
      "master-source-register.csv",
      csv [ "id"; "title"; "issuer"; "type"; "authority"; "version"; "publication_date"; "status"; "url"; "license"; "verified"; "applicability" ]
          (s |> List.map (fun o ->
              let verified =
                  match tryProp "verification" o with
                  | :? JsonObject as v ->
                      (match tryProp "verified" v with
                       | b when not (isNull b) && (b.GetValueKind() = JsonValueKind.True || b.GetValueKind() = JsonValueKind.False) -> string (b.GetValue<bool>())
                       | _ -> "")
                  | _ -> ""
              [ strOr "id" "" o; strOr "title" "" o; strOr "issuer" "" o; strOr "type" "" o; strOr "authority" "" o
                strOr "version" "" o; strOr "publication_date" "" o; strOr "status" "" o; strOr "url" "" o
                strOr "license" "" o; verified; strOr "applicability" "" o ]))
      "regulatory-applicability-matrix.csv",
      csv [ "id"; "title"; "issuer"; "authority"; "status"; "jurisdictions"; "applicability" ]
          (s
           |> List.filter (fun o ->
               [ "binding-law"; "binding-regulation"; "supervisory-expectation" ]
               |> List.contains (strOr "authority" "" o))
           |> List.map (fun o ->
               [ strOr "id" "" o; strOr "title" "" o; strOr "issuer" "" o; strOr "authority" "" o
                 strOr "status" "" o; joined "jurisdictions" o; strOr "applicability" "" o ]))
      "open-questions-register.csv",
      csv [ "record_id"; "kind"; "category_or_title"; "open_question" ]
          ((byKind "question" @ byKind "answer-unit")
           |> List.collect (fun r ->
               strList "open_questions" r.Node
               |> List.map (fun oq ->
                   [ strOr "id" "" r.Node; r.Kind; strOr "category" (strOr "title" "" r.Node) r.Node; oq ])))
      "framework-crosswalk.csv",
      csv [ "question_id"; "category"; "source_id"; "locator"; "relation"; "basis" ]
          ((q @ c)
           |> List.collect (fun o ->
               [ "source_refs"; "framework_refs" ]
               |> List.collect (fun k -> objList k o)
               |> List.map (fun sr ->
                   [ strOr "id" "" o; strOr "category" "control" o; strOr "source_id" "" sr; strOr "locator" "" sr
                     strOr "relation" "" sr; strOr "basis" "" sr ]))) ]

let countBy (f: JsonObject -> string) (xs: JsonObject list) =
    xs |> List.countBy f |> List.sortBy fst

let summaryMarkdown (findings: Finding list) =
    let q = byKind "question" |> List.map (fun r -> r.Node)
    let a = byKind "answer-unit" |> List.map (fun r -> r.Node)
    let table title (rows: (string * int) list) =
        [ sprintf "### %s" title; ""; "| Value | Count |"; "|---|---|" ]
        @ (rows |> List.map (fun (k, n) -> sprintf "| %s | %d |" (if k = "" then "(blank)" else k) n))
        @ [ "" ]
    let challenged = a |> List.filter (fun o -> o.ContainsKey "challenge") |> List.length
    [ "---"; "id: DD-RPT-REG-001"; "title: Generated register summary"; "status: generated"; "---"; ""
      "# Generated register summary"; ""
      "Generated by `tools/build.fsx`. Do not edit by hand."; ""
      "| Record | Count |"; "|---|---|"
      sprintf "| Canonical questions | %d |" q.Length
      sprintf "| Answer units | %d |" a.Length
      sprintf "| Answer units with challenge analysis | %d |" challenged
      sprintf "| Controls | %d |" (byKind "control").Length
      sprintf "| Evidence requirements | %d |" (byKind "evidence-requirement").Length
      sprintf "| Sources | %d |" (byKind "source").Length
      sprintf "| Proposed product requirements | %d |" (byKind "proposed-requirement").Length
      sprintf "| Objections | %d |" (byKind "objection").Length
      sprintf "| Recommendations | %d |" (byKind "recommendation").Length
      sprintf "| Errors | %d |" (findings |> List.filter (fun f -> f.Severity = Error) |> List.length)
      sprintf "| Warnings | %d |" (findings |> List.filter (fun f -> f.Severity = Warning) |> List.length)
      "" ]
    @ table "Questions by category" (countBy (strOr "category" "") q)
    @ table "Questions by requirement classification" (countBy (strOr "requirement_classification" "") q)
    @ table "Answer units by status" (countBy (strOr "status" "") a)
    @ table "Answer units by customer statement kind" (countBy (strOr "customer_statement_kind" "") a)
    @ table "Warnings by code" (findings |> List.filter (fun f -> f.Severity = Warning) |> List.countBy (fun f -> f.Code))
    |> String.concat "\n"

// ---------- Main ----------

let allFindings =
    parseFindings
    @ schemaFindings
    @ duplicateIdFindings
    @ referenceFindings
    @ honestyFindings
    @ statementTextFindings
    @ reviewFindings
    @ emDashFindings
    @ duplicateQuestionFindings
    @ orphanFindings

let checkOnly = fsi.CommandLineArgs |> Array.contains "--check"

let errors = allFindings |> List.filter (fun f -> f.Severity = Error)
let warnings = allFindings |> List.filter (fun f -> f.Severity = Warning)

errors |> List.truncate 200 |> List.iter (fun f -> eprintfn "ERROR %s %s %s" f.Code f.Location f.Message)

warnings
|> List.countBy (fun f -> f.Code)
|> List.iter (fun (c, n) -> printfn "warning %s: %d" c n)

if not checkOnly then
    let outDir = Path.Combine(root, "reports", "generated")
    Directory.CreateDirectory outDir |> ignore
    registers |> List.iter (fun (name, content) -> File.WriteAllText(Path.Combine(outDir, name), content + "\n"))
    File.WriteAllText(Path.Combine(outDir, "REGISTER-SUMMARY.md"), summaryMarkdown allFindings + "\n")
    File.WriteAllText(
        Path.Combine(outDir, "validation-findings.csv"),
        csv [ "severity"; "code"; "location"; "message" ]
            (allFindings |> List.map (fun f -> [ string f.Severity; f.Code; f.Location; f.Message ]))
        + "\n")

printfn "records=%d errors=%d warnings=%d" records.Length errors.Length warnings.Length
exit (if errors.IsEmpty then 0 else 1)
