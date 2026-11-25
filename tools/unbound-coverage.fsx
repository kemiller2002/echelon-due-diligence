// Keyword coverage of the Unbound requirements baseline by due diligence category.
// Usage: dotnet fsi tools/unbound-coverage.fsx <path-to-unbound-clone>
// Output: gap-analysis/generated/unbound-baseline-coverage.csv
// This is a screening heuristic, not a determination of adequacy: a keyword hit means a
// requirement mentions the topic, not that it satisfies a customer's concern.
open System
open System.IO
open System.Text.Json
open System.Text.RegularExpressions

let unbound = fsi.CommandLineArgs |> Array.tryItem 1 |> Option.defaultValue "/home/user/unbound"
let root = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, ".."))

type Req = { Id: string; Text: string; Status: string }

let reqs =
    File.ReadLines(Path.Combine(unbound, "requirements", "baseline", "baseline.jsonl"))
    |> Seq.map (fun l ->
        let d = JsonDocument.Parse(l).RootElement
        let s (k: string) =
            match d.TryGetProperty k with
            | true, v when v.ValueKind = JsonValueKind.String -> v.GetString()
            | _ -> ""
        { Id = s "id"; Text = (s "text").ToLowerInvariant(); Status = s "status" })
    |> List.ofSeq

// Category -> keyword regexes (word-boundary, lowercase).
let topics: (string * string list) list =
    [ "GOV", [ "board"; "governance"; "conflict of interest"; "ownership" ]
      "FST", [ "financial statement"; "going concern"; "runway"; "solvency" ]
      "AUD", [ "soc 2"; "soc 1"; "auditor"; "attestation"; "right to audit"; "iso 27001" ]
      "LEG", [ "contract"; "liabilit"; "indemn"; "addend"; "msa" ]
      "INS", [ "insurance"; "insurer"; "e&o"; "cyber liability" ]
      "HR", [ "background check"; "training"; "onboarding"; "offboarding"; "personnel" ]
      "IAM", [ "provision"; "access review"; "privileged"; "least privilege"; "break-glass"; "service identit" ]
      "AUN", [ "mfa"; "multi-factor"; "authenticat"; "sso"; "saml"; "oidc"; "passkey"; "session" ]
      "AUZ", [ "authoriz"; "permission"; "role"; "entitlement"; "separation of duties"; "segregation of duties" ]
      "TEN", [ "tenant"; "partner segregation"; "isolation"; "sponsor scope" ]
      "APP", [ "xss"; "injection"; "csrf"; "input validation"; "output encoding"; "owasp" ]
      "API", [ "api"; "rate limit"; "idempotency key"; "webhook" ]
      "SDL", [ "code review"; "secure development"; "sdlc"; "threat model" ]
      "CHG", [ "change management"; "deployment"; "rollback"; "emergency change"; "release" ]
      "SCS", [ "dependenc"; "sbom"; "supply chain"; "provenance"; "signing" ]
      "VUL", [ "vulnerabilit"; "patch"; "cve"; "remediation sla" ]
      "PEN", [ "penetration"; "pen test"; "red team" ]
      "SCN", [ "scan"; "sast"; "dast"; "secret scanning" ]
      "MON", [ "logging"; "log "; "monitor"; "siem"; "alert"; "heartbeat" ]
      "IR", [ "incident"; "breach"; "notification"; "forensic" ]
      "NET", [ "network"; "firewall"; "segmentation"; "ddos"; "waf" ]
      "INF", [ "infrastructure"; "hosting"; "container"; "hardening" ]
      "CLD", [ "cloud"; "region"; "residency"; "aws"; "azure"; "gcp" ]
      "ENC", [ "encrypt"; "key management"; "kms"; "hsm"; "tls"; "cryptograph" ]
      "PRV", [ "privacy"; "personal data"; "gdpr"; "ccpa"; "glba"; "data subject"; "consent" ]
      "DCL", [ "classification"; "sensitive data"; "pii"; "restricted data" ]
      "RET", [ "retention"; "deletion"; "legal hold"; "purge"; "sanitiz" ]
      "BCP", [ "continuity"; "business impact"; "key person" ]
      "DR", [ "disaster"; "rto"; "rpo"; "failover" ]
      "BKP", [ "backup"; "restore" ]
      "AVL", [ "availability"; "uptime"; "sla"; "status page"; "degraded" ]
      "PRF", [ "performance"; "latency"; "load test"; "capacity" ]
      "SUP", [ "support"; "help desk"; "escalation" ]
      "PRT", [ "export"; "portab"; "migration" ]
      "TRM", [ "termination"; "offboard"; "exit"; "transition assistance"; "wind-down" ]
      "ESC", [ "escrow" ]
      "A11Y", [ "wcag"; "accessib"; "screen reader"; "vpat" ]
      "AIG", [ "ai "; "model"; "llm"; "agent" ]
      "AIS", [ "prompt injection"; "jailbreak"; "model output" ]
      "AIA", [ "agent"; "human approval"; "interrupt"; "autonom" ]
      "TPR", [ "vendor"; "third party"; "third-party"; "due diligence" ]
      "SUB", [ "subprocessor"; "subservice"; "sub-processor" ]
      "REG", [ "regulator"; "examination"; "compliance program"; "regulatory change" ]
      "AML", [ "ofac"; "sanction"; "aml"; "bsa"; "kyc"; "sdn" ]
      "FCT", [ "maker-checker"; "dual control"; "approval limit"; "segregation" ]
      "ACT", [ "journal"; "ledger"; "posting"; "period close"; "asc 958" ]
      "TXI", [ "idempoten"; "exactly once"; "atomic"; "replay"; "concurren" ]
      "FRD", [ "fraud"; "account takeover"; "anomal" ]
      "PAY", [ "ach"; "nacha"; "wire"; "check"; "positive pay"; "disburse" ]
      "RCN", [ "reconcil" ]
      "CUS", [ "custod" ]
      "INV", [ "investment"; "nav"; "rebalanc"; "allocation" ]
      "FEE", [ "fee" ]
      "RRP", [ "990"; "acknowledg"; "1099"; "schedule d"; "unclaimed property" ]
      "DAF", [ "advisor"; "successor"; "donor-advised"; "daf" ]
      "GRT", [ "grant" ]
      "CHV", [ "charity"; "eligib"; "pub 78"; "bmf"; "equivalency" ]
      "CON", [ "contribution" ]
      "DON", [ "donor" ]
      "WLB", [ "white-label"; "white label"; "embedded"; "co-brand"; "partner brand" ] ]

let matches (kw: string) (text: string) =
    Regex.IsMatch(text, @"(^|[^a-z])" + Regex.Escape kw)

let coverage =
    topics
    |> List.map (fun (cat, kws) ->
        let hits = reqs |> List.filter (fun r -> kws |> List.exists (fun k -> matches k r.Text))
        let adopted = hits |> List.filter (fun r -> r.Status <> "original" && r.Status <> "proposed" && r.Status <> "unvalidated")
        cat, hits.Length, adopted.Length, hits |> List.truncate 12 |> List.map (fun r -> r.Id))

let band n =
    if n = 0 then "none"
    elif n < 5 then "thin"
    elif n < 20 then "moderate"
    else "extensive"

let csvLines =
    "category,baseline_hits,refined_or_adopted_hits,screening_band,sample_ids"
    :: (coverage
        |> List.map (fun (c, n, a, ids) -> sprintf "%s,%d,%d,%s,\"%s\"" c n a (band n) (String.concat "; " ids)))

let outDir = Path.Combine(root, "gap-analysis", "generated")
Directory.CreateDirectory outDir |> ignore
File.WriteAllLines(Path.Combine(outDir, "unbound-baseline-coverage.csv"), csvLines)
printfn "requirements=%d categories=%d" reqs.Length coverage.Length
coverage |> List.filter (fun (_, n, _, _) -> n < 5) |> List.iter (fun (c, n, _, _) -> printfn "thin-or-none %s %d" c n)
