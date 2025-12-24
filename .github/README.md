# GitHub Actions Documentation

This directory contains all GitHub Actions workflows and related documentation for the Marathon Calendar project.

## 📁 Directory Contents

### Workflows

| File | Purpose |
|------|---------|
| `workflows/generate-and-deploy.yml` | Main CI/CD pipeline - generates calendars and deploys to R2 + GitHub |

### Documentation

| File | Audience | Purpose |
|------|----------|---------|
| `QUICK_START.md` | Users & Admins | Fast setup and subscription guide |
| `R2_SETUP.md` | Repository Owners | Complete Cloudflare R2 configuration guide |
| `WORKFLOW_GUIDE.md` | Developers | Detailed workflow explanation and customization |
| `CONFIGURATION.md` | Admins | All configuration options and settings |
| `CHANGES_SUMMARY.md` | Everyone | Changelog and feature overview |
| `R2_ENV_EXAMPLE.txt` | Developers | Environment variables template |

## 🚀 Quick Links

**Getting Started:**
- 👤 **I want to subscribe** → [QUICK_START.md](QUICK_START.md)
- 🏗️ **I want to deploy** → [R2_SETUP.md](R2_SETUP.md)
- ⚙️ **I want to configure** → [CONFIGURATION.md](CONFIGURATION.md)

**Advanced:**
- 🔧 **Customize workflow** → [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)
- 📊 **See what changed** → [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)

## 🎯 Key Features

### Zero-Configuration Option
The workflow works out-of-the-box:
- ✅ No setup required
- ✅ Generates calendars automatically
- ✅ Commits to GitHub for Raw URL access
- ✅ Perfect for personal use

### Optional R2 CDN Deployment
Add Cloudflare R2 for production use:
- ⚡ Global CDN acceleration
- 💰 Zero egress costs
- 🌍 200+ edge locations
- 🔒 High reliability

## ⚙️ Key Configuration Options

### Git Commit to Repository

**Default:** ✅ Enabled

**Purpose:** Allows GitHub Raw URLs as distribution method

**Disable:** Set repository variable `SKIP_GIT_COMMIT` to `true`

**Recommendation:** Keep enabled for redundancy

### R2 Deployment

**Default:** ❌ Not configured (gracefully skipped)

**Purpose:** Fast global distribution via CDN

**Enable:** Configure 4 R2 secrets (see [R2_SETUP.md](R2_SETUP.md))

**Recommendation:** Enable for public sharing

## 📋 Common Tasks

### Subscribe to Calendar
```
See: QUICK_START.md → Section "For Users"
```

### Set Up R2
```
See: R2_SETUP.md → Complete step-by-step guide
```

### Customize Workflow
```
See: WORKFLOW_GUIDE.md → Customization Guide
```

### Change Settings
```
See: CONFIGURATION.md → All options explained
```

### Add Events
```
Edit: events/YYYY/YYYY-MM.yaml
Then: git commit and push
```

## 🤔 Decision Tree

```
Do you want to deploy the calendar?
│
├─ No → You don't need this folder
│
└─ Yes → Do you need R2 CDN?
    │
    ├─ No (< 100 users) → Default config works!
    │   └─ Access via GitHub Raw URLs
    │
    └─ Yes (100+ users) → Configure R2
        ├─ Read: R2_SETUP.md
        ├─ Configure secrets
        └─ Access via R2 URLs
```

## 🔗 Distribution Methods

### Method 1: GitHub Raw (Default)
```
https://raw.githubusercontent.com/USERNAME/repo/main/output/marathon-calendar.ics
```
- ✅ No configuration needed
- ✅ Free forever
- ⚠️ Slower for global users
- 👥 Good for < 100 subscribers

### Method 2: Cloudflare R2 (Optional)
```
https://your-domain.com/marathon-calendar.ics
```
- ✅ Global CDN acceleration
- ✅ ~$0.02/month cost
- ✅ Faster for all users
- 👥 Good for 100+ subscribers

### Method 3: Both (Recommended)
```
Primary: R2 CDN
Backup: GitHub Raw
```
- ✅ Best reliability
- ✅ Redundancy
- ✅ Minimal cost
- 👥 Professional setup

## 🆘 Getting Help

**Can't find what you need?**
1. Check the relevant documentation file above
2. Search in [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)
3. Open a GitHub Issue
4. Check GitHub Actions logs

**Common issues:**
- Workflow fails → [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md#troubleshooting)
- R2 upload fails → [R2_SETUP.md](R2_SETUP.md#troubleshooting)
- Calendar not updating → [QUICK_START.md](QUICK_START.md#troubleshooting)

## 📊 Project Status

**Current Version:** 2.0.0 (with R2 support)

**Features:**
- ✅ Automatic calendar generation
- ✅ Multiple calendar variants (Global, China)
- ✅ Cloudflare R2 CDN deployment
- ✅ GitHub Actions automation
- ✅ Multiple trigger options
- ✅ Comprehensive documentation

**Upcoming:**
- 🔄 More regional calendars
- 🔄 Web interface
- 🔄 Advanced filtering options

---

**Questions?** Start with [QUICK_START.md](QUICK_START.md) for the fastest path to success!

