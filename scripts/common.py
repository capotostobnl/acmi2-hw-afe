from dataclasses import dataclass
from pathlib import Path
import shutil
import zipfile
import json

from pathlib import Path

@dataclass(frozen=True)
class KiCadVariables:
    drawing_number_prefix: str
    assy_suffix: str
    fab_suffix: str
    schema_suffix: str

@dataclass(frozen=True)
class KiCadProjectContext:
    project_file: Path
    project_root: Path
    variables: KiCadVariables


def load_context() -> KiCadProjectContext:
    project_file = find_kicad_project_file()
    project_root = project_file.parent

    variables = load_kicad_variables(project_file)

    return KiCadProjectContext(
        project_file=project_file,
        project_root=project_root,
        variables=variables,
    )


def find_kicad_project_file() -> Path:
    """
    Searches upward from this script folder until it finds a .kicad_pro file.
    Assumes only one exists in project root.
    """
    here = Path(__file__).resolve()

    for parent in here.parents:
        matches = list(parent.glob("*.kicad_pro"))
        if matches:
            return matches[0]

    raise FileNotFoundError("No .kicad_pro file found in parent directories.")


def load_kicad_variables(project_file: Path) -> dict:
    with open(project_file, encoding="utf-8") as f:
        data = json.load(f)

    return data.get("text_variables", {})
