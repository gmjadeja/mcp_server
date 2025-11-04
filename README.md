# MCP Server Education Website

An educational web application for teaching MCP (Model Context Protocol) servers. Built with Django and auto-updated using Claude AI.

## Features

- **Comprehensive Courses**: Structured learning paths for MCP servers
- **Interactive Labs**: Hands-on exercises and coding challenges
- **Learning Paths**: Choose between Claude-supported or custom MCP server development
- **Auto-Updates**: Content automatically updated with latest MCP information using Claude AI
- **Modern UI**: Beautiful, responsive design with Tailwind CSS

## Requirements

- Python 3.10+
- Django 5.2.7+
- Anthropic API key (for Claude integration)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gmjadeja/mcp_server.git
cd mcp_server
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Auto-Update Content with Claude

The website includes automated content updates using Claude AI. To update content:

### Update specific content:
```bash
python manage.py update_content --type course --id 1
python manage.py update_content --type lesson --id 1
python manage.py update_content --type lab --id 1
```

### Update all content older than X days:
```bash
python manage.py update_content --all --days 7
```

Content updates are created as "pending" and can be reviewed and approved in the Django admin.

## Setting Up Scheduled Updates

To automatically update content, set up a cron job or scheduled task:

### Linux/Mac (cron):
```bash
# Update content weekly
0 2 * * 0 cd /path/to/project && source venv/bin/activate && python manage.py update_content --all --days 7
```

### Windows (Task Scheduler):
Create a scheduled task that runs:
```powershell
cd C:\path\to\project
venv\Scripts\activate
python manage.py update_content --all --days 7
```

## Deployment

### Using a Lightweight Web Server (Gunicorn)

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn demo_site.wsgi:application --bind 0.0.0.0:8000
```

### Production Settings

Make sure to:
- Set `DEBUG=False` in production
- Use a proper database (PostgreSQL recommended)
- Set up proper static file serving
- Configure ALLOWED_HOSTS correctly
- Use environment variables for sensitive data

## Project Structure

```
demo_site/
├── demo_site/          # Django project settings
├── hello/              # Main app
│   ├── models.py       # Course, Lesson, Lab models
│   ├── views.py        # View functions
│   ├── services/       # Claude API service
│   └── management/     # Management commands
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS)
└── media/              # User-uploaded files
```

## Domain Configuration

The site is configured for:
- `mcp-server.ca`
- `www.mcp-server.ca`
- `mcp-servcer.ca`
- `www.mcp-servcer.ca`

Update `ALLOWED_HOSTS` in `settings.py` if needed.

## License

MIT License

