# Deployment Guide for MCP Education Website

## Quick Start for Local Development

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment:**
   - Copy `.env.example` to `.env`
   - Add your `ANTHROPIC_API_KEY` in `.env`
   - Set `DEBUG=True` for development

3. **Initialize Database:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Run Development Server:**
   ```bash
   python manage.py runserver
   ```

## Production Deployment

### Option 1: Using Gunicorn (Recommended for Linux/Mac)

1. **Install Gunicorn:**
   ```bash
   pip install gunicorn
   ```

2. **Collect Static Files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Run with Gunicorn:**
   ```bash
   gunicorn demo_site.wsgi:application --bind 0.0.0.0:8000 --workers 4
   ```

### Option 2: Using Waitress (Lightweight for Windows)

1. **Install Waitress:**
   ```bash
   pip install waitress
   ```

2. **Run with Waitress:**
   ```bash
   waitress-serve --port=8000 demo_site.wsgi:application
   ```

### Option 3: Using uWSGI (Advanced)

```bash
pip install uwsgi
uwsgi --http :8000 --module demo_site.wsgi --processes 4 --threads 2
```

## Setting Up Auto-Updates

### Windows (Task Scheduler)

1. Run `setup_auto_update.bat` as Administrator, OR

2. Manually create a scheduled task:
   - Open Task Scheduler
   - Create Basic Task
   - Trigger: Weekly on Sundays at 2:00 AM
   - Action: Start a program
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `C:\path\to\manage.py update_content --all --days 7`
   - Start in: `C:\path\to\project`

### Linux/Mac (Cron)

1. Run `setup_auto_update.sh`, OR

2. Manually add to crontab:
   ```bash
   crontab -e
   ```
   Add this line:
   ```
   0 2 * * 0 cd /path/to/project && source venv/bin/activate && python manage.py update_content --all --days 7
   ```

## Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Set a secure `SECRET_KEY` in `.env`
- [ ] Configure `ALLOWED_HOSTS` in `settings.py`
- [ ] Set up proper database (PostgreSQL recommended)
- [ ] Configure static file serving (nginx, Apache, or cloud storage)
- [ ] Set up SSL/HTTPS certificate
- [ ] Configure domain DNS to point to your server
- [ ] Set up regular backups
- [ ] Configure logging
- [ ] Set up monitoring (optional)
- [ ] Test auto-update functionality
- [ ] Create initial content in Django admin

## Domain Configuration

Your domain `mcp-server.ca` (or `mcp-servcer.ca`) should:
1. Point DNS A record to your server's IP address
2. Be included in `ALLOWED_HOSTS` in `settings.py`
3. Have SSL certificate configured (use Let's Encrypt for free SSL)

## Lightweight Server Recommendations

### For Windows Laptop:
- **Waitress**: Python-native, works well on Windows
- **Nginx** (reverse proxy) + **Gunicorn/Waitress**: Best performance

### For Linux:
- **Gunicorn** + **Nginx**: Industry standard
- **Systemd** service for auto-restart on reboot

## Environment Variables

Create a `.env` file with:
```env
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key
```

**Never commit `.env` to git!**

## Troubleshooting

### Static files not loading:
```bash
python manage.py collectstatic
```

### Database errors:
```bash
python manage.py migrate
```

### Auto-updates not working:
- Check `ANTHROPIC_API_KEY` is set correctly
- Check scheduled task/cron job is running
- Check logs: `python manage.py update_content --all --days 7`

### Domain not accessible:
- Check `ALLOWED_HOSTS` includes your domain
- Check firewall allows port 80/443
- Check DNS is correctly configured

