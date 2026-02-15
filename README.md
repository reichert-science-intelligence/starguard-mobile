---
title: StarGuard AI - Medicare Advantage Intelligence Platform
emoji: ⭐
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 8000
pinned: false
---

# StarGuard AI - Mobile Intelligence Platform

**Complete Medicare Advantage analytics and AI system** - 10-page mobile-optimized application showcasing:

- Executive Dashboard & Star Rating Predictions
- HEDIS Gap Analysis & Member Risk Stratification
- ROI Portfolio Optimization & Care Gap Workflow
- Provider Performance Scorecards
- Member 360° Profiles with AI Recommendations
- ML Model Performance Monitoring

**Tech Stack:** Python 3.11, Shiny for Python, Mobile-first responsive design

**Live Demo:** Fully functional on mobile and desktop devices

---

# StarGuard AI Mobile Companion App

Medicare Advantage analytics platform for portfolio/consulting launch.

**Target Completion:** 6 weeks (February–March 2026)  
**Owner:** Robert Reichert  
**Version:** 1.0

## Setup

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

## Run

```bash
# From starguard-mobile directory (with venv activated):
shiny run app.app --port 8000

# Or use the run script:
shiny run run:app --port 8000
```

## Project Structure

```
starguard-mobile/
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── pages/
│   ├── components/
│   ├── utils/
│   ├── assets/
│   └── data/
├── tests/
├── docs/
├── requirements.txt
└── README.md
```
