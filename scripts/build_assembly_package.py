"""
build_assembly_package.py
Assembly Drawing + Gerbers plotting script for plotting schematics from KiCAD.
Tested on KiCAD Ver 9, Windows.
"""
import subprocess
from common import load_context, KICAD_CLI, KiCadProjectContext


def build_assembly(ctx: KiCadProjectContext):
    """foo"""
    KICAD_CLI
    subprocess


if __name__ == "__main__":
    local_ctx = load_context()
    build_assembly(local_ctx)
