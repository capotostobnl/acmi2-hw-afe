import subprocess
from common import load_context


def build_schematic(ctx, sch_out_dir):
    """
    Generates schematic PDF package using KiCad CLI.
    Output name is driven by KiCad project variables:
    DRAWING_NUMBER-PREFIX + DRAWING-SCHEMA_SUFFIX
    """

    # ---- Extract naming variables ----
    prefix = ctx.variables["DRAWING_NUMBER-PREFIX"]
    suffix = ctx.variables["DRAWING-SCHEMA_SUFFIX"]

    filename = f"{prefix}{suffix}.pdf"

    output_path = sch_out_dir / filename

    # ---- Schematic file ----
    schematic_file = ctx.project_root / (ctx.project_file.stem + ".kicad_sch")

    # ---- Drawing sheet ----
    drawing_sheet = ctx.project_root / \
        "KiCAD_NSLS_PLDF_Schematic.kicad_wks"
    print(drawing_sheet)
    print(drawing_sheet.exists())
    # ---- KiCad CLI export ----
    cmd = [
        "kicad-cli",
        "sch",
        "export",
        "pdf",
        "--output",
        str(output_path),
        "--theme",
        "NSLS-II",
        "--drawing-sheet",
        str(drawing_sheet),
        str(schematic_file)
    ]

    print("Running:", " ".join(cmd))

    subprocess.run(cmd, check=True)

    print("Generated schematic:", output_path)


if __name__ == "__main__":
    ctx = load_context()
    build_schematic(ctx)
