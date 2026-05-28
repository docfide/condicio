import json
from pathlib import Path

from condicio.validator import CondicioValidator, validate_document, is_valid


_HERE = Path(__file__).resolve().parent
_SCHEMA = _HERE.parent.parent / "schema" / "condicio.schema.json"
_EXAMPLES = _HERE.parent.parent / "schema" / "examples"


def test_schema_exists():
    assert _SCHEMA.exists(), f"Schema not found at {_SCHEMA}"


def test_validator_initializes():
    v = CondicioValidator(schema_path=str(_SCHEMA))
    assert v._schema is not None


def test_validate_all_examples():
    v = CondicioValidator(schema_path=str(_SCHEMA))
    for fpath in sorted(_EXAMPLES.iterdir()):
        if fpath.suffix == ".json":
            data = json.loads(fpath.read_text())
            errors = v.validate(data)
            assert not errors, f"{fpath.name}: {errors}"


def test_is_valid_returns_true():
    v = CondicioValidator(schema_path=str(_SCHEMA))
    data = json.loads((_EXAMPLES / "nda.json").read_text())
    assert v.is_valid(data) is True


def test_is_valid_returns_false():
    v = CondicioValidator(schema_path=str(_SCHEMA))
    bad = {"condicio": "bad"}
    assert v.is_valid(bad) is False


def test_validate_detects_missing_required():
    v = CondicioValidator(schema_path=str(_SCHEMA))
    errors = v.validate({})
    paths = {e.path for e in errors}
    assert any("condicio" in p for p in paths) or len(errors) > 0


def test_validate_convenience():
    data = json.loads((_EXAMPLES / "nda.json").read_text())
    errors = validate_document(data, schema_path=str(_SCHEMA))
    assert not errors


def test_validate_all_yaml_examples():
    try:
        import yaml
    except ImportError:
        return  # skip if pyyaml not installed
    v = CondicioValidator(schema_path=str(_SCHEMA))
    for fpath in sorted(_EXAMPLES.iterdir()):
        if fpath.suffix in (".yaml", ".yml"):
            data = yaml.safe_load(fpath.read_text())
            errors = v.validate(data)
            assert not errors, f"{fpath.name}: {errors}"
