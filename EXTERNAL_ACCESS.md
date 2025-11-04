# Making Your Website Accessible from Outside

## Current Status

✅ **Settings are configured correctly** - Your `ALLOWED_HOSTS` includes:
- `mcp-server.ca`
- `www.mcp-server.ca`
- `mcp-servcer.ca`
- `www.mcp-servcer.ca`

❌ **Server is currently only accessible locally** - It's running on `127.0.0.1:8000`

## Making It Accessible from Outside

### Option 1: Development Server (Testing Only)

**Windows:**
```bash
python manage.py runserver 0.0.0.0:8000
```
Or use: `run_server_public.bat`

**Linux/Mac:**
```bash
python manage.py runserver 0.0.0.0:8000
```
Or use: `run_server_public.sh`

⚠️ **Warning**: Django's development server is NOT for production use!

### Option 2: Production Server (Recommended)

Use a production WSGI server:

**Windows (Waitress):**
```bash
waitress-serve --host=0.0.0.0 --port=8000 demo_site.wsgi:application
```

**Linux (Gunicorn):**
```bash
gunicorn --bind 0.0.0.0:8000 demo_site.wsgi:application
```

## Required Steps for External Access

### 1. Configure Firewall

**Windows:**
- Open Windows Firewall
- Allow incoming connections on port 8000 (or 80/443 for production)
- Or run: `netsh advfirewall firewall add rule name="Django" dir=in action=allow protocol=TCP localport=8000`

**Linux:**
```bash
sudo ufw allow 8000
# Or for production:
sudo ufw allow 80
sudo ufw allow 443
```

### 2. Set Up Domain DNS

1. Log into your domain registrar (where you bought `mcp-server.ca`)
2. Add an **A Record**:
   - **Name**: `@` or `mcp-server.ca`
   - **Type**: A
   - **Value**: Your public IP address
3. Add a **CNAME Record** for www:
   - **Name**: `www`
   - **Type**: CNAME
   - **Value**: `mcp-server.ca`

### 3. Find Your Public IP

**Windows:**
```powershell
Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing | Select-Object -ExpandProperty Content
```

**Linux/Mac:**
```bash
curl https://api.ipify.org
```

Or visit: https://whatismyipaddress.com/

### 4. Update Environment Variables

Make sure your `.env` file has:
```env
DEBUG=False
SECRET_KEY=your-secure-secret-key-here
ANTHROPIC_API_KEY=your-api-key
```

### 5. Configure Port Forwarding (If Behind Router)

If your laptop is behind a router:
1. Access your router admin panel (usually 192.168.1.1)
2. Set up port forwarding:
   - External Port: 80 (HTTP) or 443 (HTTPS)
   - Internal Port: 8000
   - Internal IP: Your laptop's local IP (192.168.x.x)
   - Protocol: TCP

### 6. Set Up SSL/HTTPS (Recommended)

For production, use Let's Encrypt with Certbot:
```bash
# Install certbot
# Windows: Use WSL or install manually
# Linux: sudo apt-get install certbot

# Get certificate
sudo certbot certonly --standalone -d mcp-server.ca -d www.mcp-server.ca
```

Then use a reverse proxy (nginx) to serve HTTPS.

## Testing External Access

1. **From another device on same network:**
   - Use your laptop's local IP: `http://192.168.x.x:8000`

2. **From outside your network:**
   - Use your public IP: `http://your-public-ip:8000`
   - Or use your domain: `http://mcp-server.ca:8000` (after DNS propagates)

## Security Checklist

Before going public:

- [ ] Set `DEBUG=False` in `.env`
- [ ] Use a strong `SECRET_KEY`
- [ ] Set up SSL/HTTPS
- [ ] Configure proper firewall rules
- [ ] Use a production WSGI server (not Django dev server)
- [ ] Set up regular backups
- [ ] Configure logging
- [ ] Review Django security checklist: https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

## Current Configuration Review

✅ **ALLOWED_HOSTS** - Correctly configured with your domains  
✅ **Domain settings** - Ready for `mcp-server.ca`  
⚠️ **Server binding** - Currently localhost only (needs `0.0.0.0`)  
⚠️ **Firewall** - Needs to allow port 8000  
⚠️ **DNS** - Needs to point to your IP  
⚠️ **SSL** - Recommended for production  

## Troubleshooting

**Can't access from outside?**
- Check firewall settings
- Verify DNS is pointing to correct IP
- Check router port forwarding
- Ensure server is bound to `0.0.0.0` not `127.0.0.1`

**Getting "DisallowedHost" error?**
- Check `ALLOWED_HOSTS` in settings.py includes your domain
- Verify DNS is correct

**Static files not loading?**
- Run: `python manage.py collectstatic`
- Configure proper static file serving in production

