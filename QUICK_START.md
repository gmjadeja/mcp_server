# Quick Start Guide

## ✅ Completed Setup Steps

1. ✅ Dependencies installed
2. ✅ Database migrations created and applied
3. ✅ System check passed - no issues

## 🔧 Next Steps (Manual)

### 1. Create Environment File

Create a `.env` file in the project root with:
```env
DEBUG=True
SECRET_KEY=django-insecure-zbe0*_hg4t-t^q7($8x*sm5uf5&a-y#$hd0_rarp4%*(m*$77g
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

**Get your Anthropic API key from:** https://console.anthropic.com/

### 2. Create Superuser

Run this command to create an admin account:
```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### 3. Start Development Server

```bash
python manage.py runserver
```

Then visit:
- **Homepage:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

### 4. Add Initial Content

1. Login to admin panel at `/admin/`
2. Add content in this order:
   - **MCP Providers** (e.g., "Anthropic Claude", "OpenAI")
   - **Learning Paths** (e.g., "Claude-Supported MCP Servers", "Custom MCP Servers")
   - **Courses** (e.g., "Introduction to MCP Servers")
   - **Lessons** (within courses)
   - **Labs** (hands-on exercises)

### 5. Test Claude Auto-Update (Optional)

Once you have content and your API key set:
```bash
python manage.py update_content --type course --id 1
```

This will generate an update suggestion (pending approval in admin).

## 📝 Important Notes

- The server is configured for your domains: `mcp-server.ca` and `mcp-servcer.ca`
- For production, set `DEBUG=False` in `.env`
- Auto-updates create pending updates that need approval in admin
- Static files will be served automatically in development

## 🚀 Production Deployment

See `DEPLOYMENT.md` for detailed production setup instructions.

## 🆘 Troubleshooting

**Can't access admin?**
- Make sure you created a superuser (step 2)

**Static files not loading?**
- Run: `python manage.py collectstatic` (production only)

**Claude API not working?**
- Check your `.env` file has `ANTHROPIC_API_KEY` set
- Verify the API key is correct

**Database errors?**
- Run: `python manage.py migrate`

