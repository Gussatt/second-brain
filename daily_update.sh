#!/bin/bash

# ==============================================================================
# Gemini Powerhouse Daily Automation Script
# ==============================================================================

# 1. SETUP ENVIRONMENT
# Load environment variables from .env file
if [ -f "/Users/gustavo.saturnino/Documents/meuSegundoCerebro/.env" ]; then
  source "/Users/gustavo.saturnino/Documents/meuSegundoCerebro/.env"
fi
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
export HOME="$HOME"
export GEMINI_CLI_TRUST_WORKSPACE=true
export GEMINI_SANDBOX=false

# 2. NAVIGATE TO VAULT
VAULT_PATH="/Users/gustavo.saturnino/Documents/meuSegundoCerebro"
cd "$VAULT_PATH"

# 3. RUN THE DAILY POWERHOUSE ROUTINE
# We use YOLO mode to auto-approve tool calls for headless execution.
gemini --approval-mode=yolo -p "Perform the following morning routine:
1. Run the wiki-lint skill to audit '06 Wiki' for health.
2. Run the vault-update skill to update my vault Daily Brief and News.
4. Check '05 Projects' and list any project that hasn't had an update in its log for 48 hours."

echo "Routine Completed: $(date)"
