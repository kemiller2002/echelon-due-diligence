from qbc_aitpraml import Cat, challenge

C = Cat("SUB",
        industries=["all"],
        jurisdictions=["global"],
        products=["all-echelon-products"])

C.au(1, title="Published subprocessor register generated from the vendor inventory",
     status="proposed-target-state",
     rationale="UNB-XIN-SAS-011 requires a per-tenant register of subprocessors (name, function, data classes, location) generated from the vendor inventory. Neither the inventory nor the register exists.",
     target="Echelon publishes a subprocessor register per tenant, generated from the vendor inventory and from integration configuration, listing each subprocessor's legal entity, function, data categories, processing and support locations and transfer mechanism. Vendors without access to customer data are excluded and the distinction is documented. Because the register is generated from the configuration that actually routes data, an integration that sends customer data to an unlisted party fails a release check.",
     current="Not established; there are no customers or production data flows.",
     intended="Generate the register from the vendor inventory (TPR) and a data-flow declaration checked at release.",
     provable="Nothing.",
     statement="Echelon plans to publish a per-customer subprocessor list generated from its vendor inventory and data-flow configuration. No list exists yet because no production service processes customer data.",
     kind="planned",
     controls=[1, 2], evrs=[1, 2],
     requirements=["UNB-XIN-SAS-011", "SOC2-013"],
     freshness="per-event", mechanism="event-driven-automated", automation="high",
     impl_cost="low", rec_cost="low",
     disclosure="public",
     owner="Not assigned (proposed: Echelon privacy owner)")

C.au(2, title="Advance notice of subprocessor changes and customer objection rights",
     status="proposed-target-state",
     rationale="UNB-XIN-SAS-011 requires notice to tenant administrators at least 30 days before adding or replacing a subprocessor for that tenant's data, and within 72 hours with reason for emergency replacement. Objection rights are not specified in located requirements.",
     target="Echelon notifies subscribed customer contacts at least 30 days before adding or replacing a subprocessor, or changing a subprocessor's location or processing scope, with the register diff. Emergency replacements are notified within 72 hours with the reason. Customers may object on reasonable data protection grounds; Echelon then offers an alternative configuration that avoids the subprocessor for that tenant where technically possible, or a termination right with pro-rated refund. Notices are generated from the register diff so none can be skipped.",
     current="Not established.",
     intended="Implement per UNB-XIN-SAS-011 with objection handling defined in the customer agreement.",
     provable="Nothing.",
     statement="Echelon plans 30 days' advance notice of subprocessor changes, 72-hour notice for emergency replacements, and an objection right. Not yet in place.",
     kind="planned",
     controls=[3], evrs=[3],
     requirements=["UNB-XIN-SAS-011"],
     freshness="per-event", mechanism="event-driven-automated", automation="full",
     impl_cost="low", rec_cost="low",
     disclosure="public",
     owner="Not assigned (proposed: Echelon privacy owner)",
     challenge=challenge(
         intent="Customers want control over who processes their data and time to assess changes.",
         adverse="A new subprocessor with weak controls or in an unacceptable jurisdiction receives customer data without the customer's knowledge.",
         conv_eff="Notice periods work, but objection rights are rarely exercised and often end only in a right to terminate, which customers cannot practically use.",
         legal="GDPR Article 28(2) requires prior specific or general written authorization and information about changes with an opportunity to object, where GDPR applies. US law generally does not require this.",
         contract="Very common in data processing agreements.",
         history="GDPR-era DPA convention, now applied globally.",
         elim="Per-tenant routing can make some subprocessors optional so an objecting customer is excluded rather than forced to terminate.",
         auto="Notices generated from register diffs; data-flow check blocks unlisted subprocessors.",
         cont="Register history and notice delivery records.",
         alt="Per-tenant subprocessor selection where feasible, so objection leads to exclusion rather than termination.",
         verif="Customers can verify their tenant's register and the release check.",
         accept="Likely; it gives customers more control than standard terms.",
         invalid="Core infrastructure providers (cloud host) cannot be made optional per tenant.",
         conv_cost="low",
         alt_cost="medium (per-tenant routing complexity)",
         alt_risk="Configuration variety increases testing burden and isolation complexity.",
         pro=["Real control instead of a theoretical right.", "Automated notices cannot be forgotten."],
         con=["Per-tenant variability adds complexity.", "Not possible for core hosting."],
         tech="stronger", inst="likely"))

C.au(3, title="Flow-down terms and oversight of subprocessors",
     status="unknown",
     rationale="No data processing agreement template or subprocessor contracts were located. SOC2-013 requires contracts and monitoring of subservice organizations; TPR controls would apply.",
     target="Each subprocessor is bound by written terms at least as protective as Echelon's commitments to the customer: confidentiality, security measures, purpose limitation including no AI training on customer data, breach notice, assistance with data subject requests, deletion at end of service, audit rights and approval of further sub-subprocessors. Echelon remains responsible to the customer for subprocessor performance. Subprocessors are monitored under the TPR program at the tier their data access implies.",
     current="Unknown.",
     intended="Create a DPA template and flow-down checklist; record each subprocessor's terms in the vendor register.",
     provable="Nothing.",
     statement="Echelon has not yet established subprocessor flow-down terms. It plans to bind subprocessors to terms at least as protective as its customer commitments and to remain responsible for their performance.",
     kind="not-available",
     controls=[4], evrs=[4],
     requirements=["SOC2-013", "SOC2-022"],
     freshness="P1Y", mechanism="periodic-manual", automation="low",
     impl_cost="low", rec_cost="low",
     owner="Not assigned (proposed: Echelon counsel)",
     residual=["Large providers' standard DPAs may not match every customer-specific commitment."])

C.au(4, title="Data location, processing location and cross-border transfers",
     status="unknown",
     rationale="No hosting region, support location or transfer mechanism has been decided in any record located. CNV-ARC-001 specifies one managed PostgreSQL cluster but not its region.",
     target="Customer data, backups, logs, AI inference and support access are confined to documented regions, by default the United States, enforced by infrastructure configuration and provider region settings and verified by automated configuration checks. Any processing outside the region, including AI inference and follow-the-sun support, is listed in the register with its transfer mechanism (for EU or UK personal data, Standard Contractual Clauses or the Data Privacy Framework where the recipient is certified).",
     current="Unknown; no production hosting decision located.",
     intended="Decide hosting region and AI inference region before production and encode them as checked configuration.",
     provable="Nothing.",
     statement="Echelon has not yet fixed its hosting and processing locations. It intends US-only processing by default, including AI inference, enforced by configuration.",
     kind="planned",
     controls=[5], evrs=[5],
     requirements=["CNV-ARC-001"],
     freshness="P1D", mechanism="continuous-automated", automation="high",
     impl_cost="low", rec_cost="low",
     owner="Not assigned (proposed: Echelon engineering owner)",
     open=["Do the AI providers in use offer US-only inference commitments under Echelon's account terms?"])

C.au(5, title="AI providers as subprocessors",
     status="unknown",
     rationale="Unbound requires AI inference metering (CNV-ECO-001) and subprocessor notice (UNB-XIN-SAS-011) but does not specify how AI providers appear in the register, which legal entity is the subprocessor when models are reached through a cloud marketplace, or whether engineering AI tools ever receive customer data. Echelon uses AI coding agents whose providers receive repository content.",
     target="Every AI provider that receives customer content is a listed subprocessor, naming the contracting entity that processes the data (for example the cloud platform hosting a model rather than the model developer, where that is the case), its region and its retention terms. Switching to a new AI provider, or to a different hosting route for a model, triggers the subprocessor notice process; changing model version within the same provider and route does not, but is recorded in the AI inventory. Engineering AI tools never receive customer data, enforced by keeping customer data out of engineering environments; if that ever changes, those providers become subprocessors and are listed.",
     current="Unknown. AI coding agent providers receive Echelon source and repository content; no customer data exists in engineering environments because there are no customers.",
     intended="Add AI provider fields to the subprocessor register and a rule keeping customer data out of engineering environments.",
     provable="Nothing.",
     statement="Echelon plans to list every AI provider that receives customer content as a subprocessor and to give advance notice before adding or switching one. Its engineering AI tools are not intended to receive customer data. Not yet in place.",
     kind="planned",
     controls=[6], evrs=[6],
     requirements=["UNB-XIN-SAS-011", "CNV-ECO-001", "SOC2-028"],
     freshness="per-event", mechanism="event-driven-automated", automation="high",
     impl_cost="low", rec_cost="low",
     owner="Not assigned (proposed: Echelon privacy owner)")

# ---------------- Controls ----------------
C.ctl(1, title="Generated per-tenant subprocessor register",
      objective="The subprocessor register for each tenant is generated from the vendor inventory and data-flow configuration and published.",
      type="detective-automated", level="L6-automated-analysis",
      systems=["not yet assigned"],
      related=["UNB-XIN-SAS-011"],
      refs=["SRC-GDPR|Art. 28|r", "SRC-ISO-27018||r", "SRC-CSA-CCM-V4|STA|r"],
      evrs=[1], owner="Not assigned (proposed: Echelon privacy owner)")
C.ctl(2, title="Release check blocks data flows to unlisted subprocessors",
      objective="A release fails if configuration routes customer data to a party absent from that tenant's register.",
      type="preventive-gate", level="L5-build-release-gate",
      systems=["not yet assigned"],
      related=["UNB-XIN-SAS-011", "SOC2-030"],
      refs=["SRC-GDPR|Art. 28|r"],
      evrs=[2], owner="Not assigned (proposed: Echelon engineering owner)")
C.ctl(3, title="Automated subprocessor change notice and objection workflow",
      objective="Register diffs generate notices 30 days ahead (72 hours after for emergencies, with reason); objections are recorded and resolved by exclusion or termination right.",
      type="preventive-procedural", level="L6-automated-analysis",
      systems=["not yet assigned"],
      related=["UNB-XIN-SAS-011"],
      refs=["SRC-GDPR|Art. 28(2)|d", "SRC-EU-SCC-2021|Clause 9|d", "SRC-EDPB-GL-07-2020||r"],
      evrs=[3], owner="Not assigned (proposed: Echelon privacy owner)")
C.ctl(4, title="Subprocessor flow-down terms",
      objective="Subprocessors are bound by terms at least as protective as customer commitments, including no AI training and sub-subprocessor approval; Echelon remains responsible.",
      type="administrative", level="L10-external-or-manual",
      systems=["not yet assigned"],
      related=["SOC2-013"],
      refs=["SRC-GDPR|Art. 28(4)|d", "SRC-EU-SCC-2021|Clause 9|r", "SRC-ISO-27001-2022|A.5.20|r"],
      evrs=[4], owner="Not assigned (proposed: Echelon counsel)")
C.ctl(5, title="Region enforcement by configuration with automated verification",
      objective="Storage, backup, logging, AI inference and support access are restricted to documented regions by configuration, continuously verified.",
      type="preventive-structural", level="L9-runtime-monitored",
      systems=["not yet assigned"],
      refs=["SRC-NIST-SP800-53-R5|SA-9(5)|r", "SRC-GDPR|Art. 46|r", "SRC-EU-US-DPF||r"],
      evrs=[5], owner="Not assigned (proposed: Echelon engineering owner)")
C.ctl(6, title="AI provider subprocessor listing and engineering data exclusion",
      objective="AI providers receiving customer content are listed with contracting entity, region and retention; customer data is excluded from engineering environments where AI coding agents operate.",
      type="preventive-structural", level="L3-restricted-interface",
      systems=["not yet assigned"],
      related=["UNB-XIN-SAS-011", "CNV-ARC-002"],
      refs=["SRC-GDPR|Art. 28|r", "SRC-NIST-AI-RMF-1.0|GOVERN 6.1|r"],
      evrs=[6], owner="Not assigned (proposed: Echelon privacy owner)")

# ---------------- Evidence ----------------
C.evr(1, title="Published subprocessor register and history", description="Per-tenant register with entity, function, data categories, locations, transfer mechanism, and version history.",
      mechanism="event-driven-automated", freshness="per-event", format="Web page and JSON", disclosure="public")
C.evr(2, title="Data-flow release check results", description="Per release: data-flow destinations compared to tenant registers, with failures.",
      mechanism="event-driven-automated", freshness="per-event", format="CI report", disclosure="internal")
C.evr(3, title="Subprocessor notice and objection log", description="Notices sent with dates and recipients, emergency notices with reasons, objections and resolutions.",
      mechanism="event-driven-automated", freshness="per-event", format="Notification log", disclosure="customer-only")
C.evr(4, title="Subprocessor terms register", description="Per subprocessor: DPA reference, flow-down checklist result, sub-subprocessor approvals.",
      mechanism="periodic-manual", freshness="P1Y", format="Register entry", disclosure="nda")
C.evr(5, title="Region configuration verification", description="Automated check results showing data stores, backups, logs and AI inference endpoints in approved regions.",
      mechanism="continuous-automated", freshness="P1D", format="Configuration scan report")
C.evr(6, title="AI provider subprocessor entries and engineering data exclusion checks", description="Register entries for AI providers and checks that engineering environments contain no customer data.",
      mechanism="periodic-automated", freshness="P30D", format="Register and scan report")

# ---------------- Questions ----------------
C.q(1, "Subprocessor list", "Do you publish a current list of subprocessors that process customer data, including each one's function, data categories and processing location?",
    "Customers must know who handles their data.",
    "Unknown parties process customer data.",
    ["SRC-GDPR|Art. 28|d", "SRC-ECH-UNB-BASELINE|UNB-XIN-SAS-011", "SRC-ISO-27018||r", "SRC-CSA-CAIQ-V4||r"],
    "contractual-common", "high",
    ["Please provide your list of sub-processors.", "Which third parties will have access to our data?"],
    disclosure="public")
C.q(1, "Tenant-specific list", "Is your subprocessor list specific to the services and configuration we use, or a generic list for all customers?",
    "Generic lists over- or under-state the parties handling a given customer's data.",
    "Customer assessment based on an inaccurate list.",
    ["SRC-ECH-UNB-BASELINE|UNB-XIN-SAS-011"],
    "customer-preference", "low")
C.q(1, "List accuracy", "How do you ensure the published subprocessor list matches where our data actually flows?",
    "Lists maintained by hand drift from reality.",
    "Data sent to unlisted parties.",
    ["SRC-GDPR|Art. 28|r", "SRC-ECH-UNB-SOC2-DIRECTIVE|SOC2-013"],
    "customer-preference", "medium")
C.q(1, "Scope of listing", "How do you decide which vendors are subprocessors, as opposed to vendors with no access to our data?",
    "Misclassification hides data access.",
    "Vendor with data access omitted from the list.",
    ["SRC-EDPB-GL-07-2020||r", "SRC-GDPR|Art. 28|r"],
    "industry-convention", "low")

C.q(2, "Change notice", "How much advance notice do you give before adding or replacing a subprocessor that will process our data?",
    "Customers need time to assess changes.",
    "New subprocessor used before the customer can react.",
    ["SRC-GDPR|Art. 28(2)|d", "SRC-EU-SCC-2021|Clause 9|d", "SRC-ECH-UNB-BASELINE|UNB-XIN-SAS-011"],
    "contractual-common", "high", disclosure="public")
C.q(2, "Objection right", "Can we object to a new subprocessor, and what happens if we do?",
    "An objection right without a practical outcome is not control.",
    "Customer forced to accept an unacceptable subprocessor or terminate.",
    ["SRC-GDPR|Art. 28(2)|d", "SRC-EU-SCC-2021|Clause 9|r"],
    "contractual-common", "medium", jurisdictions=["EU", "UK", "global"])
C.q(2, "Notice mechanism", "How are subprocessor change notices delivered, and can we choose who receives them?",
    "Notices sent to the wrong person are missed.",
    "Customer unaware of a change despite notice being sent.",
    ["SRC-ECH-UNB-BASELINE|UNB-XIN-SAS-011"],
    "customer-preference", "low")
C.q(2, "Emergency replacement", "If you must replace a subprocessor urgently, how quickly do you notify us and what information do you provide?",
    "Emergencies should not become a loophole for unannounced changes.",
    "Unreviewed emergency subprocessor becomes permanent.",
    ["SRC-ECH-UNB-BASELINE|UNB-XIN-SAS-011"],
    "contractual-common", "medium")
C.q(2, "Scope changes", "Do you notify us when an existing subprocessor's processing location, data categories or function changes?",
    "Changes in an existing relationship can matter as much as new ones.",
    "Data moved to a new country under an existing subprocessor without notice.",
    ["SRC-GDPR|Art. 28|r", "SRC-EU-SCC-2021|Clause 9|r"],
    "customer-preference", "medium")

C.q(3, "Flow-down", "Do you impose data protection obligations on subprocessors at least as protective as those in our agreement with you?",
    "Protections must follow the data.",
    "Weaker obligations at the subprocessor level.",
    ["SRC-GDPR|Art. 28(4)|d", "SRC-ISO-27001-2022|A.5.20|r", "SRC-CSA-CCM-V4|STA|r"],
    "legal-regulatory", "high", jurisdictions=["EU", "UK", "global"], authority="EU and UK data protection authorities",
    scope="Legally required where GDPR or UK GDPR applies to the processing; contractual elsewhere.")
C.q(3, "Liability", "Do you remain fully responsible to us for the performance and failures of your subprocessors?",
    "Customer should not have to pursue subprocessors directly.",
    "Accountability gap after a subprocessor failure.",
    ["SRC-GDPR|Art. 28(4)|d"],
    "contractual-common", "medium")
C.q(3, "Subprocessor oversight", "How do you assess and monitor the security of your subprocessors?",
    "Contract terms need verification.",
    "Subprocessor control failures undetected.",
    ["SRC-ECH-UNB-SOC2-DIRECTIVE|SOC2-013", "SRC-AICPA-TSC|CC9.2|r", "SRC-INTERAGENCY-TPRM-2023|Ongoing Monitoring|r"],
    "industry-convention", "medium")
C.q(3, "Secondary use and AI training", "Do your subprocessor agreements prohibit subprocessors from using our data for their own purposes, including training AI models?",
    "Secondary use is a common hidden risk, especially with AI services.",
    "Customer data used to train third-party models.",
    ["SRC-GDPR|Art. 28|r", "SRC-ECH-UNB-SOC2-DIRECTIVE|SOC2-028"],
    "contractual-common", "high")
C.q(3, "Sub-subprocessors", "Can your subprocessors engage their own subprocessors for our data, and how do you control that?",
    "Each layer adds parties the customer never approved.",
    "Uncontrolled chain of processors.",
    ["SRC-GDPR|Art. 28(4)|d", "SRC-EU-SCC-2021|Clause 9|r"],
    "contractual-common", "low")

C.q(4, "Data location", "In which countries is our data stored and processed, including backups, logs, AI inference and support access?",
    "Location determines applicable law and regulator expectations.",
    "Data processed in a jurisdiction the customer cannot accept.",
    ["SRC-NIST-SP800-53-R5|SA-9(5)|r", "SRC-CSA-CAIQ-V4||r", "SRC-GDPR|Art. 44|r"],
    "customer-preference", "high",
    ["Where are your data centers located?", "Will our data ever leave the United States?"])
C.q(4, "Transfer mechanism", "For personal data from the EU or UK, what transfer mechanism do you and your subprocessors rely on?",
    "Transfers need a lawful basis.",
    "Unlawful international transfers.",
    ["SRC-GDPR|Art. 46|d", "SRC-EU-SCC-2021||d", "SRC-EU-US-DPF||d", "SRC-UK-GDPR||r"],
    "legal-regulatory", "medium", jurisdictions=["EU", "UK"], authority="EU and UK data protection authorities",
    scope="Applies only where EU or UK personal data is processed; no such exposure is established for Echelon.")
C.q(4, "Residency commitment", "Can you commit contractually that our data, including AI processing, stays in the United States?",
    "Some US financial institutions and public bodies require domestic processing.",
    "Offshore processing in breach of customer policy.",
    ["SRC-FEDRAMP||r", "SRC-STATERAMP||r"],
    "customer-preference", "medium", jurisdictions=["US-federal", "US-states"], industries=["banking", "public-sector", "financial-services"])

C.q(5, "AI providers as subprocessors", "Are the AI model providers that receive our data listed as subprocessors?",
    "AI providers are often omitted from subprocessor lists.",
    "Undisclosed AI processing of customer data.",
    ["SRC-ECH-UNB-BASELINE|UNB-XIN-SAS-011", "SRC-GDPR|Art. 28|r", "SRC-NIST-AI-RMF-1.0|GOVERN 6.1|r"],
    "contractual-common", "high")
C.q(5, "AI contracting entity", "When a model is accessed through a cloud platform rather than directly from its developer, which company actually processes our data and is listed as the subprocessor?",
    "The model developer and the hosting provider may have different terms and locations.",
    "Wrong entity assessed; actual processor's terms unknown.",
    ["SRC-EDPB-GL-07-2020||r", "SRC-NIST-AI-600-1||r"],
    "customer-preference", "low")
C.q(5, "AI provider changes", "Will switching to a new AI model provider, or to a new hosting route for a model, trigger your subprocessor notice process?",
    "AI provider changes are frequent and easy to treat as technical rather than contractual.",
    "Customer data sent to a new AI provider without notice.",
    ["SRC-ECH-UNB-BASELINE|UNB-XIN-SAS-011"],
    "customer-preference", "medium")
C.q(5, "Engineering AI tools", "Do the providers of your AI coding agents or developer AI tools ever receive our data, for example during troubleshooting? If so, are they listed?",
    "Engineering tools can become unlisted processors.",
    "Customer data disclosed to AI coding tool providers.",
    ["SRC-ECH-UNB-BASELINE|CNV-ARC-002", "SRC-GDPR|Art. 28|r"],
    "customer-preference", "high")
