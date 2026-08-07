"""Shared pytest fixtures and module loaders.

Scripts under ``scripts/`` are not part of the importable ``merge_odds``
package, so each one gets loaded here via ``importlib`` under a stable
module name that tests can import from directly (see ``render_module``
below). Tasks 7 and 8 append one loader block each, following this pattern.
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

_spec = importlib.util.spec_from_file_location("render_module", ROOT / "scripts" / "render.py")
render_module = importlib.util.module_from_spec(_spec)
sys.modules["render_module"] = render_module
_spec.loader.exec_module(render_module)

_vspec = importlib.util.spec_from_file_location(
    "validate_module", ROOT / "scripts" / "validate_data.py"
)
validate_module = importlib.util.module_from_spec(_vspec)
sys.modules["validate_module"] = validate_module
_vspec.loader.exec_module(validate_module)
