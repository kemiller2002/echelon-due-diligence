"""BL-015 fix pass (2026-11-25, fix-pass-agent) on the canonical CWE matrix CSV.

Applies the corrections from adversarial review DD-VAL-ADV-002 (OBJ-SKEPTIC-003/004/005/008,
OBJ-PENTEST-003/006/007) and preserves every other field. Run once from the repository
root; it refuses to run twice (detects the added columns).
"""
import csv
import sys

PATH = "security-by-construction/cwe-architectural-prevention-matrix.csv"
TAG = "Fix pass 2026-11-25 (fix-pass-agent, BL-015): "

rows = list(csv.DictReader(open(PATH, encoding="utf-8")))
if "claim_scope" in rows[0]:
    sys.exit("already applied")

SERVER = ("server-side F# assemblies only; F# compiled to WebAssembly and run in the browser executes on an "
          "attacker-controlled machine and is out of scope for every by-construction claim")
BROWSER = ("server-side F# assemblies and server-set browser policy (CSP, Trusted Types, response headers) only; "
           "browser-resident code, including the Limen kernel and any F# compiled to WebAssembly, runs on an "
           "attacker-controlled machine and is defense in depth for honest clients, never a security boundary")
NA = ("not-applicable: the platform is absent from the product; this is a statement of absence that holds only "
      "while a language and framework inventory gate proves it, not an elimination claim")


def note(r, text):
    r["notes"] = (r["notes"].rstrip() + " " if r["notes"].strip() else "") + TAG + text


out = []
for r in rows:
    fam = r["control_family"]
    cid = r["cwe_id"]
    # Scope qualifier (OBJ-PENTEST-003)
    if fam == "NA":
        scope = NA
    elif fam in ("XSS", "BROWSER", "CSRF") or cid == "CWE-1321":
        scope = BROWSER
    else:
        scope = SERVER
    lvl = r["strongest_achievable_level"]
    if fam != "NA" and lvl in ("L1", "L2", "L3", "L4") and not r["assurance_scope"].startswith("Server-side"):
        r["assurance_scope"] = "Server-side assemblies only (not browser-resident WebAssembly). " + r["assurance_scope"]

    # Prerequisite components (OBJ-PENTEST-007, OBJ-SKEPTIC-008)
    if fam == "NA":
        prereq = "not-applicable"
    elif fam == "SQL":
        prereq = "no: the Strata runtime query interface that accepts only precompiled, named queries does not exist"
    elif fam == "TENANT":
        prereq = ("no: the tenant context type and tenant-scoped Strata data interfaces do not exist; Strata models RLS "
                  "policies for schema management only")
    elif fam == "AUTHZ":
        prereq = "no: the Authorized decision type, scope-carrying query interface and policy engine do not exist"
    elif r["component_evidence"].strip():
        prereq = ("partial: a component-level pattern exists in another Echelon repository (see component_evidence); "
                  "no Unbound implementation exists")
    else:
        prereq = "no: no implementing component located; no Unbound implementation exists"

    # Row-specific corrections
    if cid == "CWE-457":
        r["strongest_achievable_level"] = "L2"
        r["supporting_levels"] = "L4;L5;L6;L7"
        note(r, "Re-rated from L1 to L2. The row's own bypasses (Unchecked.defaultof, Array.zeroCreate, CLIMutable "
                "records, reflection-based deserializers, default struct values) are expressible inside the stated "
                "scope, so elimination cannot be claimed. Option types and validated domain types make uninitialized "
                "values hard to express (L2); a banned-API gate (L5) and decoder property tests (L7) are needed to keep "
                "the bypasses out.")
    if cid in ("CWE-396", "CWE-252"):
        r["strongest_achievable_level"] = "L5"
        r["supporting_levels"] = "L2;L6;L7;L8"
        prereq = ("no: the custom F# analyzer or IL gate that rejects catch-all handlers and discarded Result values "
                  "does not exist")
        if cid == "CWE-396":
            r["assurance_scope"] = ("Server-side assemblies only (not browser-resident WebAssembly). F# code where a build "
                                    "gate (custom analyzer or IL scan) rejects catch handlers for System.Exception or "
                                    "wildcard 'with _ ->' handlers outside an allowlisted top-level fail-closed handler.")
            note(r, "Re-rated from L4 to L5. FS0025 is the incomplete-pattern warning and does not reject generic catch "
                    "handlers; only a custom analyzer or IL gate (not yet built) can. Until it exists the level is not "
                    "achievable.")
        else:
            r["assurance_scope"] = ("Server-side assemblies only (not browser-resident WebAssembly). F# code compiled with "
                                    "FS0020 (implicit discard of a non-unit value) as an error, plus a build gate that "
                                    "rejects explicit 'ignore' of Result and Option values in security-relevant modules.")
            note(r, "Re-rated from L4 to L5. FS0025 does not apply to return values. FS0020 as an error catches implicit "
                    "discards only; explicit '|> ignore' compiles, so a custom gate (not yet built) is required.")
    if cid == "CWE-636":
        r["strongest_achievable_level"] = "L7"
        r["supporting_levels"] = "L2;L5;L6;L8"
        r["assurance_scope"] = ("Server-side assemblies only (not browser-resident WebAssembly). Authorization, payment and "
                                "workflow decisions modeled as unions whose failure cases deny, checked by fault-injection "
                                "and property-based tests that assert no state is committed and no access granted on "
                                "failure.")
        note(r, "Re-rated from L4 to L7. Failing securely is a semantic property; FS0025 only forces every union case to be "
                "handled, not that the handling is safe. Fault-injection and property tests are the strongest "
                "practical evidence.")
    if cid == "CWE-1321":
        r["echelon_controls"] = ("SEC-UI-002 (no application-authored JavaScript outside the Limen kernel); proposed Limen "
                                 "kernel rule: parse untrusted JSON into Map or Object.create(null) targets, reject "
                                 "__proto__, constructor and prototype keys, no generic deep-merge or path-set utilities, "
                                 "Object.freeze on shared prototypes; lint gate on the kernel bundle")
        r["strongest_achievable_level"] = "L3"
        r["supporting_levels"] = "L5;L6;L8"
        r["known_bypasses"] = ("__proto__ or constructor.prototype keys in parsed JSON merged into plain objects; "
                               "Object.assign, spread or recursive merge of untrusted objects; path-based setters "
                               "(lodash.set style) on untrusted paths; query-string parsers that build nested objects; "
                               "third-party JavaScript dependencies of the kernel with polluting merges; prototype "
                               "gadgets that read inherited properties (for example options objects without own-property "
                               "checks).")
        r["residual_risk"] = ("Client-side prototype pollution affects only the attacker's own or a victim's browser "
                              "session (DOM XSS gadgets); server-side F# is not affected. Kernel dependencies and future "
                              "JavaScript added outside the kernel.")
        r["evidence_required"] = ("Kernel bundle inventory showing no merge or path-set utilities; lint rule results; "
                                  "tests that send __proto__, constructor and prototype keys through every kernel JSON "
                                  "entry point and assert Object.prototype is unchanged; dependency list of the kernel.")
        r["conventional_scanning_detects"] = "partial"
        r["scanning_notes"] = ("JavaScript SAST and some SCA advisories flag known polluting merge utilities; dynamic "
                               "detection requires gadget-aware testing.")
        r["hyp"] = "complementary"
        note(r, "Bypasses, controls, evidence and scanning fields replaced: the prior text was copied from the .NET "
                "deserialization row and did not apply to JavaScript (OBJ-SKEPTIC-005). Scanning comparison changed "
                "from beyond to complementary.")
    if cid == "CWE-639":
        r["control_family"] = "AUTHZ"
        r["strongest_achievable_level"] = "L7"
        r["supporting_levels"] = "L2;L3;L8;L9;L10"
        r["assurance_scope"] = ("Server-side assemblies only (not browser-resident WebAssembly). Two parts. Cross-tenant "
                                "access: application data access through Strata interfaces requiring a tenant context "
                                "type, backed by PostgreSQL row-level security forced for the application role (L2 "
                                "target for this part). Intra-tenant object and partition access (donor to donor in one "
                                "sponsor, advisor beyond delegation, partner partition to partner partition): requires a "
                                "per-object authorization decision tested against a specification (L7 target); tenant "
                                "isolation does nothing for it. PostgreSQL documents that superusers, roles with "
                                "BYPASSRLS and table owners (unless FORCE ROW LEVEL SECURITY is set) bypass row "
                                "security, and that referential integrity checks always bypass it.")
        r["known_bypasses"] = r["known_bypasses"].rstrip(".") + ("; intra-tenant object identifiers accepted from the "
                                                                 "client without a per-object decision; delegation and "
                                                                 "partner-partition scope omitted from queries.")
        note(r, "Split into cross-tenant (L2 target, TENANT controls) and intra-tenant object authorization (L7 target, "
                "AUTHZ). The row is rated at the weaker part and moved to the AUTHZ family (OBJ-PENTEST-006). The "
                "cross-tenant L2 also depends on components that do not exist.")
    if cid in ("CWE-89", "CWE-564"):
        note(r, "L1 is conditional: it holds only if the Strata runtime query interface that accepts only precompiled, "
                "named queries with typed parameters is built and passes bypass tests. That interface does not exist "
                "as of 2026-11-25 (architecture/ECHELON-CURRENT-STATE-BRIEF.md); until it does, no level is achievable "
                "beyond L5 to L6 gates on driver references, and the demonstrated level is none. Do not present L1 "
                "externally before then (OBJ-PENTEST-007).")
    if fam == "NA":
        r["strongest_achievable_level"] = "not-applicable"
        note(r, "Level changed from L1 to not-applicable: absence of the platform is not elimination by construction and "
                "must not be counted among L1 rows (OBJ-SKEPTIC-008).")

    hyp = r.pop("hyp", None) or r["architecture_vs_scanning"]
    new = {}
    for k, v in r.items():
        if k == "architecture_vs_scanning":
            new["demonstrated_architecture_vs_scanning"] = "not-demonstrated"
            new["hypothesized_architecture_vs_scanning"] = hyp
        else:
            new[k] = v
        if k == "assurance_scope":
            new["claim_scope"] = scope
            new["prerequisite_components_exist"] = prereq
    out.append(new)

with open(PATH, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys()), quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    w.writeheader()
    w.writerows(out)
print("rows", len(out), "columns", len(out[0]))
