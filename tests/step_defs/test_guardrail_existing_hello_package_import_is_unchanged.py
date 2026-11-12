"""Step definitions for the 'guardrail: existing hello package import is unchanged' scenario."""

from pytest_bdd import given, scenario, then, when

from tests import test_package


@scenario(
    "../features/guardrail-existing-hello-package-import-is-unchanged.feature",
    "guardrail: existing hello package import is unchanged",
)
def test_guardrail_existing_hello_package_import_is_unchanged() -> None:
    """Run the scenario end to end."""


@given(
    "the names exported by src/hello/__init__.py before this change are recorded in the test"
)
def exported_names_recorded() -> None:
    assert test_package.EXPORTED_NAMES == ("hello",)


@when("the test tests/test_package.py::test_existing_package_surface_unchanged runs")
def run_existing_package_surface_check() -> None:
    test_package.test_existing_package_surface_unchanged()


@then(
    "it passes, confirming `import hello` succeeds and every recorded name is still present"
)
def check_passes() -> None:
    """The When step raises on any missing name, so reaching here means it passed."""
