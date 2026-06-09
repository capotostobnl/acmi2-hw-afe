from common import load_context
from build_schematic_package import build_schematic
from build_assembly_package import build_assembly
from build_fabrication_package import build_fabrication


def get_build_options():
    schematic = assembly = fabrication = False

    while True:
        print("\nSelect package(s) to build:")
        print("  1) Schematic")
        print("  2) Assembly")
        print("  3) Fabrication")
        print("  4) All")
        print("  q) Quit")

        choice = input("\nChoice: ").strip().lower()

        try:
            if choice == "1":
                schematic = True
                break

            elif choice == "2":
                assembly = True
                break

            elif choice == "3":
                fabrication = True
                break

            elif choice == "4":
                schematic = assembly = fabrication = True
                break

            elif choice == "q":
                raise SystemExit(0)

            else:
                raise ValueError("Invalid selection")

        except ValueError as e:
            print(f"\nError: {e}")

    return schematic, assembly, fabrication


def main():
    schematic, assembly, fabrication = get_build_options()
    ctx = load_context()

    if schematic:
        # ---- Output directory ----
        sch_out_dir = ctx.project_root / "Outputs" / "SCH"
        sch_out_dir.mkdir(parents=True, exist_ok=True)

        build_schematic(ctx, sch_out_dir)
    if assembly:
        # ---- Output directory ----
        assy_out_dir = ctx.project_root / "Outputs" / "ASSY"
        assy_out_dir.mkdir(parents=True, exist_ok=True)

        build_assembly(ctx)
    if fabrication:
        # ---- Output directory ----
        fab_out_dir = ctx.project_root / "Outputs" / "FAB"
        fab_out_dir.mkdir(parents=True, exist_ok=True)
        build_fabrication(ctx)


if __name__ == "__main__":
    main()
