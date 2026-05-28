# Field Reference

Auto-generated from [`schema/condicio.schema.json`](../schema/condicio.schema.json).

## Root-level fields

- **`condicio`** **required** — Immutable identifier for the Condicio schema version. *any*

- **`specVersion`** **required** — Version of the Condicio specification this document conforms to. *string* `0.1.0`

- **`id`** — Unique identifier for this contract document (UUID, URI, or application-specific ID). *string*

- **`contract`** **required** — Top-level metadata about the contract document. *object*
  - **`title`** **required** — Full title or name of the contract. *string*
  - **`type`** — Classification of the contract type. *string* (e.g. `"NDA"`, `"MSA"`, `"SOW"`, `"License Agreement"`, `"Service Agreement"`, `"Employment Agreement"`, `"Partnership Agreement"`, `"Lease"`, `"Purchase Agreement"`, `"Insurance Policy"`)
  - **`description`** — Short summary or purpose of the contract. *string*
  - **`language`** — Primary language of the contract (BCP 47 code). *string* (e.g. `"en"`, `"de"`, `"fr"`, `"es"`, `"ja"`)
  - **`jurisdiction`** — Governing jurisdiction rendered as country or region identifier. *string* (e.g. `"New York"`, `"England and Wales"`, `"Delaware"`, `"Germany"`)
  - **`governingLaw`** — Explicit governing law clause text or reference. *string*
  - **`status`** — Lifecycle status of the contract. *string* `draft`, `proposed`, `executed`, `active`, `amended`, `terminated`, `expired`, `superseded`
  - **`contractId`** — External contract identifier used by the source system (e.g., CLM ID, document number). *string*
  - **`executionDate`** — Date the contract was signed by all parties. *date* (see [$#/$defs/date#](date))
  - **`effectiveDate`** — Date the contract becomes effective. *date* (see [$#/$defs/date#](date))
  - **`expiryDate`** — Date the contract expires. *date* (see [$#/$defs/date#](date))
  - **`renewalTerms`** — Description of renewal terms or conditions. *string*
  - **`amendmentSummary`** — Summary of amendments if this document supersedes a prior version. *string*

- **`parties`** **required** — Parties to the contract with roles and identifiers. *array*
  - Items: [$#{$defs/party}](#party)

- **`dates`** — Key dates extracted from or associated with the contract. *array*
  - Items: [$#{$defs/contractDate}](#contractDate)

- **`clauses`** — Extracted clauses, sections, or provisions. *array*
  - Items: [$#{$defs/clause}](#clause)

- **`obligations`** — Obligations, covenants, duties, or action items imposed on any party. *array*
  - Items: [$#{$defs/obligation}](#obligation)

- **`financials`** — Monetary terms and financial provisions. *object*
  - **`currency`** — Default currency for all financial terms (ISO 4217). *string* (e.g. `"USD"`, `"EUR"`, `"GBP"`, `"NGN"`)
  - **`terms`** — Individual financial terms extracted from the contract. *array*
    - Items: [$#{$defs/financialTerm}](#financialTerm)
  - **`totalContractValue`** — Total contract value in the default currency. *number*
  - **`paymentTerms`** — Standard payment terms (e.g. Net 30, Net 60). *string*
  - **`latePaymentPenalty`** — Late payment penalty or interest rate. *string*
  - **`paymentSchedule`** — Structured payment schedule if applicable. *array*
    - Items: [$#{$defs/payment}](#payment)

- **`risks`** — Risk flags and assessments identified in the contract. *array*
  - Items: [$#{$defs/risk}](#risk)

- **`definitions`** — Defined terms and their definitions extracted from the contract. *array*
  - **`term`** **required** — The defined term or capitalised phrase. *string*
  - **`definition`** **required** — The definition text. *string*
  - **`clauseRef`** — Reference to the clause where this term is defined. *string*

- **`metadata`** — Extraction and processing metadata. *object*
  - **`extractedAt`** — ISO 8601 timestamp of extraction. *string*
  - **`extractedBy`** — Name or identifier of the extraction tool or agent. *string*
  - **`extractionEngine`** — Tool, engine, or model used for extraction. *object*
    - **`name`** —  *string*
    - **`version`** —  *string*
  - **`confidence`** — Overall extraction confidence score (0.0 to 1.0). *number*
  - **`sourceDocument`** — Reference to the source document. *object*
    - **`filename`** —  *string*
    - **`mediaType`** —  *string*
    - **`size`** —  *integer*
    - **`pages`** —  *integer*
    - **`hash`** —  *object*
      - **`algorithm`** —  *string* (e.g. `"sha256"`, `"md5"`)
      - **`value`** —  *string*
    - **`uri`** —  *string*
  - **`tags`** — Arbitrary tags or labels applied to this contract. *array*
  - **`custom`** — Extensible container for tool-specific or organisation-specific metadata. *object*

---

## Defined types (`$defs`)

### date

A date string in ISO 8601 format (YYYY-MM-DD) or full datetime.

One of the following:

**Option 1:** 


**Option 2:** 



---

### contactInfo

Contact information for a person or organisation.

- **`name`** —  *string*
- **`email`** —  *string*
- **`phone`** —  *string*
- **`address`** —  *address* (see [$#/$defs/address#](address))

---

### address

A postal address.

- **`street`** —  *string*
- **`city`** —  *string*
- **`stateOrProvince`** —  *string*
- **`postalCode`** —  *string*
- **`country`** —  *string*

---

### party

A named party to the contract.

- **`id`** — Unique identifier for this party within the document. *string*
- **`name`** **required** — Full legal name of the party. *string*
- **`alias`** — Short name or abbreviation used throughout the contract. *string*
- **`role`** **required** — Role of the party in the contract. *string* (e.g. `"buyer"`, `"seller"`, `"licensor"`, `"licensee"`, `"employer"`, `"employee"`, `"landlord"`, `"tenant"`, `"insurer"`, `"insured"`, `"service provider"`, `"client"`, `"joint venture partner"`)
- **`type`** — Legal entity type. *string* (e.g. `"corporation"`, `"llc"`, `"individual"`, `"partnership"`, `"government"`, `"non-profit"`)
- **`jurisdiction`** — Jurisdiction of formation or residence. *string* (e.g. `"Delaware"`, `"England and Wales"`, `"Germany"`)
- **`contact`** —  *contactInfo* (see [$#/$defs/contactInfo#](contactInfo))
- **`representative`** — Signatory or representative acting for this party. *contactInfo* (see [$#/$defs/contactInfo#](contactInfo))

---

### contractDate

A named date associated with the contract.

- **`label`** **required** — Semantic label for this date. *string* (e.g. `"execution"`, `"effective"`, `"expiry"`, `"renewal"`, `"notice deadline"`, `"delivery"`, `"payment due"`, `"termination"`)
- **`date`** **required** —  *date* (see [$#/$defs/date#](date))
- **`description`** — Context or description of this date. *string*
- **`clauseRef`** — Reference to the relevant clause. *string*

---

### clause

An extracted clause, section, or provision.

- **`id`** **required** — Clause identifier (e.g., section number or generated ID). *string*
- **`title`** — Clause heading or title. *string*
- **`text`** **required** — Full text of the clause. *string*
- **`summary`** — Short AI-generated or human-written summary. *string*
- **`type`** — Classification of the clause. *string* (e.g. `"confidentiality"`, `"indemnification"`, `"limitation of liability"`, `"termination"`, `"payment"`, `"warranty"`, `"intellectual property"`, `"data protection"`, `"non-compete"`, `"force majeure"`, `"dispute resolution"`, `"governing law"`, `"assignment"`, `"insurance"`, `"audit"`)
- **`scope`** — Scope of the clause (e.g., which parties it binds). *string*
- **`obligationRefs`** — References to obligations derived from this clause. *array*
- **`riskRefs`** — References to risks identified in this clause. *array*
- **`confidence`** — Extraction confidence for this clause (0.0 to 1.0). *number*

---

### obligation

An obligation, duty, covenant, or action item imposed on a party.

- **`id`** — Unique identifier for this obligation. *string*
- **`description`** **required** — Description of the obligation. *string*
- **`obligor`** **required** — Party or role responsible for fulfilling the obligation. *string*
- **`beneficiary`** — Party or role entitled to the obligation. *string*
- **`type`** — Category of obligation. *string* (e.g. `"payment"`, `"delivery"`, `"reporting"`, `"compliance"`, `"confidentiality"`, `"insurance"`, `"maintenance"`, `"notice"`, `"performance"`, `"non-competition"`)
- **`deadline`** — Date or trigger for the obligation. *string*
- **`deadlineType`** — How the deadline is defined. *string* `fixed date`, `days from event`, `recurring`, `conditional`, `ongoing`
- **`status`** — Current status of the obligation. *string* `pending`, `fulfilled`, `overdue`, `waived`, `breached`
- **`clauseRef`** — Reference to the source clause. *string*
- **`confidence`** — Extraction confidence (0.0 to 1.0). *number*

---

### financialTerm

A financial term or monetary provision.

- **`label`** **required** — Label for this financial term. *string* (e.g. `"contract value"`, `"annual fee"`, `"monthly payment"`, `"deposit"`, `"interest rate"`, `"late fee"`, `"minimum commitment"`, `"cap"`, `"threshold"`)
- **`amount`** **required** — Monetary amount as a number. *number*
- **`currency`** — ISO 4217 currency code (overrides top-level currency). *string*
- **`period`** — Period this amount applies to. *string* (e.g. `"one-time"`, `"monthly"`, `"annually"`, `"quarterly"`, `"per unit"`)
- **`description`** — Context or description of this financial term. *string*
- **`clauseRef`** — Reference to the relevant clause. *string*

---

### payment

A scheduled payment.

- **`dueDate`** **required** —  *date* (see [$#/$defs/date#](date))
- **`amount`** **required** —  *number*
- **`description`** —  *string*
- **`condition`** — Condition or trigger for this payment. *string*
- **`status`** —  *string* `pending`, `paid`, `overdue`, `cancelled`
- **`paidDate`** —  *date* (see [$#/$defs/date#](date))

---

### risk

A risk flag or assessment identified in the contract.

- **`id`** — Unique identifier for this risk. *string*
- **`description`** **required** — Description of the risk. *string*
- **`severity`** **required** — Risk severity level. *string* `low`, `medium`, `high`, `critical`
- **`category`** — Risk category. *string* (e.g. `"financial"`, `"legal"`, `"compliance"`, `"operational"`, `"reputational"`, `"data security"`, `"intellectual property"`)
- **`impact`** — Description of potential impact. *string*
- **`mitigation`** — Existing mitigation or recommended action. *string*
- **`affectedParty`** — Party most affected by this risk. *string*
- **`clauseRef`** — Reference to the relevant clause. *string*
- **`confidence`** — Extraction confidence (0.0 to 1.0). *number*

---
