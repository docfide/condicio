# Condicio Schema

**An open schema for structured contract intelligence data.**

Condicio (Latin: *agreement, condition, stipulation*) defines a standard way to represent extracted contract data: parties, clauses, obligations, risk flags, key dates, financial terms, and more.

## Why

Every contract intelligence tool — CLM platforms, AI extraction engines, obligation trackers — invents its own output format. There is no universally agreed-upon schema for what structured contract data should look like. Condicio fixes that.

A common schema means:
- **Interoperability** — tools can exchange contract data without custom transforms
- **Portability** — move between CLM platforms without losing structured data
- **Ecosystem** — validation, analysis, and reporting tools built once, work everywhere

## Status

**Pre-release** (v0.1.0). Under active development. Contributions welcome.

## Schema

The canonical schema is at [`schema/condicio.schema.json`](schema/condicio.schema.json) (JSON Schema 2020-12).

### Core sections

| Section | Description |
|---------|-------------|
| `contract` | Document-level metadata: title, type, jurisdiction, status |
| `parties` | Named parties with roles, identifiers, contact info |
| `dates` | Key dates: execution, effective, expiry, renewal, notice periods |
| `clauses` | Extracted clauses/sections with optional classification |
| `obligations` | Action items, deadlines, responsible parties |
| `financials` | Monetary terms: amounts, payment schedules, currency, interest |
| `risks` | Risk flags, severity, categories, descriptions |
| `definitions` | Defined terms and their definitions |
| `metadata` | Extraction source, confidence scores, timestamps, tool info |

## Usage

```bash
npm install condicio-schema
```

Then validate your contract data against the schema using any JSON Schema validator:

```js
import Ajv from 'ajv'
import condicio from 'condicio-schema'

const ajv = new Ajv()
const validate = ajv.compile(condicio)
const valid = validate(myContractData)
```

## Examples

See [`schema/examples/`](schema/examples/) for sample contract data files.

## License

Apache 2.0
