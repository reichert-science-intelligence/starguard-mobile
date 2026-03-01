"""Mobile-optimized theme configuration for StarGuard AI."""

from shinyswatch import theme

# Mobile-first CSS overrides
MOBILE_CSS = """
<style>
/* Base mobile styles */
* {
    box-sizing: border-box;
    -webkit-font-smoothing: antialiased;
}

body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    font-size: 16px;  /* Prevents iOS zoom on input focus */
}

/* Container optimizations */
.container-fluid {
    padding: 0.5rem;
    max-width: 100vw;
    overflow-x: hidden;
}

/* Touch-friendly buttons */
.btn {
    min-height: 44px;  /* iOS touch target minimum */
    min-width: 44px;
    font-size: 16px;
    padding: 0.75rem 1.5rem;
    margin: 0.5rem 0;
}

/* ==================== BUTTON ANIMATIONS ==================== */
.btn-primary, .btn-secondary {
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.btn-primary:hover, .btn-secondary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
}

.btn-primary:active, .btn-secondary:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(124, 58, 237, 0.2);
}

/* Ripple effect */
.btn-primary::after, .btn-secondary::after {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.4);
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

.btn-primary:active::after, .btn-secondary:active::after {
    width: 300px;
    height: 300px;
}

/* Pulse animation for primary action buttons */
@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
}

.btn-primary {
    animation: pulse 2s infinite;
}

.btn-primary:hover {
    animation: none;
}

/* Specific animations for action buttons */
button[id*="execute_btn"],
button[id*="contact_btn"],
button[id*="assign_btn"],
button[id*="history_btn"] {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

button[id*="execute_btn"]:hover,
button[id*="contact_btn"]:hover,
button[id*="assign_btn"]:hover,
button[id*="history_btn"]:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 6px 16px rgba(124, 58, 237, 0.5);
}

/* Mobile navigation */
.navbar {
    position: sticky;
    top: 0;
    z-index: 1000;
    background: #7c3aed;
    padding: 0.75rem;
}

.nav-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: white;
    margin: 0;
}

/* Card layouts */
.card {
    margin-bottom: 1rem;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border: none;
}

.card-header {
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    color: white;
    font-weight: 600;
    padding: 1rem;
    border-radius: 12px 12px 0 0;
}

.card-body {
    padding: 1rem;
}

/* Form inputs */
input, select, textarea {
    font-size: 16px !important;  /* Prevents iOS zoom */
    padding: 0.75rem;
    border-radius: 8px;
    border: 2px solid #e0e0e0;
    width: 100%;
    margin-bottom: 1rem;
}

input:focus, select:focus, textarea:focus {
    outline: none;
    border-color: #7c3aed;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15);
}

/* Charts responsive */
.plotly {
    width: 100%;
    height: 300px;
}

/* Loading states */
.shiny-busy {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

/* Responsive breakpoints */
@media (min-width: 768px) {
    .container-fluid {
        padding: 1.5rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .plotly {
        height: 400px;
    }
}

/* ==================== DARK MODE SUPPORT ==================== */
@media (prefers-color-scheme: dark) {
    body {
        background-color: #1a1a1a;
        color: #e0e0e0;
    }
    
    .card {
        background-color: #2a2a2a;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        color: #e0e0e0;
    }
    
    .card-body {
        color: #e0e0e0;
    }
    
    /* Fix all text in cards to be white in dark mode */
    .card h1, .card h2, .card h3, .card h4, .card h5, .card h6,
    .card p, .card span, .card div, .card li, .card td, .card th {
        color: #e0e0e0 !important;
    }
    
    /* Keep specific colored elements */
    .card-header {
        color: white !important;
    }
    
    input, select, textarea {
        background-color: #333;
        color: #e0e0e0;
        border-color: #444;
    }
    
    .nav-tabs-container {
        background: #2a2a2a;
        border-bottom-color: #444;
    }
    
    .shiny-input-radiogroup label span {
        background: #333;
        color: #e0e0e0;
    }
    
    /* Metric boxes and info rows */
    .metric-box, [style*="background: #f8f9fa"] {
        background: #333 !important;
        color: #e0e0e0 !important;
    }
    
    /* Strong tags in dark mode */
    strong {
        color: #e0e0e0;
    }
    
    /* Text color fixes */
    .text-muted {
        color: #999 !important;
    }
    
    /* Alert boxes in dark mode */
    .alert-box, [style*="border-left: 4px solid"] {
        background: #2a2a2a !important;
    }
    
    /* Info rows and scenario details in dark mode */
    [style*="border-bottom: 1px solid #e0e0e0"] {
        border-bottom-color: #444 !important;
    }
    
    [style*="background: #f5f3ff"] {
        background: #4c1d95 !important;
    }
    
    /* Self-correction event text in dark mode */
    [style*="background: #fff8f0"] span {
        color: #e0e0e0 !important;
    }
    
    /* ROI Scenario cards in dark mode */
    .scenario-card {
        background: #2a2a2a !important;
        border-color: #444 !important;
    }
    
    .scenario-label {
        color: #b0b0b0 !important;
    }
    
    .scenario-value {
        color: #e0e0e0 !important;
    }
    
    .scenario-subtitle {
        color: #999 !important;
    }
    
    .scenario-revenue {
        color: #4ade80 !important;
    }
    
    .scenario-revenue-box {
        background: #1a3a2a !important;
    }
    
    .scenario-highlight {
        background: #4c1d95 !important;
    }
    
    .scenario-detail {
        border-bottom-color: #444 !important;
    }
    
    /* Risk Stratification cards in dark mode */
    .risk-category-card, .segment-card {
        background: #2a2a2a !important;
        border-color: #444 !important;
    }
    
    .risk-label, .hcc-label, .segment-label, .opp-label {
        color: #b0b0b0 !important;
    }
    
    .risk-value, .hcc-value, .segment-value, .opp-value {
        color: #e0e0e0 !important;
    }
    
    /* HCC category cards - bright text for dark backgrounds */
    .hcc-category-card {
        background: #2a2a2a !important;
        border-left-color: #8b5cf6 !important;
    }
    
    .hcc-code {
        color: #f0f0f0 !important;
    }
    
    .hcc-name {
        color: #d0d0d0 !important;
    }
    
    .hcc-metric-label {
        color: #c0c0c0 !important;
    }
    
    .hcc-metric-value {
        color: #e0e0e0 !important;
    }
    
    .hcc-prevalence {
        color: #a78bfa !important;
    }
    
    .hcc-category-card [style*="color: #7c3aed"] {
        color: #a78bfa !important;
    }
    
    .hcc-category-card [style*="color: #28a745"] {
        color: #4ade80 !important;
    }
    
    .hcc-category-card [style*="color: #1a1a1a"] {
        color: #e0e0e0 !important;
    }
    
    /* Detailed HCC Analysis title - bright in dark mode */
    .hcc-detailed-title {
        color: #f0f0f0 !important;
        border-bottom-color: #8b5cf6 !important;
    }
    
    /* Detailed HCC tiles STAY WHITE even in dark mode */
    .hcc-detailed-tile {
        background: white !important;
        border-color: #e0e0e0 !important;
    }
    
    /* Force ALL text in detailed tiles to be DARK (since bg is white) */
    .hcc-detailed-tile,
    .hcc-detailed-tile h4,
    .hcc-detailed-tile strong,
    .hcc-detailed-tile span {
        color: #1a1a1a !important;
    }
    
    /* Accent colors stay visible in detailed tiles */
    .hcc-detailed-tile [style*="color: #7c3aed"] {
        color: #7c3aed !important;
    }
    
    .hcc-detailed-tile [style*="color: #28a745"] {
        color: #28a745 !important;
    }
    
    /* Opportunity cards in dark mode */
    .opportunity-card {
        background: #2a2a2a !important;
        border-color: #444 !important;
    }
    
    .opportunity-card strong {
        color: #b0b0b0 !important;
    }
    
    .opportunity-card span {
        color: #e0e0e0 !important;
    }
    
    /* ROI Portfolio Optimizer in dark mode */
    .scenario-row {
        background: #2a2a2a !important;
        border-left-color: #8b5cf6 !important;
    }

    /* Care Gap Workflow cards in dark mode */
    .member-card {
        background: #2a2a2a !important;
    }

    .member-card strong {
        color: #b0b0b0 !important;
    }

    .member-card span {
        color: #e0e0e0 !important;
    }

    /* Intervention & campaign cards stay white with dark text in dark mode */
    .intervention-card,
    .campaign-card {
        background: white !important;
        border-color: #e0e0e0 !important;
    }

    .intervention-card h4,
    .intervention-card strong,
    .campaign-card h4,
    .campaign-card strong {
        color: #1a1a1a !important;
    }

    /* Force pure black on data value spans (override any card/div span rules) */
    .intervention-card span,
    .campaign-card span {
        color: #000000 !important;
    }

    /* Executive Dashboard - opportunity cards stay white with dark text */
    .opportunity-card {
        background: white !important;
        border-color: #e0e0e0 !important;
    }

    .opportunity-card strong {
        color: #1a1a1a !important;
    }

    .opportunity-card span {
        color: #000000 !important;
    }

    /* Provider Scorecard cards in dark mode - keep white with dark text */
    .provider-card {
        background: white !important;
        border-color: #e0e0e0 !important;
    }

    .provider-card strong,
    .provider-card span,
    .provider-card h4 {
        color: #1a1a1a !important;
    }

    .provider-card [style*="color: #666"] {
        color: #666 !important;
    }

    .provider-card [style*="color: #7c3aed"] {
        color: #7c3aed !important;
    }

    /* Model Monitor cards in dark mode - keep white with dark text */
    .model-component-card {
        background: white !important;
        border-color: #e0e0e0 !important;
    }

    .model-component-card strong,
    .model-component-card span {
        color: #1a1a1a !important;
    }

    .model-component-card [style*="color: #7c3aed"] {
        color: #7c3aed !important;
    }

    .model-component-card [style*="color: #666"] {
        color: #666 !important;
    }

    /* Member Profile cards in dark mode - keep white with dark text */
    .member-profile-card {
        background: white !important;
        border-color: #e0e0e0 !important;
    }

    .member-profile-card strong,
    .member-profile-card span,
    .member-profile-card h4 {
        color: #1a1a1a !important;
    }

    .member-profile-card [style*="color: #7c3aed"] {
        color: #7c3aed !important;
    }

    .member-profile-card [style*="color: #666"] {
        color: #666 !important;
    }
}

/* ==================== HAMBURGER MENU & SIDEBAR ==================== */
.menu-toggle {
    position: fixed;
    top: 1rem;
    right: 1rem;
    z-index: 2000;
    background: white;
    border: 2px solid #7c3aed;
    border-radius: 8px;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
}

.menu-toggle:hover {
    background: #f5f3ff;
    transform: scale(1.05);
}

.menu-toggle:active {
    transform: scale(0.95);
}

.hamburger-icon {
    width: 24px;
    height: 20px;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.hamburger-icon span {
    display: block;
    height: 3px;
    width: 100%;
    background: #7c3aed;
    border-radius: 3px;
    transition: all 0.3s ease;
}

.menu-toggle.active .hamburger-icon span:nth-child(1) {
    transform: translateY(8.5px) rotate(45deg);
}

.menu-toggle.active .hamburger-icon span:nth-child(2) {
    opacity: 0;
}

.menu-toggle.active .hamburger-icon span:nth-child(3) {
    transform: translateY(-8.5px) rotate(-45deg);
}

/* Sidebar overlay */
.sidebar-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1500;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s ease, visibility 0.3s ease;
}

.sidebar-overlay.active {
    opacity: 1;
    visibility: visible;
}

/* Sidebar */
.nav-sidebar {
    position: fixed;
    top: 0;
    right: -280px;
    width: 280px;
    height: 100%;
    background: white;
    z-index: 1600;
    box-shadow: -4px 0 16px rgba(0,0,0,0.2);
    transition: right 0.3s ease;
    overflow-y: auto;
}

.nav-sidebar.active {
    right: 0;
}

.sidebar-header {
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    color: white;
    padding: 1.5rem;
    position: sticky;
    top: 0;
    z-index: 10;
}

.sidebar-header h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 700;
}

.sidebar-header p {
    margin: 0.25rem 0 0 0;
    font-size: 0.875rem;
    opacity: 0.9;
}

.sidebar-nav {
    padding: 1rem 0;
}

.sidebar-nav-item {
    display: block;
    padding: 1rem 1.5rem;
    color: #333;
    text-decoration: none;
    font-weight: 600;
    font-size: 1rem;
    border-left: 4px solid transparent;
    transition: all 0.2s ease;
    cursor: pointer;
}

.sidebar-nav-item:hover {
    background: #f5f3ff;
    border-left-color: #7c3aed;
}

.sidebar-nav-item.active {
    background: #ede9fe;
    border-left-color: #7c3aed;
    color: #7c3aed;
}

/* Hide old navigation tabs container on mobile */
.nav-tabs-container {
    display: none;
}

/* Adjust navbar for hamburger menu */
.navbar {
    padding-right: 60px; /* Space for hamburger button */
}

/* Desktop: show tabs, hide hamburger */
@media (min-width: 768px) {
    .menu-toggle {
        display: none;
    }
    
    .nav-tabs-container {
        display: block;
    }
    
    .nav-sidebar {
        display: none;
    }
}

/* ==================== iPHONE OPTIMIZATIONS ==================== */

/* Prevent number wrapping on iPhone */
@supports (-webkit-touch-callout: none) {
    /* iPhone-specific styles */
    
    /* Force 7+ digit numbers to stay on single line */
    span[style*="font-size: 1.5rem"],
    span[style*="font-size: 1.25rem"],
    span[style*="font-size: 1.75rem"],
    span[style*="font-size: 2rem"] {
        white-space: nowrap !important;
        display: inline-block !important;
        max-width: 100%;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
    
    /* Smaller font size for very long numbers on iPhone */
    span[style*="font-size: 2rem"] {
        font-size: 1.75rem !important;
    }
    
    span[style*="font-size: 1.75rem"] {
        font-size: 1.5rem !important;
    }
}

/* iPhone Safari text rendering */
@media only screen and (max-width: 430px) {
    /* iPhone 14 Pro Max and smaller */
    
    /* Force single-line for large numbers */
    .metric-value,
    span[style*="font-weight: 900"],
    span[style*="font-weight: 700"] {
        white-space: nowrap !important;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
}

/* ==================== CONTRAST FIXES FOR ALL PLATFORMS ==================== */

/* Dark backgrounds - lighten text */
div[style*="background: #2a2a2a"] span,
div[style*="background: #f8f9fa"] span,
div[style*="background: #f5f3ff"] span,
.hcc-category-card span,
.risk-category-card span,
.segment-card span,
.opportunity-card span {
    color: #666 !important;
}

/* Purple/colored backgrounds - lighten text */
div[style*="background: #f5f3ff"] strong,
div[style*="background: #f5f3ff"] span,
div[style*="background: #f0f7f0"] strong,
div[style*="background: #f0f7f0"] span,
div[style*="background: #fff8f0"] strong,
div[style*="background: #fff8f0"] span {
    color: #666 !important;
}

/* White backgrounds - darken text */
div[style*="background: white"] h4,
div[style*="background: white"] .hcc-code,
div[style*="background: white"] .hcc-name {
    color: #1a1a1a !important;
}

/* Force proper contrast on white tiles */
.hcc-detailed-tile *,
.intervention-card *,
.campaign-card *,
.opportunity-card *,
.model-component-card *,
.provider-card * {
    color: #1a1a1a !important;
}

/* Exception: keep metric values visible */
.hcc-detailed-tile span[style*="font-size: 1"],
.intervention-card span[style*="font-size: 1"],
.campaign-card span[style*="font-size: 1"],
.opportunity-card span[style*="font-size: 1"],
.model-component-card span[style*="font-size: 1"],
.provider-card span[style*="font-size: 1"] {
    color: #000000 !important;
}

/* Metric boxes - ensure readability */
.metric-box {
    white-space: nowrap;
}

.metric-box .metric-value {
    white-space: nowrap !important;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}

/* ==================== iPHONE SAFE AREA ==================== */

@supports (padding: max(0px)) {
    /* iPhone notch/safe area support */
    body {
        padding-left: env(safe-area-inset-left);
        padding-right: env(safe-area-inset-right);
        padding-bottom: env(safe-area-inset-bottom);
    }
    
    .navbar {
        padding-top: max(1rem, env(safe-area-inset-top));
    }
}

/* ==================== iPHONE TOUCH OPTIMIZATIONS ==================== */

/* Larger touch targets for iPhone */
@media (hover: none) and (pointer: coarse) {
    button,
    .btn-primary,
    .btn-secondary,
    .sidebar-nav-item {
        min-height: 44px !important; /* Apple's recommended minimum */
        padding: 0.75rem 1.5rem !important;
    }
    
    /* Prevent text selection on buttons */
    button,
    .btn-primary,
    .btn-secondary {
        -webkit-user-select: none;
        user-select: none;
        -webkit-tap-highlight-color: transparent;
    }
}

/* ==================== iPHONE SCROLLING ==================== */

/* Smooth scrolling on iPhone */
.sidebar,
.main-content {
    -webkit-overflow-scrolling: touch;
}

/* Prevent bounce scroll on body */
body {
    overscroll-behavior-y: none;
}
</style>
"""

# Meta tags for mobile optimization
MOBILE_META_TAGS = """
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#7c3aed">
"""


def get_theme():
    """Return mobile-optimized theme."""
    return theme.flatly


def get_mobile_css():
    """Return mobile CSS string for head injection."""
    return MOBILE_CSS


def get_mobile_meta():
    """Return mobile meta tags string for head injection."""
    return MOBILE_META_TAGS
