# Cloudflare R2 Setup Guide

This guide explains how to set up Cloudflare R2 bucket and configure GitHub secrets for automatic deployment.

## Prerequisites

- Cloudflare account with R2 enabled
- GitHub repository with admin access

## Step 1: Create R2 Bucket

1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Navigate to **R2** in the sidebar
3. Click **Create bucket**
4. Enter bucket name (e.g., `marathon-calendar`)
5. Choose a location (auto or specific region)
6. Click **Create bucket**

## Step 2: Get R2 Account ID

1. In the R2 dashboard, your Account ID is displayed at the top
2. Copy the Account ID (format: `a1b2c3d4e5f6...`)

## Step 3: Create R2 API Token

1. In Cloudflare Dashboard, go to **R2** → **Manage R2 API Tokens**
2. Click **Create API Token**
3. Configure the token:
   - **Token name**: `marathon-calendar-github-actions`
   - **Permissions**: 
     - ✅ Object Read & Write
   - **Specify bucket** (optional): Select your specific bucket for better security
   - **TTL**: Never expire (or set expiration as needed)
4. Click **Create API Token**
5. **Important**: Copy both:
   - **Access Key ID** (like AWS Access Key)
   - **Secret Access Key** (like AWS Secret Key)
   
   ⚠️ The Secret Access Key is only shown once!

## Step 4: Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add the following:

### Required Secrets

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `R2_ACCOUNT_ID` | Your Cloudflare Account ID | `a1b2c3d4e5f6...` |
| `R2_BUCKET_NAME` | Your R2 bucket name | `marathon-calendar` |
| `R2_ACCESS_KEY_ID` | R2 API Token Access Key ID | `abc123...` |
| `R2_SECRET_ACCESS_KEY` | R2 API Token Secret Access Key | `xyz789...` |

### Optional Secrets

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `R2_PUBLIC_URL` | Custom domain or R2 public bucket URL | `https://calendar.yourdomain.com` |

## Step 5: Configure Public Access (Optional)

If you want your calendar files to be publicly accessible via R2:

### Option A: Public Bucket (Simple)

1. In R2 dashboard, select your bucket
2. Go to **Settings** → **Public access**
3. Enable **Allow public access**
4. Note the public URL: `https://pub-{hash}.r2.dev`
5. Add this URL as `R2_PUBLIC_URL` secret in GitHub

### Option B: Custom Domain (Recommended)

1. In R2 dashboard, select your bucket
2. Go to **Settings** → **Custom Domains**
3. Click **Connect Domain**
4. Enter your domain (e.g., `calendar.yourdomain.com`)
5. Follow DNS configuration instructions
6. Once verified, add this domain as `R2_PUBLIC_URL` secret

**Example DNS Record:**
```
Type: CNAME
Name: calendar
Target: {your-bucket}.r2.cloudflarestorage.com
Proxy: ✅ Proxied (recommended for CDN)
```

## Step 6: Test the Workflow

1. Make a change to an event YAML file in `events/` directory
2. Commit and push to `main` branch
3. Go to **Actions** tab in GitHub
4. Watch the "Generate and Deploy Calendar" workflow run
5. Check the deployment summary for access URLs

## Access Your Calendar

### Via R2 (Recommended - Fast CDN)

```
https://YOUR_R2_PUBLIC_URL/marathon-calendar.ics
```

Subscribe in calendar apps using `webcal://` protocol:
```
webcal://YOUR_R2_PUBLIC_URL/marathon-calendar.ics
```

### Via GitHub (Fallback)

```
https://raw.githubusercontent.com/YOUR_USERNAME/marathon-calendar/main/output/marathon-calendar.ics
```

## Troubleshooting

### Workflow Fails with "Access Denied"

- Verify R2 API token has correct permissions
- Check that bucket name matches exactly
- Ensure Account ID is correct

### Files Not Publicly Accessible

- Enable public access on R2 bucket, or
- Configure custom domain properly
- Check that files were actually uploaded (check workflow logs)

### Calendar Not Updating

- Check GitHub Actions workflow status
- Verify workflow triggers are configured correctly
- Force update: manually trigger workflow from Actions tab

## Security Best Practices

1. **Use specific bucket permissions**: Only grant access to the specific bucket needed
2. **Rotate tokens regularly**: Set expiration dates and rotate API tokens
3. **Use separate tokens**: Different tokens for different purposes (CI/CD, local dev, etc.)
4. **Monitor usage**: Check R2 dashboard for unusual activity
5. **Enable Cloudflare WAF**: If using custom domain, enable Web Application Firewall rules

## Cost Considerations

**Cloudflare R2 Pricing** (as of 2024):
- Storage: $0.015 per GB/month
- Class A Operations (writes): $4.50 per million
- Class B Operations (reads): $0.36 per million
- Egress: **FREE** (no bandwidth charges!)

**Estimated monthly costs for this project**:
- Storage (< 1 MB): < $0.01
- Writes (< 100/month): < $0.01
- Reads (depends on subscribers): $0.00 - $0.36

**Total: ~$0.02 - $0.37 per month** (essentially free!)

R2's free tier includes:
- 10 GB storage/month
- 1 million Class A operations/month
- 10 million Class B operations/month

## Additional Features

### Cache Control

The workflow sets appropriate cache headers:
- `max-age=3600` (1 hour cache)
- Calendar apps typically check every 24 hours anyway

### Metadata

Each uploaded file includes:
- Content-Type: `text/calendar`
- Generated timestamp
- Custom metadata for tracking

### Multiple Calendars

The workflow automatically uploads all `.ics` files in `output/`:
- `marathon-calendar.ics` - All events
- `china.ics` - China-specific events (if generated)
- Add more filtered calendars as needed

## Next Steps

1. ✅ Set up R2 bucket and API tokens
2. ✅ Configure GitHub secrets
3. ✅ Test workflow execution
4. 🔄 (Optional) Set up custom domain
5. 📱 Subscribe to calendar in your apps
6. 🌟 Share calendar URL with others!

## Support

For issues related to:
- **Cloudflare R2**: [Cloudflare Docs](https://developers.cloudflare.com/r2/)
- **GitHub Actions**: [GitHub Actions Docs](https://docs.github.com/actions)
- **This Project**: Open an issue in this repository

