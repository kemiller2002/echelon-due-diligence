import json

VON = "2026-11-25"


def V(ok, method, url=None):
    v = {"verified": ok, "verified_on": VON, "method": method}
    if url:
        v["evidence_url"] = url
    return v


def R(id, title, issuer, type, authority, version, pub, url, applicability, license,
      limitations, status, verification, jur=None, ind=None, eff=None, sup=None,
      rel=None, notes=None):
    r = {"id": id, "title": title, "issuer": issuer, "type": type, "authority": authority,
         "version": version, "publication_date": pub}
    if eff:
        r["effective_date"] = eff
    r["url"] = url
    if jur:
        r["jurisdictions"] = jur
    if ind:
        r["industries"] = ind
    r["applicability"] = applicability
    r["license"] = license
    r["limitations"] = limitations
    r["status"] = status
    if sup:
        r["superseded_by"] = sup
    if rel:
        r["related_sources"] = rel
    if notes:
        r["notes"] = notes
    r["verification"] = verification
    return r


def write(path, recs):
    with open(path, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


NIST_LIC = ("NIST Technical Series publication. Per NIST's copyright and licensing statement for "
            "Technical Series Publications (fetched 2026-11-25), works authored by NIST employees are "
            "not subject to copyright protection within the United States; foreign rights are reserved "
            "and NIST grants a non-exclusive license outside the US. Reuse and quotation permitted with "
            "citation; third-party material inside a publication may carry its own rights.")
NIST_LIC_URL = "https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-software-and-technical-series-publications"

ISO_LIC = ("Copyrighted ISO/IEC publication sold per copy (price shown on the IEC Webstore). Text may "
           "not be reproduced or redistributed without a license. Echelon may cite clause and control "
           "identifiers and write original paraphrase only; do not copy control text into questions, "
           "answers or customer documents.")
ISO_ONLY_LIC = ("Copyrighted ISO publication sold per copy. Text may not be reproduced or redistributed "
                "without a license. Cite clause numbers and paraphrase only.")

US_GOV_LIC = ("US federal government work; not subject to US copyright (17 U.S.C. 105). Free to reuse "
              "and quote with citation.")
EU_LIC = ("EU legal act published in the Official Journal. EUR-Lex content may be reused with "
          "acknowledgment under the Commission reuse policy (Decision 2011/833/EU); only the OJ "
          "edition is authentic.")

ECH = ("Echelon Foundry (small US software company, Indiana LLC, no production system, no SOC report, "
       "no ISO certificate as of 2026-11-25)")
UNB = ("Unbound (DAF administration platform, requirements stage only, intended to serve DAF sponsors "
       "including financial-institution-affiliated sponsors)")
