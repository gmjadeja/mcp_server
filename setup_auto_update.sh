#!/bin/bash
# Linux/Mac script to set up scheduled auto-updates via cron

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"
MANAGE_PY="$PROJECT_DIR/manage.py"

# Add cron job to update content weekly on Sundays at 2 AM
CRON_JOB="0 2 * * 0 cd $PROJECT_DIR && source venv/bin/activate && $VENV_PYTHON $MANAGE_PY update_content --all --days 7"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "update_content"; then
    echo "Cron job for auto-update already exists!"
    crontab -l | grep "update_content"
else
    # Add the cron job
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Cron job added successfully!"
    echo "Schedule: Weekly on Sundays at 2:00 AM"
    echo "Command: python manage.py update_content --all --days 7"
fi

echo ""
echo "To view your cron jobs: crontab -l"
echo "To remove this cron job: crontab -e (then delete the line)"

