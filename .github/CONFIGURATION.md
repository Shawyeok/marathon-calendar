# Workflow Configuration Options

This document explains all configuration options for the GitHub Actions workflow.

## Overview

The workflow is designed to be **zero-configuration** by default, but offers several optional customizations.

## Default Behavior

✅ **Out of the box:**
- Generates calendar files from YAML events
- Commits generated files to repository (enables GitHub Raw URLs)
- Skips R2 upload if not configured
- Runs on push, schedule, and manual trigger

## Configuration Options

### 1. Cloudflare R2 Deployment (Optional)

**Purpose:** Deploy to R2 CDN for faster global access

**Setup:** Configure these repository secrets:

| Secret Name | Required | Description |
|------------|----------|-------------|
| `R2_ACCOUNT_ID` | Yes | Cloudflare Account ID |
| `R2_BUCKET_NAME` | Yes | R2 bucket name |
| `R2_ACCESS_KEY_ID` | Yes | R2 API Access Key |
| `R2_SECRET_ACCESS_KEY` | Yes | R2 API Secret Key |
| `R2_PUBLIC_URL` | No | Public URL for display |

**How to configure:**
1. Go to: Settings → Secrets and variables → Actions → Secrets
2. Click "New repository secret"
3. Add each secret above

**If not configured:** Workflow skips R2 upload (no error)

📖 **Detailed guide:** [R2_SETUP.md](R2_SETUP.md)

---

### 2. Skip Git Commit (Optional)

**Purpose:** Disable committing generated files back to repository

**When to use:**
- ✅ You only use R2 for distribution (not GitHub Raw URLs)
- ✅ You want cleaner git history
- ✅ You want to avoid merge conflicts
- ✅ Generated files are very large

**Default:** Enabled (commits are made)

**How to disable:**
1. Go to: Settings → Secrets and variables → Actions → Variables
2. Click "New repository variable"
3. Name: `SKIP_GIT_COMMIT`
4. Value: `true`
5. Click "Add variable"

**Impact:**
- ❌ GitHub Raw URLs will not work
- ❌ No backup if R2 fails
- ❌ No version history of calendar changes
- ✅ Cleaner git history
- ✅ Slightly faster workflow

**Recommendation:** Keep enabled unless you have a specific reason to disable

---

### 3. Workflow Schedule (Editable)

**Purpose:** Automatic daily calendar updates

**Default:** Daily at 00:00 UTC
```yaml
schedule:
  - cron: '0 0 * * *'
```

**Common alternatives:**

| Schedule | Cron Expression | Use Case |
|----------|----------------|----------|
| Every 6 hours | `0 */6 * * *` | Frequent updates |
| Every 12 hours | `0 */12 * * *` | Twice daily |
| Weekly (Monday) | `0 0 * * 1` | Low activity |
| Disable | Remove `schedule:` | Manual only |

**How to change:**
1. Edit: `.github/workflows/generate-and-deploy.yml`
2. Find the `schedule:` section
3. Modify the cron expression
4. Commit and push

**Tip:** Test cron expressions at [crontab.guru](https://crontab.guru)

---

### 4. Python Version (Editable)

**Default:** Python 3.10

**How to change:**
```yaml
env:
  PYTHON_VERSION: '3.11'  # Change here
```

**Supported versions:** 3.10, 3.11, 3.12

---

### 5. Cache Control Headers (Editable)

**Purpose:** Control how long calendars are cached by clients

**Default:** 1 hour (`max-age=3600`)

**How to change:**
Edit the R2 upload step:
```yaml
--cache-control "max-age=7200, public"  # 2 hours
```

**Common values:**
- `max-age=1800` - 30 minutes (frequent changes)
- `max-age=3600` - 1 hour (default)
- `max-age=7200` - 2 hours (stable content)
- `max-age=86400` - 24 hours (very stable)

**Note:** Most calendar apps check every 24 hours regardless

---

### 6. Artifact Retention (Editable)

**Purpose:** How long to keep workflow artifacts

**Default:** 30 days

**How to change:**
```yaml
- name: Upload artifacts
  uses: actions/upload-artifact@v4
  with:
    retention-days: 90  # Change here
```

**Options:** 1-90 days (GitHub limits)

---

## Distribution Strategy

Choose your distribution method:

### Strategy 1: GitHub Only (Zero Config) 🆓
```yaml
✅ Git commit: Enabled (default)
❌ R2 upload: Not configured
```
**Access:** GitHub Raw URLs only
**Cost:** Free
**Speed:** Good
**Setup:** None required

### Strategy 2: R2 + GitHub Backup (Recommended) ⭐
```yaml
✅ Git commit: Enabled (default)
✅ R2 upload: Configured
```
**Access:** R2 URLs (primary) + GitHub Raw URLs (backup)
**Cost:** ~$0.02/month
**Speed:** Excellent (CDN)
**Setup:** R2 configuration required

### Strategy 3: R2 Only (Advanced) 🚀
```yaml
❌ Git commit: Disabled via SKIP_GIT_COMMIT
✅ R2 upload: Configured
```
**Access:** R2 URLs only
**Cost:** ~$0.02/month
**Speed:** Excellent (CDN)
**Setup:** R2 configuration required
**Note:** No backup if R2 fails

---

## Workflow Permissions

**Required permissions:**
```yaml
permissions:
  contents: write  # For git commit
```

**How to verify:**
1. Go to: Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Select: "Read and write permissions"
4. Click "Save"

**If disabled:** Git commit step will fail (but R2 upload will still work)

---

## Environment-Specific Configuration

### Development/Testing

**Recommended setup:**
- Use a separate R2 bucket (`marathon-calendar-dev`)
- Use a test repository
- Enable all logging
- Shorter artifact retention (7 days)

### Production

**Recommended setup:**
- Use production R2 bucket with custom domain
- Enable branch protection on `main`
- Longer artifact retention (30+ days)
- Monitor workflow runs

---

## Advanced Customization

### Add More Calendar Variants

Edit the generation step:
```yaml
- name: Generate calendar files
  run: |
    python scripts/generate_calendar.py
    python scripts/generate_china_calendar.py
    python scripts/generate_usa_calendar.py      # Add new
    python scripts/generate_europe_calendar.py   # Add new
```

### Conditional R2 Upload (Only if Files Changed)

Add before R2 upload:
```yaml
- name: Check if files changed
  id: check_changes
  run: |
    if git diff --quiet output/; then
      echo "changed=false" >> $GITHUB_OUTPUT
    else
      echo "changed=true" >> $GITHUB_OUTPUT
    fi

- name: Upload to Cloudflare R2
  if: steps.check_changes.outputs.changed == 'true'
  # ... rest of step
```

### Notification on Failure

Add at the end:
```yaml
- name: Notify on failure
  if: failure()
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: 'Workflow failed: ' + context.workflow,
        body: 'Workflow run failed: ' + context.serverUrl + '/' + context.repo.owner + '/' + context.repo.repo + '/actions/runs/' + context.runId
      })
```

---

## Configuration Matrix

| Use Case | Git Commit | R2 Upload | Best For |
|----------|-----------|-----------|----------|
| 🎯 **Personal use** | ✅ Enabled | ❌ No | Simple setup |
| 🌟 **Public sharing (small)** | ✅ Enabled | ❌ No | < 100 subscribers |
| 🚀 **Public sharing (large)** | ✅ Enabled | ✅ Yes | 100+ subscribers |
| ⚡ **High performance** | ❌ Disabled | ✅ Yes | Maximum speed |
| 💾 **Archive/backup** | ✅ Enabled | ✅ Yes | Long-term storage |

---

## Troubleshooting Configuration

### Issue: R2 upload fails but workflow succeeds
**Cause:** `continue-on-error: true` on R2 step
**Solution:** Check R2 secrets are correct

### Issue: Git commit fails
**Cause:** Missing `contents: write` permission
**Solution:** Enable in Settings → Actions → General

### Issue: Workflow doesn't trigger
**Cause:** Path filters don't match changed files
**Solution:** Check paths in workflow trigger section

### Issue: Schedule doesn't run
**Cause:** Repository is private or inactive
**Solution:** Make repository public or make manual commit

---

## Quick Configuration Checklist

**For zero-config setup:**
- [ ] Nothing required - just push events!

**For R2 deployment:**
- [ ] Create R2 bucket
- [ ] Generate API token
- [ ] Add 4 R2 secrets to GitHub
- [ ] Test workflow manually
- [ ] Verify R2 upload in logs

**For production:**
- [ ] Configure R2 with custom domain
- [ ] Enable branch protection
- [ ] Set up monitoring
- [ ] Test calendar subscription
- [ ] Share subscription URLs

---

## Support

- **Configuration questions:** See [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)
- **R2 setup:** See [R2_SETUP.md](R2_SETUP.md)
- **Quick start:** See [QUICK_START.md](QUICK_START.md)
- **Issues:** Open a GitHub Issue

---

**Last updated:** December 23, 2025

