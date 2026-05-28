from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import jsonschema
import referencing
import yaml


SCHEMA_URL = "https://raw.githubusercontent.com/docfide/condicio/main/schema/condicio.schema.json"

_HERE = Path(__file__).resolve().parent
_PACKAGE_SCHEMA = _HERE.parent / "schema" / "condicio.schema.json"
_FALLBACK_PATHS = [
    _PACKAGE_SCHEMA,
    Path("schema/condicio.schema.json"),
    Path("../schema/condicio.schema.json"),
]


class ValidationError:
    path: str
    message: str
    schema_path: Optional[str] = None

    def __init__(self, path: str, message: str, schema_path: Optional[str] = None):
        self.path = path
        self.message = message
        self.schema_path = schema_path

    def __repr__(self) -> str:
        return f"{self.path}: {self.message}"


class CondicioValidator:
    def __init__(self, schema_path: Optional[str] = None):
        self._schema = self._load_schema(schema_path)
        self._validator = jsonschema.Draft202012Validator(
            self._schema,
            registry=self._build_registry(self._schema),
            format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER,
        )

    @staticmethod
    def _load_schema(schema_path: Optional[str] = None) -> dict:
        if schema_path:
            source = schema_path
        else:
            source = SCHEMA_URL

        if source.startswith(("http://", "https://")):
            import urllib.request
            try:
                with urllib.request.urlopen(source) as resp:
                    return json.loads(resp.read().decode())
            except Exception:
                pass

        p = Path(source)
        if p.exists():
            with open(p) as f:
                return json.load(f)

        for fp in _FALLBACK_PATHS:
            if fp.exists():
                with open(fp) as f:
                    return json.load(f)

        raise FileNotFoundError(
            f"Cannot find schema at {source}. "
            f"Tried URL, path, and fallbacks: {_FALLBACK_PATHS}"
        )

    @staticmethod
    def _build_registry(schema: dict):
        return referencing.Registry().with_resource(
            "https://raw.githubusercontent.com/docfide/condicio/main/schema/condicio.schema.json",
            referencing.Resource.from_contents(schema),
        )

    def validate(self, data: dict) -> list[ValidationError]:
        errors = []
        for err in self._validator.iter_errors(data):
            errors.append(ValidationError(
                path="/" + "/".join(str(p) for p in err.absolute_path) if err.absolute_path else "(root)",
                message=err.message,
            ))
        return errors

    def is_valid(self, data: dict) -> bool:
        return self._validator.is_valid(data)


_default_validator: Optional[CondicioValidator] = None


def _get_validator() -> CondicioValidator:
    global _default_validator
    if _default_validator is None:
        _default_validator = CondicioValidator()
    return _default_validator


def load_document(path: str) -> dict:
    p = Path(path)
    raw = p.read_text(encoding="utf-8")
    if p.suffix in (".yaml", ".yml"):
        return yaml.safe_load(raw)
    return json.loads(raw)


def validate_document(data: dict, schema_path: Optional[str] = None) -> list[ValidationError]:
    if schema_path:
        return CondicioValidator(schema_path=schema_path).validate(data)
    return _get_validator().validate(data)


def is_valid(data: dict, schema_path: Optional[str] = None) -> bool:
    if schema_path:
        return CondicioValidator(schema_path=schema_path).is_valid(data)
    return _get_validator().is_valid(data)
