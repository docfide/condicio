# Condicio Python

Python tools for the [Condicio](https://github.com/docfide/condicio) contract intelligence schema.

- **Validate** Condicio documents against the JSON Schema
- **Work with typed models** — dataclasses for every schema type
- **Serialize/deserialize** to/from JSON and YAML
- **CLI** for validation and inspection

## Install

```bash
pip install condicio
```

## Usage

### CLI

```bash
# Validate a Condicio document
condicio validate document.json

# Validate with verbose output
condicio validate document.json --verbose

# Load from YAML
condicio validate document.yaml
```

### Python

```python
from condicio.validator import validate_document
from condicio.models import CondicioDocument, Party, Obligation

# Validate a raw dict
with open("document.json") as f:
    import json
    data = json.load(f)

errors = validate_document(data)
if errors:
    for err in errors:
        print(f"  {err.path}: {err.message}")
else:
    print("Valid Condicio document")

# Deserialize to typed models
from condicio.models import document_from_dict

doc = document_from_dict(data)
print(f"Contract: {doc.contract.title}")
for party in doc.parties:
    print(f"  Party: {party.name} ({party.role})")
```

## Schema URL

By default, the validator fetches the latest schema from:

```
https://raw.githubusercontent.com/docfide/condicio/main/schema/condicio.schema.json
```

You can pass a custom schema path or URL:

```python
from condicio.validator import CondicioValidator

v = CondicioValidator(schema_path="path/to/condicio.schema.json")
errors = v.validate(data)
```

## License

Apache 2.0
