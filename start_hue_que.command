#!/bin/bash

# 1. Navigate to the project directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# 2. Launch Canon EOS Utility 3
# We use the -a flag to ensure it opens the application bundle
open -a "/Applications/Canon Utilities/EOS Utility/EU3/EOS Utility 3.app"

# 3. Launch the Web Server in a new Terminal window
osascript -e "tell application \"Terminal\" to do script \"cd '$DIR' && source venv/bin/activate && python3 app.py\""

# 4. Launch the Renamer in the CURRENT window (for ID entry)
echo "------------------------------------------------"
echo "HUE-QUE SYSTEM STARTING..."
echo "------------------------------------------------"
source venv/bin/activate
python3 renamer.py
