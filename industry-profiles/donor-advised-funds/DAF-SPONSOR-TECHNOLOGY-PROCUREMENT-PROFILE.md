---
id: DD-IND-DAF-001
title: DAF sponsor technology procurement profile
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [due-diligence, donor-advised-funds, industry-profile, third-party-risk]
---

# DAF sponsor technology procurement profile

## Purpose and classification rules

For each organization relevant to Unbound, this profile records what is publicly
documented about supplier or vendor security, privacy and risk requirements. Each finding
is classified as:

- **Documented:** stated in a retrieved public document about vendors, service providers
  or third parties of that organization.
- **Inferred:** a reasonable inference from documented facts (for example, that a sponsor
  administered by a parent company would apply that parent's supplier process). The basis
  is stated.
- **Unknown:** nothing public was found.

An organization's description of its own security controls is **not** treated as a vendor
requirement (DD-GOV-001 rule 2). Where such statements imply a product constraint for
Unbound, that is labeled as an inference.

All `SRC-Q-` sources were retrieved on 2026-11-25 unless marked unverified. No login-gated
supplier portal or confidential material was accessed.

## Summary

| Organization | Operating model (documented) | Vendor requirements documented? | Best available proxy |
|---|---|---|---|
| Fidelity Charitable | Contracts with FMR LLC and affiliates; National Charitable Services LLC provides administration and recordkeeping | No (for the charity); Yes (for Fidelity Investments suppliers) | SRC-Q-FIDELITY-SUPPLIER-POLICIES (inferred applicability) |
| National Philanthropic Trust | Independent sponsor; runs private-label DAF programs and the GivingPoint portal for financial institutions | Partial: privacy policy states service provider flow-down | SRC-Q-NPT-TERMS-PRIVACY |
| DAFgiving360 (Schwab) | Charles Schwab & Co. provides administrative services (search snippet only) | Unknown (privacy notice not retrievable) | Schwab supplier requirements not found publicly |
| American Endowment Foundation | Independent sponsor; uses cloud hosting service providers | No | SRC-Q-AEF-PRIVACY-POLICY |
| Greater Horizons | Affiliate of Greater Kansas City Community Foundation | Partial: consent-based service provider login | SRC-Q-GKCCF-PRIVACY-POLICY |
| Edward Jones Charitable Gift Fund | Third-party administrator runs day-to-day operations | No (firm has a non-public Third Party Management Policy) | SRC-Q-EDWARD-JONES-DAF-BROCHURE, SRC-Q-EDWARD-JONES-CODE |
| Vanguard Charitable | Independent charity; shares data with Vanguard Group representatives when authorized and with technology vendors | Partial: confidentiality agreements required | SRC-Q-VANGUARD-CHARITABLE-PRIVACY |
| Morgan Stanley GIFT | Investment management by Morgan Stanley Smith Barney; back office administration by RenPSG (unaffiliated) | Yes for Morgan Stanley suppliers; applicability to GIFT vendors inferred | SRC-Q-MS-GIFT-PAGE, SRC-Q-MS-MIN-SECURITY-STANDARDS |
| Goldman Sachs Philanthropy Fund | Affiliated DAF sponsor; administrator not determined | Yes for Goldman Sachs vendors; applicability to the fund unknown | SRC-Q-GS-VENDOR-TECH-RISK-EXPECTATIONS |
| Bank of America Charitable Gift Fund | Bank of America N.A. is sole trustee | Yes for Bank of America suppliers (detailed document non-public) | SRC-Q-BOA-CGF-GUIDELINES-2024, SRC-Q-BOA-SUPPLIER-EXPECTATIONS |
| Community foundations | Varied; many use packaged fund accounting and donor portals | Unknown (no public vendor requirements found) | Privacy policies only |
| Independent wealth managers and RIAs | Regulation S-P service provider oversight | Regulatory-driven (see DD-IND-FS-001) | SRC-Q-SEC-REG-SP-2024-FACT-SHEET |
| Custodians | Integration programs | Unknown | none |
| Third-party DAF administrators (Ren, Foundation Source, others) | Provide administration to sponsors | Unknown for their own vendors; Ren claims SOC 2 Type 1 | SRC-Q-GIVINGCOMPASS-REN-2026 |

## Per-organization findings

### Fidelity Charitable

| Finding | Class | Source IDs |
|---|---|---|
| The Trustees contracted with FMR LLC and affiliated companies for administrative and investment management services; National Charitable Services LLC provides administrative and recordkeeping services; payments to FMR equal the administrative fee net of tier credits | Documented (audited financial statement note 7) | SRC-Q-FC-AUDITED-FS-FY2025 |
| National Charitable Services provides services to Fidelity Charitable and collects donor personal information in that role | Documented | SRC-Q-NCS-PRIVACY-POLICY |
| A technology vendor supporting Fidelity Charitable operations is likely to contract with, or be assessed by, FMR and therefore meet Fidelity Supplier Policies (background investigations, accessibility with third-party ACR, location disclosure) | Inferred, Medium confidence. Basis: administration is contracted to FMR. Not stated by Fidelity Charitable | SRC-Q-FIDELITY-SUPPLIER-POLICIES, SRC-Q-FC-AUDITED-FS-FY2025 |
| Fidelity Charitable tells donors to log in only through its site and to avoid third-party tools that ask for Giving Account credentials | Documented (own control statement, not a vendor requirement) | SRC-Q-FC-SECURITY-PAGE |
| Implication: any Unbound integration with Fidelity Charitable must not depend on donor credential sharing or screen scraping; an official API or file-based arrangement would be needed | Inferred, High confidence | SRC-Q-FC-SECURITY-PAGE |
| Fidelity Charitable reviews every grant recommendation and recipient and cites AI-enabled fraud; transactions may take longer for verification | Documented (own control) | SRC-Q-FC-SECURITY-PAGE |
| Fidelity Charitable's own vendor security questionnaire or supplier code | Unknown | none |

Relationship note: Fidelity Charitable is more likely a competitor or integration
counterparty than a buyer of a DAF administration platform, because administration is
already provided by FMR. This is an inference.

### National Philanthropic Trust (NPT)

| Finding | Class | Source IDs |
|---|---|---|
| NPT limits access to personal data to employees, agents, contractors and other third parties with a need to know, who process only on NPT instructions under a duty of confidentiality; NPT transfers personal data to a third party only if it agrees to comply with NPT procedures and policies or puts adequate measures in place | Documented (privacy policy, last updated October 29, 2026) | SRC-Q-NPT-TERMS-PRIVACY |
| NPT offers private-label DAF programs to financial institutions with advisor and client dashboards and claims "industry-certified security and compliance" | Documented (marketing) | SRC-Q-NPT-FINANCIAL-INSTITUTIONS |
| Financial institution partners of NPT expect certified security from their DAF technology; NPT is both a potential buyer of components and a direct competitor of Unbound in the private-label market | Inferred, Medium | SRC-Q-NPT-FINANCIAL-INSTITUTIONS |
| The specific certification NPT holds; NPT vendor questionnaire content | Unknown | none |

### DAFgiving360 (Charles Schwab)

| Finding | Class | Source IDs |
|---|---|---|
| Privacy notice reportedly states information is shared with Charles Schwab & Co., Inc. so that it can provide administrative services to DAFgiving360, and lists service provider categories (hosting, IT infrastructure, communications, marketing) | Unverified (search snippets only; site returned HTTP 403) | SRC-Q-DAFGIVING360-PRIVACY |
| Schwab supplier security requirements | Unknown. Schwab's public Code of Business Conduct applies to employees and contingent workers; no supplier security document was found | none |
| If administration is provided by Schwab, a technology vendor would likely be assessed under Schwab TPRM | Inferred, Low to Medium (depends on the unverified administration statement) | SRC-Q-DAFGIVING360-PRIVACY |

### American Endowment Foundation (AEF)

| Finding | Class | Source IDs |
|---|---|---|
| AEF shares information with cloud hosting service providers; many service providers are US companies; data transmitted to them is handled under their own privacy policies; AEF states encryption is its strategy for stored personal information | Documented (privacy policy, March 2024) | SRC-Q-AEF-PRIVACY-POLICY |
| The policy disclaims governing practices of third-party service providers even when branded as or provided on behalf of AEF | Documented | SRC-Q-AEF-PRIVACY-POLICY |
| Implication: a white-labeled Unbound service for AEF would fall outside AEF's privacy policy, so Unbound would need its own donor-facing privacy notice or a contractual arrangement to operate under AEF's | Inferred, Medium | SRC-Q-AEF-PRIVACY-POLICY |
| AEF vendor requirements | Unknown | none |

### Greater Horizons (Greater Kansas City Community Foundation affiliate)

| Finding | Class | Source IDs |
|---|---|---|
| Privacy policy covering the Community Foundation and affiliates including Greater Horizons (September 2024) states service representatives of third-party Service Providers may log in to a user's account, with consent, to troubleshoot | Documented | SRC-Q-GKCCF-PRIVACY-POLICY |
| Implication: Unbound support access to donor accounts should be consent-gated, time-bounded and logged so the sponsor's notice remains accurate | Inferred, High | SRC-Q-GKCCF-PRIVACY-POLICY |
| Vendor security requirements | Unknown | none |

### Edward Jones (Edward Jones Charitable Gift Fund)

| Finding | Class | Source IDs |
|---|---|---|
| A third-party administrator is responsible for day-to-day operations of the DAF | Documented (client brochure; administrator not named) | SRC-Q-EDWARD-JONES-DAF-BROCHURE |
| Edward Jones maintains a Third Party Management Policy and treats third-party risk as a top concern, especially for critical third parties | Documented (code of conduct); policy content not public | SRC-Q-EDWARD-JONES-CODE |
| The sponsoring organization and administrator are Renaissance Charitable Foundation and Ren | Unverified (search snippet of a Ren help article; the article URL returned 404) | none |
| Vendor requirements for the DAF program | Unknown | none |

### Vanguard Charitable

| Finding | Class | Source IDs |
|---|---|---|
| Third parties receiving personal data are bound by agreements with Vanguard Charitable protecting confidentiality; data may be shared with third-party technology vendors to diagnose or troubleshoot; HyperWallet (a PayPal service) is used for certain payments; account-level permission extends to designated Vanguard Group representatives | Documented (privacy policy, May 16, 2023) | SRC-Q-VANGUARD-CHARITABLE-PRIVACY |
| Vanguard Group supplier security requirements | Unknown (no public document found) | none |

### Morgan Stanley (Morgan Stanley Global Impact Funding Trust, MS GIFT)

| Finding | Class | Source IDs |
|---|---|---|
| Morgan Stanley Smith Barney LLC provides investment management; back office administration is provided by RenPSG, an unaffiliated charitable gift administrator | Documented | SRC-Q-MS-GIFT-PAGE |
| Morgan Stanley publishes Minimum Security Standards, IT and cyber security standards, Third Party Regulatory Requirements and Data Processing Terms for suppliers | Documented | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-MS-SECURITY-STANDARDS-IT-CYBER, SRC-Q-MS-THIRD-PARTY-REG-REQS, SRC-Q-MS-DATA-PROCESSING-TERMS |
| A technology vendor contracted by Morgan Stanley for GIFT would meet these documents; a vendor contracted by RenPSG would face RenPSG's requirements (unknown), possibly with Morgan Stanley flow-down | Inferred, Medium | SRC-Q-MS-GIFT-PAGE, SRC-Q-MS-MIN-SECURITY-STANDARDS |
| Unbound is a potential replacement for or complement to RenPSG; the incumbent publicly claims SOC 2 Type 1 | Inferred (competitive context) | SRC-Q-GIVINGCOMPASS-REN-2026 |

### Goldman Sachs (Goldman Sachs Philanthropy Fund)

| Finding | Class | Source IDs |
|---|---|---|
| Goldman Sachs publishes General Vendor Technology Risk Expectations and a Vendor Code of Conduct | Documented | SRC-Q-GS-VENDOR-TECH-RISK-EXPECTATIONS, SRC-Q-GS-VENDOR-CODE |
| The Philanthropy Fund's administrator and whether firm vendor requirements apply to the fund's technology vendors | Unknown | none |

### Bank of America (Bank of America Charitable Gift Fund)

| Finding | Class | Source IDs |
|---|---|---|
| Bank of America, N.A. is the named sole trustee; all activities are subject to the trustee's discretion; donors use an online portal | Documented | SRC-Q-BOA-CGF-GUIDELINES-2024 |
| Bank of America suppliers are expected to meet a non-public Service Provider Security Requirements Document covering information security, business continuity, change management, data management, retention and destruction | Documented (existence); content unknown | SRC-Q-BOA-SUPPLIER-EXPECTATIONS |
| A technology vendor to the Charitable Gift Fund would contract with or through a national bank and be subject to bank TPRM under the interagency guidance | Inferred, High | SRC-Q-BOA-CGF-GUIDELINES-2024, SRC-INTERAGENCY-TPRM-2023 |

### Community foundations (general)

| Finding | Class | Source IDs |
|---|---|---|
| No community foundation reviewed publishes vendor security requirements | Unknown | none |
| Community foundation privacy notices describe service providers and consent-based support access (Greater Horizons example) | Documented for one | SRC-Q-GKCCF-PRIVACY-POLICY |
| Community foundations are likely to accept vendor-standard assurance (SOC 2, HECVAT-like questionnaires) rather than impose bespoke control documents, and procurement depth will vary widely by size | Inferred, Low | none |

### Independent wealth managers and RIAs

See DD-IND-FS-001. Documented driver: Regulation S-P service provider oversight and 72-hour
service provider breach notice (SRC-Q-SEC-REG-SP-2024-FACT-SHEET). The adviser outsourcing
rule proposal was withdrawn (SRC-Q-DECHERT-SEC-WITHDRAWALS-2025). RIAs that recommend a DAF
sponsor are not necessarily the contracting party for Unbound; their diligence would focus
on data shared through advisor portals and integrations.

### Custodians

Unknown. Schwab Advisor Services integration pages returned HTTP 403. Integration
security criteria are typically disclosed under integration agreements.

### Third-party DAF administrators

| Organization | Finding | Class | Source IDs |
|---|---|---|---|
| Ren (Renaissance) | Indianapolis-based administrator serving financial services firms, nonprofits and community foundations; described as holding SOC 2 Type 1 (May 2026 press release) | Documented (secondary) | SRC-Q-GIVINGCOMPASS-REN-2026 |
| RenPSG | Back office administrator for MS GIFT | Documented | SRC-Q-MS-GIFT-PAGE |
| NPT technology (GivingPoint) | Private-label portal with claimed industry-certified security | Documented (marketing) | SRC-Q-NPT-FINANCIAL-INSTITUTIONS |
| National Charitable Services | Administrator and recordkeeper for Fidelity Charitable | Documented | SRC-Q-FC-AUDITED-FS-FY2025 |
| Foundation Source, Foundant and others | Market DAF or community foundation platforms; no assurance artifacts retrieved | Unknown | none |
| "FCS" (named in the research brief) | Could not be identified with confidence; no matching administrator found | Unknown | none |

## Cross-cutting implications for Unbound (inferences, to be validated)

1. **The buyer is often a parent institution's TPRM function.** Sponsors affiliated with
   Fidelity, Morgan Stanley, Bank of America and possibly Schwab and Goldman Sachs are
   administered by or through the parent or an outsourced administrator. Expect large-bank
   supplier standards (DD-IND-FS-001) rather than charity-sized questionnaires.
2. **Credential-free integration.** Documented sponsor warnings against credential-sharing
   tools mean Unbound integrations must use sponsor-sanctioned interfaces.
3. **Consent-based support access** should be a product capability, because sponsor
   privacy notices describe it.
4. **Privacy notice ownership** for white-labeled services must be designed, because at
   least one sponsor disclaims coverage of branded third-party services.
5. **Incumbent assurance baseline is modest** (one administrator publicly cites SOC 2
   Type 1). A credible SOC 2 Type II would be differentiating, but large-bank sponsors will
   still apply their own standards.

## Open questions

- Who administers the Goldman Sachs Philanthropy Fund and the Edward Jones Charitable Gift
  Fund (sponsor and administrator names to be confirmed from Form 990 Schedule R or
  program disclosures)?
- Confirm DAFgiving360 administration arrangements from a retrievable copy of its privacy
  notice or Form 990.
- Do any community foundations publish vendor security requirements or use HECVAT-like
  instruments? Requires targeted outreach or procurement portal review.
- Identify the administrator referred to as "FCS".
