# Contributing to Condicio

Thanks for your interest in contributing. Condicio is an open standard, and
community participation is what makes it useful.

## Ways to contribute

- **Add examples** — new contract types in JSON + YAML that validate against the schema
- **Propose extensions** — submit an RFC for new schema sections or fields
- **Report issues** — schemas that don't validate, unclear field descriptions, missing use cases
- **Improve docs** — fix typos, clarify explanations, add tutorials
- **Build integrations** — connectors for CLM platforms, extraction engines, obligation trackers

## Development setup

```bash
git clone https://github.com/docfide/condicio
cd condicio
npm install
npm test
```

All examples must validate against the schema before a PR is merged.

## Contribution guidelines

### Schema changes

- Preserve backward compatibility where possible
- Add new optional fields before changing required fields
- Every field must include a `description`
- New `$defs` should follow the existing composable pattern
- Update or add examples for any schema change

### Examples

- Each contract type should have both `.json` and `.yaml` versions
- Use realistic but fictional party names and data
- Include a reasonable set of obligations, risks, and clauses
- Run `npm test` before submitting

### Pull requests

1. Open an issue first to discuss significant changes
2. Fork the repo and create a feature branch
3. Make your changes and run `npm test`
4. Submit the PR with a clear description of what changed and why

## Code of Conduct

All contributors must adhere to the [Code of Conduct](CODE_OF_CONDUCT.md).
