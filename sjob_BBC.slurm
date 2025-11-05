#!/bin/bash
#SBATCH --job-name=tvprog-scrape-BBC
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --output=logs/%x_%j.out        # per-job stdout
#SBATCH --error=logs/%x_%j.err         # per-job stderr
# #SBATCH --mail-type=FAIL,END
# #SBATCH --mail-user=you@example.com

set -euo pipefail

# Always start where the job was submitted
cd "$SLURM_SUBMIT_DIR"

# Ensure the logs directory exists *before* we write anything there
mkdir -p logs

#################################
# Virtual environment (your way)
#################################
# Your settings:
VENV_DIR="./home/ak562fx/ss"

# Create/activate + install deps (mirrors your script)
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment in $VENV_DIR ..."
  python3 -m venv "$VENV_DIR"
fi

echo "Activating virtual environment ..."
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

echo "Upgrading pip ..."
pip install --upgrade pip

if [ -f requirements.txt ]; then
  echo "Installing requirements ..."
  pip install -r requirements.txt
else
  echo "requirements.txt not found, skipping install."
  # Minimal deps for your script:
  pip install requests beautifulsoup4 > /dev/null || true
fi

############################
# Run the scraper script   #
############################
# Update the script name if yours differs
python scraper_BBC.py

echo "Done. Check logs/ and tv_programs_BBC.txt in $SLURM_SUBMIT_DIR."
