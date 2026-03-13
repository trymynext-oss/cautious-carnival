#!/bin/bash

echo "🚀 Starting WhatsApp Allocation Bot Setup..."

# update pip
echo "Updating pip..."
python3 -m pip install --upgrade pip

# install dependencies
echo "Installing required Python packages..."
pip install telethon neonize

# create required files if missing
echo "Checking project files..."

files=("whatsapp.py" "allocate.py" "allocate_worker.py" "accounts.py" "config.py")

for f in "${files[@]}"
do
    if [ ! -f "$f" ]; then
        echo "⚠ Missing file: $f"
    else
        echo "✔ Found $f"
    fi
done

# create accounts storage if missing
if [ ! -f "accounts.py" ]; then
echo "accounts = []" > accounts.py
echo "✔ Created accounts.py"
fi

# create session folder
mkdir -p session

echo ""
echo "✅ Setup completed!"
echo ""
echo "Next step:"
echo "Run the bot with:"
echo ""
echo "python whatsapp.py"
echo ""