---
id: DD-IND-INS-001
title: Cyber insurance underwriting profile (what applications ask)
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [due-diligence, insurance, cyber, underwriting]
---

# Cyber insurance underwriting profile

## Purpose and relevance

Customers increasingly ask vendors for cyber and technology errors and omissions
insurance (for example, a cyber insurance certificate is a gated trust artifact at Plaid,
SRC-Q-PLAID-SECURITY-PORTAL-2023). Echelon will itself apply for coverage. Carrier
applications therefore matter twice: they show the controls the insurance market treats
as gating, and they will be the questions Echelon must answer truthfully. Per DD-ARC-001,
Echelon has no insurance policy established; nothing here implies coverage exists.

Sources are public carrier application forms and a state toolkit, retrieved on
2026-11-25. Question text is not reproduced (carrier forms are copyrighted); topics are
paraphrased.

| Source ID | Form | Edition |
|---|---|---|
| SRC-Q-ATBAY-CYBER-APP-2026 | At-Bay Cyber Insurance Application | 06/2026 |
| SRC-Q-TMHCC-NETGUARD-APP-2026 | Tokio Marine HCC NetGuard Plus application | 4/2026 (from file name) |
| SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022 | Beazley Ransomware Supplemental | 05/2022 |
| SRC-Q-CORVUS-RANSOMWARE-SUPP-2022 | Corvus Ransomware Supplemental | 07/2022 |
| SRC-Q-AXIS-RANSOMWARE-SUPP | AXIS Cyber Ransomware Supplemental | 01/2022 (from form code) |
| SRC-Q-INDIANA-CYBER-INSURANCE-TOOLKIT | Indiana underwriting questions compilation | undated |

Not retrieved: technology E&O applications (Tokio Marine HCC and At-Bay technology forms
returned HTML error pages to retrieval). Search results indicated technology E&O forms ask
which contract clauses (liability caps, consequential damages disclaimers, warranty
disclaimers) the applicant uses; this is **unverified** and recorded as an open question.

## What applications ask

| Topic | What is asked | Sources | Frequency |
|---|---|---|---|
| Exposure profile | Revenue, employees, industry, domains, record counts by sensitive data type (government IDs, financial accounts, payment cards, PHI, credentials) | SRC-Q-ATBAY-CYBER-APP-2026, SRC-Q-TMHCC-NETGUARD-APP-2026 | All |
| MFA for email | Enforced on all email access, including web mail and non-corporate devices | SRC-Q-ATBAY-CYBER-APP-2026, SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022, SRC-Q-CORVUS-RANSOMWARE-SUPP-2022, SRC-Q-TMHCC-NETGUARD-APP-2026 | All |
| MFA for remote access | All remote network access including VPN; named MFA provider; VPN product and hosting | SRC-Q-ATBAY-CYBER-APP-2026, SRC-Q-TMHCC-NETGUARD-APP-2026, SRC-Q-CORVUS-RANSOMWARE-SUPP-2022 | All |
| MFA for privileged and vendor access | Domain admin accounts, PAM tool access, third-party or vendor access; factor type (SMS, authenticator, security key) | SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022, SRC-Q-AXIS-RANSOMWARE-SUPP, SRC-Q-INDIANA-CYBER-INSURANCE-TOOLKIT | Most |
| MFA as a continuing representation | Answering yes represents MFA is enforced before inception and will remain so for the policy period | SRC-Q-TMHCC-NETGUARD-APP-2026 | One (high impact) |
| EDR | Product name, management model (in-house or MDR), coverage of 100% of workstations and servers, automatic containment | SRC-Q-ATBAY-CYBER-APP-2026, SRC-Q-TMHCC-NETGUARD-APP-2026, SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022, SRC-Q-INDIANA-CYBER-INSURANCE-TOOLKIT | All |
| SOC / 24x7 monitoring | Existence, hours, internal or outsourced, authority to remediate | SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022, SRC-Q-AXIS-RANSOMWARE-SUPP | Most ransomware forms |
| Backups | Offline or air-gapped, cloud backup vs sync services, immutability, encryption, offline copy of decryption keys, MFA on backup access, restore testing frequency, integrity checks, time to restore all data | SRC-Q-ATBAY-CYBER-APP-2026, SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022, SRC-Q-CORVUS-RANSOMWARE-SUPP-2022, SRC-Q-AXIS-RANSOMWARE-SUPP, SRC-Q-TMHCC-NETGUARD-APP-2026, SRC-Q-INDIANA-CYBER-INSURANCE-TOOLKIT | All |
| BC/DR and incident response | BC/DR plan tested in the last year; ransomware tabletop in last two years | SRC-Q-ATBAY-CYBER-APP-2026, SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022, SRC-Q-CORVUS-RANSOMWARE-SUPP-2022 | Most |
| Email security | Secure email gateway product, attachment detonation, link screening, external tagging, SPF, DKIM, DMARC, macros disabled, legacy protocols disabled | SRC-Q-ATBAY-CYBER-APP-2026, SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022, SRC-Q-CORVUS-RANSOMWARE-SUPP-2022 | Most |
| Training | Phishing training and simulations, remedial training, role-based training | SRC-Q-ATBAY-CYBER-APP-2026, SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022, SRC-Q-AXIS-RANSOMWARE-SUPP | All |
| Privileged account hygiene | Local admin rights, PAM coverage, number of domain admin and service accounts, service account interactive login denial, long or random passwords, rotation, vaulting | SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022, SRC-Q-AXIS-RANSOMWARE-SUPP | Ransomware forms |
| Asset and configuration management | Asset discovery, CMDB, end-of-life software and its segregation, hardened baselines | SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022 | Ransomware forms |
| Vulnerability and patching | Scan coverage percentage and frequency, pen test frequency, critical and normal patch time targets | SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022, SRC-Q-AXIS-RANSOMWARE-SUPP, SRC-Q-ATBAY-CYBER-APP-2026 | Most |
| Network exposure | RDP and remote tools exposure and MFA, inbound SMB, default-deny firewalls, protective DNS, segmentation, SSL VPN login pages tied to declared domains | SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022, SRC-Q-AXIS-RANSOMWARE-SUPP, SRC-Q-TMHCC-NETGUARD-APP-2026 | Most |
| Encryption and data governance | Encryption of stored data; written data governance policies; retention schedules | SRC-Q-ATBAY-CYBER-APP-2026, SRC-Q-CORVUS-RANSOMWARE-SUPP-2022, SRC-Q-INDIANA-CYBER-INSURANCE-TOOLKIT | Most |
| Payment fraud controls | Dual authorization for transfers above a threshold ($25,000 in one form); call-back verification of new or changed payee instructions; verification of vendor bank accounts before AP setup | SRC-Q-ATBAY-CYBER-APP-2026, SRC-Q-TMHCC-NETGUARD-APP-2026, SRC-Q-INDIANA-CYBER-INSURANCE-TOOLKIT | Most |
| Compliance attestations | HIPAA, PCI DSS level, outsourced card processing | SRC-Q-ATBAY-CYBER-APP-2026, SRC-Q-INDIANA-CYBER-INSURANCE-TOOLKIT | Most |
| IT and security resourcing | IT budget share on security, security headcount, named CISO or equivalent, use of an MSP | SRC-Q-BEAZLEY-RANSOMWARE-SUPP-2022, SRC-Q-ATBAY-CYBER-APP-2026 | Some |
| Cloud platforms | Which IaaS platforms are used | SRC-Q-CORVUS-RANSOMWARE-SUPP-2022 | Some |
| Media liability | Licensed third-party content and legal review before publishing | SRC-Q-ATBAY-CYBER-APP-2026 | Some |
| Loss history and known circumstances | Prior cyber events above a threshold in three years; awareness of facts that could give rise to a claim | SRC-Q-ATBAY-CYBER-APP-2026 | All |

## Observations

- **Controls become warranties.** At least one form converts the MFA answer into a
  continuing representation for the policy period (SRC-Q-TMHCC-NETGUARD-APP-2026). An
  inaccurate or lapsed answer can jeopardize coverage. Echelon answers must be verified,
  not aspirational.
- **Product names are asked.** EDR, email security, MFA and VPN products are named in
  pick lists, because carriers track vulnerable products. Generic answers ("we use
  endpoint protection") are insufficient.
- **Ransomware recovery dominates.** Backup immutability, offline keys and restore time
  appear in every form.
- **Payment fraud controls overlap with Unbound's product.** Dual authorization and
  call-back verification are asked of the applicant's own finance function, but DAF
  sponsors will ask the same questions about Unbound grant disbursement workflows
  (see DD-QNR-001 topic 32).
- **Applications target the corporate environment, not the hosted product.** Customer
  questionnaires target the product. Both sets are needed in the question bank, tagged by
  population.

## Implications for Echelon (proposed, not implemented)

| Underwriting expectation | Echelon current state (DD-ARC-001) | Answer status |
|---|---|---|
| MFA on email, remote, privileged, backup and vendor access | Not established | `unknown` |
| EDR on 100% of endpoints, monitored | Not established | `unknown` |
| Immutable, offline, encrypted backups with tested restores | Not established; Unbound requirements describe intent | `proposed-target-state` for Unbound, `unknown` corporately |
| Tested BC/DR and ransomware tabletop | Not established | `unknown` |
| Dual authorization and call-back verification for payments | Not established | `unknown` |
| Named security contact | Not established | `unknown` |

## Open questions

- Retrieve and review a public technology E&O application to confirm contract-clause
  questions (liability caps, consequential damages, warranties, beta products).
- Determine whether DAF sponsors specify minimum cyber and E&O limits for vendors (not
  found publicly; public-sector RFPs set limits per solicitation, per search results only).
