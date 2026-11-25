---
id: DD-RES-OWNER-001
title: Owner fact verification checklist
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
---

# Owner fact verification checklist

Many answer units are `unknown` not because research failed but because the facts live
with the owner (DD-VAL-ADV-002, insurer and procurement perspectives). Each item below
can be checked in minutes to hours and converts an `unknown` into either a current fact
(after evidence is recorded) or a known gap. Record each result as evidence and update
the affected answer units with a human `review`.

| # | Fact to verify | Evidence to capture | Affects |
|---|---|---|---|
| 1 | Entity formation status of Echelon Foundry, LLC: filed, date, members, managers, registered agent | State filing record | GOV, LEG, IPR, AML (OFAC 50 percent), contracting party |
| 2 | IP assignment or license from founders to the LLC | Signed assignment | IPR, ESC, LEG |
| 3 | MFA enforced on email, code hosting (GitHub), domain registrar, cloud consoles, package registries (npm, NuGet) | Admin console screenshots or exported settings | AUN, IAM, INS |
| 4 | Phishing-resistant MFA (passkeys or security keys) on administrative accounts | Settings export | AUN, INS |
| 5 | Branch protection and required review on Echelon repositories; who can push to main | Repository settings export | CHG, SDL, AIA, SCS |
| 6 | Package publishing credentials for Limen (npm) and Aegis (NuGet): who holds them, MFA, trusted publishing | Registry settings | SCS, IAM |
| 7 | Workforce devices: disk encryption, OS updates, screen lock, EDR or built-in protection | Device settings | END, INS |
| 8 | Backups of corporate data (email, documents, repositories) and last restore test | Backup configuration, restore record | BKP, INS |
| 9 | Domain and DNS inventory with registrar lock and DNSSEC status | Registrar export | NET, ASM |
| 10 | AI providers and agent platforms used for engineering, with plan tier and training and retention terms | Account plans, terms | AIG, AIS, SUB, IPR |
| 11 | Insurance held (general liability, cyber, tech E&O) or quotes requested | Certificates or quotes | INS, LEG |
| 12 | Bank and payment controls for Echelon's own accounts (dual control, call-back on payee changes) | Bank settings | FRD, INS |
| 13 | Any security incident affecting corporate systems to date | Owner attestation | IR |
| 14 | Headcount and contractors, and their access | Roster | HR, IAM, BCP |
| 15 | Whether any vulnerability report channel exists (security.txt, email) | Published file | VUL |

Note: items 3 to 8 and 12 are exactly what cyber insurance applications ask
(DD-IND-INS-001). Never answer an insurance application from target answers; carriers
may treat answers as warranties.
