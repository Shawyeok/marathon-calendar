# Quick Start Guide

Get your marathon calendar up and running in minutes!

## 🚀 For Users (Subscribe to Calendar)

### Option 1: Subscribe via Webcal (Easiest)

Click or copy these links to automatically add to your calendar app:

**📱 All Marathons Worldwide:**
```
webcal://YOUR_R2_DOMAIN/marathon-calendar.ics
```

**🇨🇳 China Marathons Only:**
```
webcal://YOUR_R2_DOMAIN/china.ics
```

### Option 2: Subscribe via HTTPS

Use these URLs if webcal doesn't work:

**All Marathons:**
```
https://YOUR_R2_DOMAIN/marathon-calendar.ics
```

**China Marathons:**
```
https://YOUR_R2_DOMAIN/china.ics
```

### Option 3: Backup (GitHub Raw)

If R2 is not available, use GitHub:

**All Marathons:**
```
https://raw.githubusercontent.com/YOUR_USERNAME/marathon-calendar/main/output/marathon-calendar.ics
```

**China Marathons:**
```
https://raw.githubusercontent.com/YOUR_USERNAME/marathon-calendar/main/output/china.ics
```

---

## 🛠️ For Repository Owners (Initial Setup)

### 1. Fork or Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/marathon-calendar.git
cd marathon-calendar
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Test Locally

```bash
# Generate all calendars
python scripts/generate_calendar.py
python scripts/generate_china_calendar.py

# Check output
ls -lh output/
```

### 4. Push to GitHub

```bash
git add .
git commit -m "Initial setup"
git push origin main
```

### 5. Configure R2 (Optional but Recommended)

See [R2_SETUP.md](R2_SETUP.md) for detailed instructions.

**Quick version:**
1. Create Cloudflare R2 bucket
2. Generate API token
3. Add 4 secrets to GitHub:
   - `R2_ACCOUNT_ID`
   - `R2_BUCKET_NAME`
   - `R2_ACCESS_KEY_ID`
   - `R2_SECRET_ACCESS_KEY`

### 6. Enable GitHub Actions

1. Go to repository Settings → Actions → General
2. Set "Workflow permissions" to "Read and write permissions"
3. Save

### 7. Trigger First Workflow Run

1. Go to Actions tab
2. Select "Generate and Deploy Calendar"
3. Click "Run workflow"
4. Wait for completion (about 30 seconds)

### 8. Get Your Calendar URLs

Check the workflow summary for your calendar URLs!

---

## ✍️ Adding Events

### Quick Add

1. Create or edit file: `events/2026/2026-03.yaml`
2. Copy template from `events/TEMPLATE.yaml.example`
3. Fill in event details
4. Commit and push

```bash
git add events/2026/2026-03.yaml
git commit -m "Add Shanghai Marathon 2026"
git push
```

### Minimal Event Example

```yaml
- id: example-marathon-2026
  name: Example Marathon 2026
  date: 2026-03-15
  location:
    city: Shanghai
    country: China
  
  registration:
    open_date: 2025-12-01
    close_date: 2026-01-31
    url: https://example.com/register
```

---

## 🔧 Troubleshooting

### Calendar Not Updating?

**Check workflow status:**
```
GitHub → Actions → Latest run → Check for errors
```

**Force re-run:**
```
Actions → Select workflow → Run workflow
```

### YAML Syntax Error?

**Validate locally:**
```bash
python scripts/generate_calendar.py
# If error, fix YAML file and try again
```

**Common issues:**
- Missing required fields (`id`, `name`, `date`, `location`)
- Incorrect date format (use `YYYY-MM-DD`)
- Wrong indentation (use 2 spaces)
- Special characters not quoted

### R2 Upload Failing?

**Check secrets are configured:**
```
Settings → Secrets → Actions → Check R2 secrets exist
```

**Verify credentials:**
- Account ID matches Cloudflare dashboard
- Bucket name is exactly correct
- API token has write permissions

### Can't Subscribe to Calendar?

**Try different URL:**
- Try webcal:// instead of https://
- Try GitHub raw URL if R2 fails
- Check URL is accessible in browser

**Device-specific:**
- **iPhone**: Must use Safari for webcal://
- **Android**: Use Google Calendar web interface
- **Outlook**: Use https:// URL only

---

## 📚 Next Steps

- **Add more events**: See [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Configure R2**: See [R2_SETUP.md](R2_SETUP.md)
- **Customize workflow**: See [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)
- **Full deployment**: See [DEPLOYMENT.md](../DEPLOYMENT.md)

---

## 💡 Tips

### Auto-Update Frequency

Your calendar app will check for updates:
- **iPhone/iPad**: Daily
- **Google Calendar**: Every 24 hours
- **Outlook**: Based on your settings

### Multiple Calendars

You can subscribe to multiple calendars:
- All marathons (global view)
- China only (focused view)
- Both (separate calendars in your app)

### Sharing Your Calendar

Share the subscription URL with:
- Running clubs
- Social media
- Marathon communities
- Friends and family

### Manual Refresh

Force calendar to update now:
- **iPhone**: Pull down in calendar view
- **Google Calendar**: Wait or re-subscribe
- **Outlook**: Right-click calendar → Update

---

## 🆘 Getting Help

- **Quick questions**: Check [README.md](../README.md)
- **Setup issues**: Check [DEPLOYMENT.md](../DEPLOYMENT.md)
- **Workflow issues**: Check [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)
- **R2 setup**: Check [R2_SETUP.md](R2_SETUP.md)
- **Bug reports**: Open a GitHub Issue
- **Feature requests**: Open a GitHub Issue with "enhancement" label

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Subscribe to calendar | 1 minute |
| Fork and setup repository | 5 minutes |
| Configure R2 (optional) | 10-15 minutes |
| Add first event | 5 minutes |
| Full customization | 30+ minutes |

---

**Ready?** Start with subscribing to the calendar, then explore adding your own events! 🏃‍♀️🏃‍♂️

