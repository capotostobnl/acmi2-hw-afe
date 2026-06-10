"""
build_fabrication_package.py
Fab Drawing + Gerbers plotting script for plotting schematics from KiCAD.
Tested on KiCAD Ver 9, Windows.
"""
from pathlib import Path
import atexit
import subprocess
import shutil
from common import load_context, KICAD_CLI, KiCadProjectContext


def build_fab(ctx: KiCadProjectContext) -> None:
    build_fab_gerbers(ctx)


def cleanup_temp_dir(ctx: KiCadProjectContext) -> None:
    """Delete the TEMP Directory"""
    if ctx.fab_output_dir_temp.exists():
        shutil.rmtree(ctx.fab_output_dir_temp)
        print("Deleted temp folder:", ctx.fab_output_dir_temp)


def build_drill(ctx: KiCadProjectContext) -> None:
    """Build Drill file Excellon format"""
    prefix = ctx.variables.drawing_number_prefix
    suffix = ctx.variables.fab_suffix
    revision_num = ctx.variables.revision_num

    filename_drl = f"{prefix}-{suffix}_Rev-{revision_num}.drl"
    final_output_file = ctx.fab_output_dir / filename_drl

    output_path_temp = ctx.fab_output_dir_temp
    generated_drl_file = output_path_temp / f"{ctx.pcb_file.stem}.drl"

    cmd = [
        str(KICAD_CLI),
        "pcb",
        "export",
        "drill",
        "--output",
        str(output_path_temp),
        "--format",
        "excellon",
        "--drill-origin",
        "absolute",
        "--excellon-zeros-format",
        "decimal",
        "--excellon-oval-format",
        "alternate",
        "--excellon-units",
        "mm",
        "--gerber-precision",
        "6",
        str(ctx.pcb_file),
    ]
    print("------------------------------------------------------------------")
    print("Creating Excellon Drill Files")
    print(f"Running: {cmd}")

    subprocess.run(cmd, check=True)

    print("Generated DRILL_FILE_EXCELLON output:", str(output_path_temp))
    print("Moving file....")

    if not generated_drl_file.is_file():
        raise FileNotFoundError(
            f"Expected drill file was not generated: {generated_drl_file}"
        )

    shutil.move(generated_drl_file, final_output_file)

    print(f"Move done, moved to: {final_output_file}")
    print("------------------------------------------------------------------")


def build_ipc_d356(ctx: KiCadProjectContext) -> None:
    """Build IPC-D-356 Netlist file"""
    prefix = ctx.variables.drawing_number_prefix
    suffix = ctx.variables.fab_suffix
    revision_num = ctx.variables.revision_num

    filename_d356 = f"{prefix}-{suffix}_Rev-{revision_num}.d356"
    generated_d356_file = Path(ctx.project_root / filename_d356)

    final_output_file = Path(ctx.fab_output_dir / filename_d356)

    cmd = [
        str(KICAD_CLI),
        "pcb",
        "export",
        "ipcd356",
        "--output",
        str(filename_d356),
        str(ctx.pcb_file),
    ]
    print("------------------------------------------------------------------")
    print("Creating IPC-D-356 Netlist Files")
    print(f"Running: {cmd}")

    subprocess.run(cmd, check=True)

    print(f"Generated IPC-D-356 output: {generated_d356_file}")

    print(f"Moving file....{generated_d356_file}")
    # KiCAD puts the d356 file to the project root directory by default, and
    # can't be changed by CLI...

    if not generated_d356_file.is_file():
        raise FileNotFoundError(
            f"Expected d356 file was not generated: {generated_d356_file}"
        )

    shutil.move(generated_d356_file, final_output_file)

    print(f"Move done, moved to: {final_output_file}")
    print("------------------------------------------------------------------")


def build_fab_gerbers(ctx: KiCadProjectContext) -> None:
    """Build Fab Gerbers"""
    build_drill_dwg_layer_gerbers(ctx)


def build_drill_dwg_layer_gerbers(ctx: KiCadProjectContext) -> None:
    """Build Fab Gerbers"""
    prefix = ctx.variables.drawing_number_prefix
    suffix = ctx.variables.fab_suffix
    revision_num = ctx.variables.revision_num

    filename = f"{prefix}-{suffix}_Rev-{revision_num}.gbr"
    final_output_file = ctx.fab_output_dir / filename

    output_path_temp = ctx.fab_output_dir_temp
    generated_file = output_path_temp / f"{ctx.pcb_file.stem}-Drill_Drawing.gbr"

    cmd = [
        str(KICAD_CLI),
        "pcb",
        "export",
        "gerbers",
        "--output",
        str(output_path_temp),
        "--drawing-sheet",
        str(ctx.fab_titleblock),
        "--layers",
        "Drill.Drawing",
        "--include-border-title",
        "--subtract-soldermask",
        "--common-layers",
        "Edge.Cuts",
        str(ctx.pcb_file),
    ]
    print("------------------------------------------------------------------")
    print("Creating Drill Drawing Files")
    print(f"Running: {cmd}")
    subprocess.run(cmd, check=True)

    print("Generated DRILL_DRAWING_FILE output:", str(output_path_temp))
    print("Moving file....")
    if not generated_file.is_file():
        raise FileNotFoundError(
            f"Expected drill file was not generated: {generated_file}"
        )

    shutil.move(generated_file, final_output_file)

    print(f"Move done, moved to: {final_output_file}")
    print("------------------------------------------------------------------")


if __name__ == "__main__":
    local_ctx = load_context()
    # build_drill(local_ctx)
    # build_ipc_d356(local_ctx)
    # atexit.register(cleanup_temp_dir, local_ctx)
    build_drill_dwg_layer_gerbers(local_ctx)
