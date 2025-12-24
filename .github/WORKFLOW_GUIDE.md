# GitHub Workflow Guide

This document explains how the GitHub Actions workflow works and how to customize it.

## Workflow Overview

**File:** `.github/workflows/generate-and-deploy.yml`

**Purpose:** Automatically generate calendar files from YAML event data and deploy them to both Cloudflare R2 and GitHub repository.

## Trigger Events

The workflow runs automatically when:

### 1. Push to Main Branch
```yaml
on:
  push:
    branches:
      - main
    paths:
      - 'events/**'
      - 'scripts/**'
      - '.github/workflows/generate-and-deploy.yml'
```

**Triggers when:**
- Any file in `events/` directory is modified
- Any script in `scripts/` directory is modified
- The workflow file itself is modified

### 2. Manual Trigger
```yaml
workflow_dispatch:
```

**How to trigger manually:**
1. Go to Actions tab in GitHub
2. Select "Generate and Deploy Calendar"
3. Click "Run workflow"
4. Choose branch and click "Run"

### 3. Scheduled Run
```yaml
schedule:
  - cron: '0 0 * * *'  # Daily at 00:00 UTC
```

**Runs automatically:**
- Every day at midnight UTC
- Ensures calendar stays updated even without commits

## Workflow Steps

### Step 1: Checkout Repository
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    fetch-depth: 0
```

**Purpose:** Download repository code
**Details:** Full history for better git operations

### Step 2: Set up Python
```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.10'
    cache: 'pip'
```

**Purpose:** Install Python environment
**Features:** Caches pip packages for faster runs

### Step 3: Install Dependencies
```yaml
- name: Install dependencies
  run: |
    pip install --upgrade pip
    pip install -r requirements.txt
```

**Purpose:** Install required Python packages
**Packages:** icalendar, PyYAML, pytz

### Step 4: Generate Calendar Files
```yaml
- name: Generate calendar files
  run: |
    python scripts/generate_calendar.py
    python scripts/generate_china_calendar.py
    ls -lh output/
```

**Purpose:** Create ICS files from YAML data
**Outputs:**
- `output/marathon-calendar.ics` - All events
- `output/china.ics` - China events only

### Step 5: Upload to Cloudflare R2
```yaml
- name: Upload to Cloudflare R2
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.R2_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.R2_SECRET_ACCESS_KEY }}
    R2_ACCOUNT_ID: ${{ secrets.R2_ACCOUNT_ID }}
    R2_BUCKET_NAME: ${{ secrets.R2_BUCKET_NAME }}
```

**Purpose:** Deploy to R2 CDN for fast access
**Features:**
- Uses AWS CLI S3 API (R2 is S3-compatible)
- Sets `content-type: text/calendar`
- Sets `cache-control: max-age=3600`
- Adds generation timestamp metadata

**Graceful Failure:** If R2 secrets are not configured, this step fails but workflow continues

### Step 6: Commit Back to Repository
```yaml
- name: Commit generated files back to repository
  run: |
    git config --local user.email "github-actions[bot]@users.noreply.github.com"
    git config --local user.name "github-actions[bot]"
    git add output/*.ics
    git commit -m "🤖 Auto-generated calendar files [skip ci]"
    git push
```

**Purpose:** Save generated files in git for backup and GitHub raw access
**Details:**
- Uses bot identity for commits
- `[skip ci]` prevents infinite workflow loops
- Only commits if files changed

### Step 7: Generate Deployment Summary
```yaml
- name: Generate deployment summary
  if: always()
```

**Purpose:** Create a summary report in GitHub Actions UI
**Includes:**
- List of generated files and sizes
- Access URLs for R2 and GitHub
- Timestamp of deployment

### Step 8: Upload Artifacts
```yaml
- name: Upload artifacts
  uses: actions/upload-artifact@v4
  with:
    name: calendar-files
    retention-days: 30
```

**Purpose:** Store generated files as workflow artifacts
**Benefits:**
- Download files directly from workflow run
- Keep 30 days of history
- Useful for debugging and manual distribution

## Environment Variables

### Required for R2 Upload

| Variable | Source | Description |
|----------|--------|-------------|
| `AWS_ACCESS_KEY_ID` | `secrets.R2_ACCESS_KEY_ID` | R2 API access key |
| `AWS_SECRET_ACCESS_KEY` | `secrets.R2_SECRET_ACCESS_KEY` | R2 API secret key |
| `R2_ACCOUNT_ID` | `secrets.R2_ACCOUNT_ID` | Cloudflare account ID |
| `R2_BUCKET_NAME` | `secrets.R2_BUCKET_NAME` | R2 bucket name |

### Optional

| Variable | Source | Description |
|----------|--------|-------------|
| `R2_PUBLIC_URL` | `secrets.R2_PUBLIC_URL` | Public access URL |

## Permissions

```yaml
permissions:
  contents: write  # Allow pushing back to repo
```

**Required for:**
- Committing generated files
- Pushing to main branch

## Customization Guide

### Change Python Version
```yaml
env:
  PYTHON_VERSION: '3.11'  # Change here
```

### Adjust Schedule
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  - cron: '0 0 * * 1'    # Every Monday
```

### Add More Calendar Variants

Edit the generation step:
```yaml
- name: Generate calendar files
  run: |
    python scripts/generate_calendar.py
    python scripts/generate_china_calendar.py
    python scripts/generate_usa_calendar.py      # Add this
    python scripts/generate_europe_calendar.py   # Add this
```

### Change Cache Duration

Edit R2 upload step:
```yaml
--cache-control "max-age=7200"  # 2 hours instead of 1
```

### Disable R2 Upload

Comment out or remove the R2 upload step:
```yaml
# - name: Upload to Cloudflare R2
#   env: ...
#   run: ...
```

### Skip Git Commit

Comment out the commit step:
```yaml
# - name: Commit generated files back to repository
#   run: ...
```

## Monitoring and Debugging

### View Workflow Runs
1. Go to "Actions" tab
2. Select a workflow run
3. Expand steps to see detailed logs

### Check Upload Success
Look for these messages in R2 upload step:
```
✅ Uploaded: marathon-calendar.ics
✅ Uploaded: china.ics
🎉 All files uploaded successfully!
```

### Check Commit Success
Look for these messages in commit step:
```
✅ Changes pushed to repository
```

### Download Artifacts
1. Go to workflow run summary page
2. Scroll to "Artifacts" section
3. Click "calendar-files" to download

### Common Issues

#### Issue: R2 Upload Fails
**Symptoms:** "Access Denied" or "NoSuchBucket"
**Solutions:**
- Verify R2 secrets are set correctly
- Check bucket name matches exactly
- Ensure API token has write permissions

#### Issue: Git Push Fails
**Symptoms:** "Permission denied" or "protected branch"
**Solutions:**
- Check workflow has `contents: write` permission
- Verify branch protection rules allow bot commits
- Check if repository is not archived

#### Issue: Calendar Files Empty
**Symptoms:** 0 byte files generated
**Solutions:**
- Check YAML files have valid syntax
- Verify events directory has YAML files
- Look for Python errors in generation step

#### Issue: Workflow Doesn't Trigger
**Symptoms:** No run after push
**Solutions:**
- Check file paths match trigger patterns
- Verify you pushed to `main` branch
- Check Actions is enabled in repository settings

## Best Practices

### 1. Test Locally First
```bash
# Generate calendars
python scripts/generate_calendar.py
python scripts/generate_china_calendar.py

# Verify output
ls -lh output/
```

### 2. Use Branch Protection
Configure in Settings → Branches:
- Require pull request reviews
- Require status checks to pass
- Allow specific actors (github-actions bot)

### 3. Monitor Workflow Runs
- Set up notifications for failures
- Review workflow run history regularly
- Check artifact sizes and counts

### 4. Secure Secrets
- Rotate R2 API tokens regularly
- Use read-only tokens where possible
- Audit secret usage in workflow logs

### 5. Optimize Performance
- Use pip cache (already configured)
- Consider conditional R2 upload (only if files changed)
- Minimize dependencies in requirements.txt

## Advanced Configuration

### Conditional R2 Upload
Only upload if files changed:
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
  # ... rest of upload step
```

### Parallel Calendar Generation
Generate multiple calendars in parallel:
```yaml
- name: Generate calendars
  run: |
    python scripts/generate_calendar.py &
    python scripts/generate_china_calendar.py &
    wait
```

### Multi-Region R2 Buckets
Upload to multiple regions:
```yaml
- name: Upload to R2 (Primary)
  env:
    R2_BUCKET_NAME: ${{ secrets.R2_BUCKET_PRIMARY }}
  run: # ... upload commands

- name: Upload to R2 (Backup)
  env:
    R2_BUCKET_NAME: ${{ secrets.R2_BUCKET_BACKUP }}
  run: # ... upload commands
```

## Support

- **Workflow issues:** Check [GitHub Actions Docs](https://docs.github.com/actions)
- **R2 issues:** Check [R2 Setup Guide](R2_SETUP.md)
- **Python errors:** Check script logs in workflow run
- **General help:** Open an issue in the repository

## Related Documentation

- [R2 Setup Guide](R2_SETUP.md) - Configure Cloudflare R2
- [Deployment Guide](../DEPLOYMENT.md) - Full deployment instructions
- [Contributing Guide](../CONTRIBUTING.md) - How to add events
- [Project README](../README.md) - Project overview

