"""Guardrails for the existing hello package surface (src layout, py.typed marker)."""

import importlib.resources

import hello

# Names exported by src/hello/__init__.py as of SPEC-0001, recorded before the change.
EXPORTED_NAMES = ("hello",)


def check_existing_package_surface() -> None:
    for name in EXPORTED_NAMES:
        assert hasattr(hello, name), f"hello no longer exports {name!r}"


def test_existing_package_surface_unchanged() -> None:
    check_existing_package_surface()


def test_py_typed_marker_is_shipped() -> None:
    assert (importlib.resources.files("hello") / "py.typed").is_file()
