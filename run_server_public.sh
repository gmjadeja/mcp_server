#!/bin/bash
# Run Django server accessible from outside (for production testing)
# This binds to 0.0.0.0 which makes it accessible from external networks

echo "Starting Django server on 0.0.0.0:8000..."
echo "This will make the server accessible from outside your local machine."
echo ""
echo "Make sure:"
echo "1. Your firewall allows port 8000"
echo "2. Your domain DNS points to this machine's IP"
echo "3. DEBUG=False in production (set in .env)"
echo ""

python manage.py runserver 0.0.0.0:8000

