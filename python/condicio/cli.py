"""Command-line interface for Condicio."""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from condicio.validator import (
    CondicioValidator,
    load_document,
    validate_document,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="condicio",
        description="Python tools for the Condicio contract intelligence schema.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # validate
    val = sub.add_parser("validate", help="Validate a Condicio document")
    val.add_argument("file", help="Path to Condicio JSON or YAML file")
    val.add_argument("--schema", "-s", help="Path or URL to schema file")
    val.add_argument("--verbose", "-v", action="store_true", help="Show detailed errors")

    # inspect
    insp = sub.add_parser("inspect", help="Inspect a Condicio document (summary)")
    insp.add_argument("file", help="Path to Condicio JSON or YAML file")

    return parser


def cmd_validate(args: argparse.Namespace) -> int:
    try:
        data = load_document(args.file)
    except FileNotFoundError:
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON in {args.file}: {e}", file=sys.stderr)
        return 1

    try:
        errors = validate_document(data, schema_path=args.schema)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if not errors:
        print(f"{args.file}: Valid Condicio document")
        return 0

    print(f"{args.file}: {len(errors)} validation error(s)", file=sys.stderr)
    for err in errors:
        if args.verbose:
            print(f"  [{err.path}] {err.message}", file=sys.stderr)
        else:
            print(f"  {err.path}: {err.message}", file=sys.stderr)
    return 1


def cmd_inspect(args: argparse.Namespace) -> int:
    try:
        data = load_document(args.file)
    except FileNotFoundError:
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr)
        return 1

    contract = data.get("contract", {})
    parties = data.get("parties", [])
    obligations = data.get("obligations", [])
    clauses = data.get("clauses", [])
    risks = data.get("risks", [])
    financials = data.get("financials", {})

    print(f"Contract:  {contract.get('title', 'Untitled')}")
    print(f"Type:      {contract.get('type', 'N/A')}")
    print(f"Status:    {contract.get('status', 'N/A')}")
    print(f"Parties:   {len(parties)}")
    for p in parties:
        print(f"            - {p.get('name', '?')} ({p.get('role', '?')})")
    print(f"Clauses:   {len(clauses)}")
    print(f"Obligations: {len(obligations)}")
    print(f"Risks:     {len(risks)}")
    if financials.get("totalContractValue"):
        print(f"TCV:       {financials.get('currency', '')} {financials['totalContractValue']:,.2f}")

    return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        return cmd_validate(args)
    elif args.command == "inspect":
        return cmd_inspect(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
