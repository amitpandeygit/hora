"""Architectural rules, enforced rather than documented.

Two boundaries matter enough to guard:

* **Routers do HTTP, services do work.** The one serious bug this project has
  shipped — a thirteen-hour error in the pre-dawn upagraha period — lived in a
  router, where the chapter's 109 tests could not reach it.
* **The ephemeris seam holds.** Nothing above `core/ephemeris/base.py` may
  import `swisseph`, because that seam is what keeps a licence decision from
  becoming a rewrite.
"""
import ast
import pathlib

import pytest

SRC = pathlib.Path(__file__).resolve().parents[2] / "src" / "hora"
ROUTERS = sorted((SRC / "api" / "routers").glob("*.py"))
SERVICES = sorted((SRC / "services").glob("*.py"))

#: A router may be this long before it is doing something other than HTTP.
MAX_ROUTER_LINES = 90


def _tree(path):
    return ast.parse(path.read_text())


@pytest.mark.parametrize("path", ROUTERS, ids=lambda p: p.name)
def test_routers_stay_thin(path):
    lines = len(path.read_text().splitlines())
    assert lines <= MAX_ROUTER_LINES, (
        f"{path.name} is {lines} lines — move the work into hora/services"
    )


@pytest.mark.parametrize("path", ROUTERS, ids=lambda p: p.name)
def test_routers_do_not_import_calculation_modules(path):
    """A router may import request schemas and services, not the engine.

    `hora.charts.vargas` is allowed for the catalogue endpoint, which publishes
    the registry rather than computing with it.
    """
    allowed_prefixes = (
        "hora.api", "hora.services", "hora.core.settings", "hora.core.notation",
        "hora.charts.vargas", "hora.dasha.nakshatra.systems", "fastapi", "pydantic",
        "__future__",
    )
    for node in ast.walk(_tree(path)):
        module = None
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
        elif isinstance(node, ast.Import):
            module = node.names[0].name
        if module and module.startswith("hora.") and not module.startswith(allowed_prefixes):
            pytest.fail(f"{path.name} imports {module} — call a service instead")


@pytest.mark.parametrize("path", ROUTERS, ids=lambda p: p.name)
def test_routers_contain_no_loops_or_comprehensions(path):
    """Iteration in a router is a strong sign that work has crept back in."""
    for node in ast.walk(_tree(path)):
        if isinstance(node, (ast.For, ast.While, ast.ListComp, ast.DictComp)):
            pytest.fail(
                f"{path.name} contains a {type(node).__name__} — that belongs in a service"
            )


@pytest.mark.parametrize("path", SERVICES, ids=lambda p: p.name)
def test_services_do_not_import_fastapi(path):
    """A service must not know it is being served over HTTP.

    Raising HTTPException from a service is how error handling ends up scattered
    and untestable; services raise plain exceptions and routers translate them.
    """
    text = path.read_text()
    assert "fastapi" not in text, f"{path.name} imports fastapi — raise a plain error"
    assert "HTTPException" not in text, f"{path.name} raises HTTPException"


def test_nothing_above_the_ephemeris_seam_imports_swisseph():
    """The seam that keeps the Swiss Ephemeris licence decision reversible.

    Checked on real import statements, not on the word appearing in prose —
    `settings.py` names Swiss Ephemeris constants in a mapping without importing
    the library, and that is fine.

    `panchanga` and `upagraha` are permitted: they need `swe.MOON` and
    `swe.revjul` for moonrise and calendar arithmetic. Everything else must go
    through the provider.
    """
    allowed = {
        "core/ephemeris/swiss.py",
        "core/timeutil.py",
        "panchanga/core.py",
        "charts/upagraha.py",
    }
    offenders = []
    for path in SRC.rglob("*.py"):
        rel = str(path.relative_to(SRC))
        if "__pycache__" in rel or rel in allowed:
            continue
        for node in ast.walk(_tree(path)):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            if any(n.split(".")[0] == "swisseph" for n in names):
                offenders.append(rel)
                break
    assert not offenders, (
        f"{offenders} import swisseph directly — go through EphemerisProvider, "
        f"or add a deliberate exception here with a reason"
    )


def test_every_router_is_registered_on_the_app():
    """A router file that is never included is dead code that still looks alive."""
    from hora.api.main import app

    registered = {p.split("/")[2] for p in app.openapi()["paths"] if p.startswith("/v1/")}
    expected = {p.stem for p in ROUTERS if p.stem != "__init__"}

    def candidates(name: str) -> list[str]:
        """A file name maps to its URL segment by two conventions only.

        Underscores become hyphens, and a plural file name may serve a
        singular segment (tithis.py -> /v1/tithi). This used to be a
        hand-written alias table, which meant a new router failed the guard
        until someone remembered to add a row. Derive it instead.
        """
        hyphenated = name.replace("_", "-")
        out = [name, hyphenated]
        if hyphenated.endswith("s"):
            out.append(hyphenated[:-1])
        return out

    for name in expected:
        assert any(seg in registered for seg in candidates(name)), (
            f"routers/{name}.py is not mounted on the app"
        )


def test_services_are_all_exported():
    """A service nobody can import from `hora.services` is easy to duplicate."""
    from hora import services

    for path in SERVICES:
        if path.stem == "__init__":
            continue
        assert path.stem in dir(services) or any(
            path.stem.replace("_service", "") in name for name in services.__all__
        ), f"{path.stem} is not reachable from hora.services"


def test_the_package_type_checks():
    """mypy must stay clean.

    Static typing caught three real defects when it was first run: the
    panchanga dataclass declared `hora`, `lunar_months` and `solar_date` as
    bare `object`/`dict`, so nothing checked the attributes read off them in
    the serializer. Without this test that would rot again.
    """
    import shutil
    import subprocess

    mypy = shutil.which("mypy") or str(
        pathlib.Path(__file__).resolve().parents[2] / ".venv" / "bin" / "mypy"
    )
    if not pathlib.Path(mypy).exists():
        pytest.skip("mypy is not installed")

    result = subprocess.run(
        [mypy, "--ignore-missing-imports", str(SRC)],
        capture_output=True, text=True, check=False,
        cwd=pathlib.Path(__file__).resolve().parents[2],
    )
    assert result.returncode == 0, result.stdout or result.stderr
