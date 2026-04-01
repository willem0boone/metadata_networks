import os
import subprocess

BASE_DIR = r"C:\Users\willem.boone\Documents\projects\AMRIT\Passports_OceanOps\1.ARMS"
R_DIR = os.path.join(BASE_DIR, "R")


def run_r_pipeline(output_path):
    result = subprocess.run(
        ["Rscript", "extract_ETN_ARMS.R", output_path],
        capture_output=True,
        text=True,
        cwd=R_DIR   # 🔥 THIS is the fix
    )

    print("---- STDOUT ----")
    print(result.stdout)

    print("---- STDERR ----")
    print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"R script failed with code {result.returncode}")


run_r_pipeline(os.path.join(BASE_DIR, "ETN_ARMS_EXPORT", "deployments_ARMS.csv"))
