#!/bin/bash
#SBATCH --job-name=tv-flask
#SBATCH --time=00:50:00           
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
mkdir -p logs

echo "=== $(date) | Starting Flask API on $SLURM_JOB_NODELIST ==="

# Activate your venv
VENV_DIR="./home/ak562fx/ss"
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

# Install requirements
if [ -f requirements.txt ]; then
  python -m pip install --upgrade pip
  pip install --no-input -r requirements.txt
else
  pip install Flask
fi

# Run Flask server (will block until timeout)
srun python flask_now_playing.py
