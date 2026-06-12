"""
build_assembly_package.py
Assembly Drawing + Gerbers plotting script for plotting schematics from KiCAD.
Tested on KiCAD Ver 9, Windows.
"""
from pathlib import Path
import subprocess
import shutil
from datetime import datetime
from common import load_context, KICAD_CLI, KiCadProjectContext
from common import cleanup_temp_dir, zip_directory, combine_pdfs


def build_assembly(ctx: KiCadProjectContext) -> None:
    """foo"""
    KICAD_CLI
    subprocess




def build_bom(ctx: KiCadProjectContext) -> None:
    pass


def build_assy_gerbers(ctx: KiCadProjectContext) -> None:
    build_assy_top_grb(ctx)
    build_assy_bot_grb(ctx)
    build_comp_place_grb(ctx)


def build_assy_top_grb(ctx: KiCadProjectContext) -> None:
    pass


def build_assy_bot_grb(ctx: KiCadProjectContext) -> None:
    pass


def build_comp_place_grb(ctx: KiCadProjectContext) -> None:
    pass


def build_assy_pdf(ctx: KiCadProjectContext) -> None:
    build_assy_top_pdf(ctx)
    build_assy_bot_pdf(ctx)


def build_assy_top_pdf(ctx: KiCadProjectContext) -> None:
    pass

def build_assy_bot_pdf(ctx: KiCadProjectContext) -> Path:
    """Build Fab Gerbers Drill.Drawing layer PDF, **NOT** the Excellon file!"""
    output_path_temp = ctx.fab_output_dir_temp
    generated_file = output_path_temp / f"{ctx.pcb_file.stem}-Drill_Drawing.pdf"
    cmd = [
        str(KICAD_CLI),
        "pcb",
        "export",
        "pdf",
        "--output",
        str(generated_file),
        "--layers",
        "Assembly.Bottom,Edge.Cuts",
        "--drawing-sheet",
        str(ctx.fab_titleblock),
        "--include-border-title",
        "--subtract-soldermask",
        "--theme",
        "NSLS-II",
        "--mode-single",
        "--mirror",
        "--sketch-pads-on-fab-layers",
        str(ctx.pcb_file),
    ]
    print("------------------------------------------------------------------")
    print("Creating Drill Drawing Files")
    print(f"Running: {cmd}")
    subprocess.run(cmd, check=True)
    return generated_file


def build_comp_place_pdf(ctx: KiCadProjectContext) -> None:
    pass

if __name__ == "__main__":
    local_ctx = load_context()
    build_assy_bot_pdf(local_ctx)
