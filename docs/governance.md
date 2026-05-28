# Governance — Schema Extension RFC Process

This document defines how Condicio evolves. All schema changes — new fields,
new sections, new `$defs`, or structural modifications — follow the RFC
(Request for Comments) process described here.

## RFC Lifecycle

```
Proposal → Discussion → Refinement → Review → Decision → Accepted/Rejected
```

### 1. Proposal

Anyone may propose a schema extension by opening a GitHub issue using the
**RFC template**. The proposal should include:

- **Motivation** — what problem does this solve?
- **Use case** — what contracts or workflows need this?
- **Schema diff** — the proposed changes to `condicio.schema.json`
- **Example** — a complete example document showing the new fields in use
- **Backward compatibility** — does this break existing documents?

### 2. Discussion (minimum 7 days)

The proposal is discussed openly on the issue thread. Participants should
focus on:

- Does the proposal fit Condicio's scope (contract intelligence extraction)?
- Is the field broadly useful, or specific to one domain?
- Is the naming consistent with existing conventions?
- Could the same goal be achieved with existing fields?

### 3. Refinement

Based on feedback, the author may revise the proposal. Significant changes
should be summarized in a comment on the issue.

### 4. Review

A designated maintainer (or the Docfide team for v0.x) performs final review:

- Schema validity is checked (`npm test`)
- New examples validate correctly
- Documentation is updated (field reference, usage guide)

### 5. Decision

- **Accept** — schema is updated, examples are added, changelog is recorded
- **Reject** — issue is closed with explanation
- **Defer** — marked for future major version

## Versioning

Condicio follows **Semantic Versioning** for the schema specification:

- **Major** — breaking changes (removing fields, changing required fields)
- **Minor** — backward-compatible additions (new optional fields, new `$defs`)
- **Patch** — fixes, clarifications, documentation

Pre-v1.0, minor changes may include breaking changes with notice.

## Maintainers

During v0.x, the Docfide team acts as the sole maintainer, responsible for:

- Merging RFCs that have reached consensus
- Ensuring backward compatibility where practical
- Maintaining the validation pipeline and release process

Post-v1.0, maintainer roles will be formally defined with community
representation.

## Scope

Condicio is scoped to **contract intelligence extraction data** — what tools
like CLM platforms, AI extraction engines, and obligation trackers *output*
about a contract. The following are explicitly **out of scope**:

- Contract drafting or template languages (Accord Project covers this)
- Smart contract execution logic (Solidity, Rust, etc.)
- Document storage or management APIs
- Contract negotiation workflows

Extensions that push beyond this scope should be proposed as companion
specifications rather than modifications to the core schema.

## License

All RFCs and contributed schema changes are licensed under Apache 2.0.
