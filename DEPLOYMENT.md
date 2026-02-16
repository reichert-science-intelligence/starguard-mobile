# StarGuard AI - Deployment Reference

## 🚀 Live Deployments

### Mobile Version (starguard-mobile)

**Primary Deployment - Hugging Face Spaces:**
- URL: https://rreichert-starguardai.hf.space
- Status: Always-On
- Platform: Hugging Face Spaces
- Deployment: Automatic from git push

**Backup Deployment - Render.com:**
- URL: https://starguard-mobile.onrender.com
- Status: Free tier (sleeps after 15 min)
- Platform: Render.com
- Deployment: Automatic from GitHub

**Source Code:**
- GitHub: https://github.com/reichert-science-intelligence/starguard-mobile
- Organization: https://github.com/StarGuardAi/starguard-mobile (mirror)

---

## 📱 Mobile App Features

**10 Pages:**
1. Executive Dashboard - Strategic KPIs
2. Star Rating Predictor - CMS Quality
3. HEDIS Gap Analyzer - Quality Measures
4. Member Risk Stratification - HCC V28
5. ROI Portfolio Optimizer - Financial Planning
6. Care Gap Closure Workflow - Operations
7. Provider Scorecard - Network Analytics
8. Member 360° Profile - Integration Showcase
9. AI Validation Dashboard - Compliance
10. Model Monitor - ML Performance

**Tech Stack:**
- Python 3.11
- Shiny for Python 0.10.2
- Docker deployment
- Mobile-first responsive design
- Purple theme with dark mode

---

## 🔄 Deployment Commands

### Push to Hugging Face:
```bash
cd C:\Users\reich\Projects\starguard-mobile-standalone
git push hf main
```

### Push to GitHub (auto-deploys to Render):
```bash
git push personal main
# or
git push origin main
```

### Update all remotes:
```bash
git push --all
```

---

## 📊 Portfolio Links

**Live Demos:**
- Mobile (Primary): https://rreichert-starguardai.hf.space
- Mobile (Backup): https://starguard-mobile.onrender.com

**Source Code:**
- Mobile: https://github.com/reichert-science-intelligence/starguard-mobile

**LinkedIn:**
- Profile: https://linkedin.com/in/robertreichert-healthcareai

**Contact:**
- Email: reichert.starguardai@gmail.com
- Landing Page: tinyurl.com/bdevpdz5

---

## 📝 Quick Copy/Paste

**For Cursor AI:**
```
Mobile Demo: https://rreichert-starguardai.hf.space
GitHub: https://github.com/reichert-science-intelligence/starguard-mobile
```

**For LinkedIn:**
```
🚀 Live Demo: https://rreichert-starguardai.hf.space
```

**For Resume:**
```
StarGuard AI - Medicare Advantage Intelligence Platform
Live: https://rreichert-starguardai.hf.space
Code: https://github.com/reichert-science-intelligence/starguard-mobile
```

---

## 🎯 Deployment Status

- [x] Mobile version deployed to Hugging Face
- [x] Mobile version deployed to Render
- [x] Desktop version prepared (starguard-desktop-standalone) - create GitHub/HF repos then push

Last Updated: February 15, 2026

---

## 🖥️ Desktop Version (starguard-desktop)

**Standalone repo:** `C:\Users\reich\Projects\starguard-desktop-standalone`

**To deploy:**
1. Create GitHub repo: https://github.com/new → `reichert-science-intelligence/starguard-desktop`
2. Create HF Space: https://huggingface.co/new-space → `rreichert/StarGuardAI-Desktop` (SDK: Streamlit)
3. Push: `git push -u origin main` then `git push hf main`
