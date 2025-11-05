#!/bin/bash
#SBATCH --job-name=tvguide-sqlite
#SBATCH --time=00:05:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
mkdir -p logs

echo "=== $(date) | Starting $SLURM_JOB_ID in $PWD ==="

# Optional: use your existing venv; not required but harmless
VENV_DIR="./home/ak562fx/ss"
if [ -d "$VENV_DIR" ]; then
  # shellcheck disable=SC1090
  source "$VENV_DIR/bin/activate"
fi

# No requirements needed for sqlite3, but if you keep a requirements.txt, this won't hurt
if [ -f requirements.txt ] && [ -s requirements.txt ]; then
  python -m pip install --upgrade pip
  pip install --no-input -r requirements.txt
fi

# Sanity check inputs
ls -l tv_programs_*.txt || true
test -f load_tv_programs_sqlite.py

# Run
srun python load_tv_programs_sqlite.py

echo "=== $(date) | Finished $SLURM_JOB_ID ==="
