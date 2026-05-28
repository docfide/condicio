# Condicio Schema

**Open standard for contract intelligence data — parties, clauses, obligations, risks, dates, and financial terms.**

[![npm](https://img.shields.io/npm/v/condicio-schema)](https://www.npmjs.com/package/condicio-schema)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)
[![JSON Schema](https://img.shields.io/badge/JSON%20Schema-2020--12-green)](schema/condicio.schema.json)

---

## What is Condicio?

Condicio (Latin: *agreement, condition, stipulation*) defines a **universal schema** for representing structured contract intelligence data. Every contract extraction tool — CLM platforms, AI engines, obligation trackers — invents its own output format. Condicio is the missing standard.

```json
{
  "condicio": "https://condicio.dev/schema/condicio.schema.json",
  "contract": {
    "title": "Mutual Non-Disclosure Agreement",
    "type": "NDA",
    "status": "executed",
    "jurisdiction": "Delaware"
  },
  "parties": [
    { "name": "Acme Corporation", "role": "disclosing party" },
    { "name": "Beta Inc", "role": "receiving party" }
  ],
  "obligations": [
    {
      "description": "Maintain Confidential Information in strict confidence.",
      "obligor": "Beta Inc",
      "deadlineType": "ongoing"
    }
  ]
}
```

A common schema means **interoperability, portability, and an ecosystem** of tools that work together out of the box.

---

## Table of Contents

- [Why Condicio](#why-condicio)
- [Schema Overview](#schema-overview)
- [Quick Start](#quick-start)
- [Examples](#examples)
- [Use Cases](#use-cases)
- [Comparison with Related Work](#comparison-with-related-work)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Why Condicio

Every contract intelligence tool produces structured data — but they all use different schemas.

| Problem | Consequence |
|---------|-------------|
| Proprietary output formats | Vendor lock-in, costly migrations |
| No standard for obligations | Each tool tracks them differently |
| Inconsistent date representations | Parsing errors, missed deadlines |
| Non-portable risk flags | Risk intelligence trapped in one platform |

Condicio solves this by providing a **vendor-neutral, open schema** that any tool can produce and consume.

### Principles

- **Open by default** — Apache 2.0 license, community-governed
- **Extraction-first** — designed for what contract *intelligence* tools produce, not for drafting
- **Composable** — use only the sections you need (just parties? just obligations?)
- **Language-agnostic** — JSON Schema core with first-class YAML support
- **Confidence-aware** — every extracted field can carry a confidence score from the extraction engine

---

## Schema Overview

The schema is defined in [`schema/condicio.schema.json`](schema/condicio.schema.json) using **JSON Schema 2020-12**.

| Section | Type | Description |
|---------|------|-------------|
| `contract` | `object` | Document-level metadata — title, type, jurisdiction, governing law, status, IDs |
| `parties` | `[party]` | Named parties with roles, identifiers, type (corporation, individual, llc), contact info |
| `dates` | `[date]` | Key dates — execution, effective, expiry, renewal windows, notice periods |
| `clauses` | `[clause]` | Extracted clauses with classification, full text, and confidence |
| `obligations` | `[obligation]` | Actionable items — deadlines (fixed, recurring, conditional, ongoing), responsible parties, clause references |
| `financials` | `object` | Monetary terms — total contract value, currency, payment schedule, line items, late payment penalties |
| `risks` | `[risk]` | Risk flags — severity (low/medium/high/critical), category, impact, affected party |
| `definitions` | `[definition]` | Defined terms and their definitions as they appear in the contract |
| `metadata` | `object` | Extraction provenance — engine name/version, confidence score, source document info, timestamps |

### Design approach

- Uses `$defs` for composable reusable types (`party`, `clause`, `obligation`, `financialTerm`, `payment`, `risk`, `date`, `contactInfo`, `address`)
- `additionalProperties: false` at root enforces strict compliance
- A top-level `condicio` const URI identifies the schema version
- Every extraction field includes optional `confidence` (0.0–1.0) for AI-engine uncertainty

---

## Quick Start

```bash
# Install via npm
npm install condicio-schema

# Validate your contract data
npx ajv validate -s node_modules/condicio-schema/schema/condicio.schema.json -d your-contract.json
```

Or validate programmatically:

```js
import Ajv from 'ajv/dist/2020.js'
import addFormats from 'ajv-formats'
import condicio from 'condicio-schema'

const ajv = new Ajv()
addFormats(ajv)
const validate = ajv.compile(condicio)

if (validate(myContractData)) {
  console.log('Valid Condicio document')
} else {
  console.error(validate.errors)
}
```

### Local development

```bash
git clone https://github.com/docfide/condicio
cd condicio
npm install
npm test          # Validates all examples against the schema
```

---

## Examples

Ready-to-use examples in both JSON and YAML format:

| Example | Highlights |
|---------|------------|
| [NDA](schema/examples/nda.json) | Mutual confidentiality, exclusions, survival period, auto-renewal |
| [Service Agreement](schema/examples/service-agreement.json) | Milestone-based payments ($150K), IP assignment, liability cap |
| [Employment](schema/examples/employment-agreement.json) | Salary + bonus + equity, non-compete, severance, at-will |
| [License Agreement](schema/examples/license-agreement.json) | Perpetual license, maintenance SLA, audit rights, usage restrictions |

YAML equivalents are available alongside each JSON example.

---

## Use Cases

| Use Case | How Condicio Helps |
|----------|-------------------|
| **AI contract extraction** | Standard output format for any extraction engine |
| **CLM data portability** | Export contracts from one CLM, import into another |
| **Obligation tracking** | Structured obligations with deadlines, owners, status |
| **Risk assessment** | Portable risk flags with severity, category, impact |
| **Contract analytics** | Aggregate across portfolios with consistent field definitions |
| **Regulatory reporting** | Standard date, party, and clause representations |
| **M&A due diligence** | Uniform contract data from disparate sources |
| **ISDA/derivatives processing** | Extensible for financial contract specifics |

---

## Comparison with Related Work

| Standard | Focus | Status | Relationship to Condicio |
|----------|-------|--------|------------------------|
| **Accord Project** | Smart legal contracts (Cicero, Ergo) | Active | Complementary — Condicio covers extraction output, Accord covers executable contracts |
| **SALI** | Contract standards alliance (tags, classifications) | Active | Compatible — Condicio can reference SALI classification IDs |
| **LEDES** | Legal billing/invoicing | Active | Different domain — billing data, not contract intelligence |
| **LegalXML** | Court filings, legislative documents | Maintained | Different domain — e-filing, not commercial contracts |
| **OCDS (Open Contracting)** | Public procurement | Active | Different domain — government procurement transparency |
| **ODCS (Open Data Charter)** | Contract publication | Active | Different domain — contract publication, not extraction |

No existing standard addresses the **output of contract intelligence extraction** — that is the gap Condicio fills.

---

## Roadmap

- **v0.2.0** — Add SaaS/subscription contract fields, multi-currency financials
- **v0.3.0** — Add clause classification taxonomy reference, compliance mapping
- **v0.4.0** — Add attachments/schedules support, document redline tracking
- **v0.5.0** — Governance model, formal RFC process for extensions
- **v1.0.0** — Stable release, open standards body submission

---

## Contributing

Contributions are welcome and encouraged.

### How to contribute

1. **Review existing examples** — understand the patterns before proposing changes
2. **Open an issue** — discuss your use case or proposed extension
3. **Submit a PR** — with schema changes, examples, and validation passing (`npm test`)
4. **Add examples** — new contract types in both JSON and YAML formats

### Guidelines

- Preserve backward compatibility where possible
- Add new optional fields before changing required fields
- Every field should include a `description`
- New `$defs` should follow the existing composable pattern
- Every schema change should include updated examples

---

## License

Apache 2.0. See [LICENSE](LICENSE).

---

Built by [Docfide](https://docfide.com).  
Condicio is a trademark of Docfide Inc.
