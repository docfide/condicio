# Usage Guide

How to produce and consume Condicio contract data.

---

## Producing Condicio data

If you're building a contract extraction tool, CLM integration, or AI pipeline,
Condicio defines what your output should look like.

### Minimum viable document

Only the `condicio` identifier, `specVersion`, and `contract.title` are required:

```json
{
  "condicio": "https://raw.githubusercontent.com/docfide/condicio/main/schema/condicio.schema.json",
  "specVersion": "0.1.0",
  "id": "urn:uuid:a1b2c3d4-...",
  "contract": {
    "title": "My Contract"
  }
}
```

### Adding parties

```json
{
  "parties": [
    {
      "id": "party-abc",
      "name": "ABC Corp",
      "role": "client",
      "type": "corporation"
    }
  ]
}
```

### Adding obligations

Each obligation links back to its source clause:

```json
{
  "obligations": [
    {
      "description": "Deliver source code by March 1st.",
      "obligor": "DevStudio LLC",
      "deadlineType": "fixed date",
      "fixedDate": "2026-03-01",
      "status": "pending",
      "clauseRef": "3"
    }
  ]
}
```

Deadline types:
- **`fixed date`** — use with `fixedDate`
- **`days from event`** — use with `daysFromEvent`
- **`recurring`** — ongoing periodic obligation
- **`conditional`** — triggered by a future event
- **`ongoing`** — continuous, no fixed endpoint

### Adding financials

```json
{
  "financials": {
    "currency": "USD",
    "totalContractValue": 150000,
    "terms": [
      { "label": "license fee", "amount": 150000, "period": "one-time" }
    ],
    "paymentSchedule": [
      { "amount": 75000, "dueDate": "2026-01-01", "status": "paid" },
      { "amount": 75000, "dueDate": "2026-06-01", "status": "pending" }
    ]
  }
}
```

### Adding risks

```json
{
  "risks": [
    {
      "description": "No limitation of liability clause.",
      "severity": "high",
      "category": "legal",
      "impact": "Uncapped liability exposure.",
      "affectedParty": "ABC Corp",
      "confidence": 0.92
    }
  ]
}
```

Severity levels: `low`, `medium`, `high`, `critical`

### Confidence scores

Any extracted field can carry a `confidence` between `0.0` and `1.0`.
This is critical for AI-generated output — consumers can filter by
confidence threshold.

---

## Consuming Condicio data

### Validate with AJV (Node.js)

```js
import Ajv from 'ajv/dist/2020.js'
import addFormats from 'ajv-formats'
import condicio from 'condicio-schema'

const ajv = new Ajv()
addFormats(ajv)
const validate = ajv.compile(condicio)

if (validate(doc)) {
  console.log('Valid')
} else {
  console.error(validate.errors)
}
```

### Validate with the CLI

```bash
npm install -g ajv-cli
ajv validate -s node_modules/condicio-schema/schema/condicio.schema.json -d contract.json
```

### Query obligations by party

```js
const myObligations = doc.obligations.filter(o => o.obligor === 'ABC Corp')
const overdue = doc.obligations.filter(o => o.status === 'overdue')
```

### Filter by risk severity

```js
const critical = doc.risks.filter(r => r.severity === 'critical')
```

---

## YAML

Condicio supports both JSON and YAML. Valid YAML documents are structurally
identical to their JSON equivalents:

```yaml
condicio: https://raw.githubusercontent.com/docfide/condicio/main/schema/condicio.schema.json
specVersion: "0.1.0"
contract:
  title: My Contract
  type: Service Agreement
parties:
  - name: ABC Corp
    role: client
```

All examples are available in both formats under `schema/examples/`.
