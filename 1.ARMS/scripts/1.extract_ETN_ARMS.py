import os
import subprocess

# Get current script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Navigate relative to script
BASE_DIR = SCRIPT_DIR
R_DIR = os.path.join(BASE_DIR, "R")

EXPORT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "etn_arms_export"))
OUTPUT_PATH = os.path.join(EXPORT_DIR, "deployments_ARMS.csv")


def run_r_pipeline(output_path):
    result = subprocess.run(
        ["Rscript", "extract_ETN_ARMS.R", output_path],
        capture_output=True,
        text=True,
        cwd=R_DIR
    )

    print("---- STDOUT ----")
    print(result.stdout)

    print("---- STDERR ----")
    print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"R script failed with code {result.returncode}")


print("Output path:", OUTPUT_PATH)
run_r_pipeline(OUTPUT_PATH)