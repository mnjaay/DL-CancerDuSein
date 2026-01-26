"""
Configuration du thème et des styles pour l'application
"""

# Palette de couleurs - Thème Clair (Medical Blue)
COLORS = {
    'primary': '#0066CC',
    'secondary': '#00C896',
    'accent': '#FF6B6B',
    'background': '#F8FAFC',
    'surface': '#FFFFFF',
    'text_primary': '#1E293B',
    'text_secondary': '#64748B',
    'border': '#E2E8F0',
    
    # Success/Error
    'success': '#10B981',
    'success_light': '#D1FAE5',
    'error': '#EF4444',
    'error_light': '#FEE2E2',
    'warning': '#F59E0B',
    'warning_light': '#FEF3C7',
    
    # Gradients
    'gradient_primary': 'linear-gradient(135deg, #0066CC 0%, #0052A3 100%)',
    'gradient_success': 'linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%)',
    'gradient_error': 'linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%)',
}

# Thème Sombre (optionnel)
COLORS_DARK = {
    'primary': '#3B82F6',
    'background': '#0F172A',
    'surface': '#1E293B',
    'text_primary': '#F1F5F9',
    'text_secondary': '#94A3B8',
}

# Typography
FONTS = {
    'heading': "'Inter', sans-serif",
    'body': "'Inter', sans-serif",
    'mono': "'Fira Code', monospace",
}

# Spacing
SPACING = {
    'xs': '0.25rem',
    'sm': '0.5rem',
    'md': '1rem',
    'lg': '1.5rem',
    'xl': '2rem',
    'xxl': '3rem',
}

# Border Radius
RADIUS = {
    'sm': '8px',
    'md': '12px',
    'lg': '16px',
    'full': '9999px',
}

# Shadows
SHADOWS = {
    'sm': '0 2px 8px rgba(0, 0, 0, 0.08)',
    'md': '0 4px 16px rgba(0, 0, 0, 0.12)',
    'lg': '0 8px 32px rgba(0, 0, 0, 0.16)',
    'xl': '0 20px 48px rgba(0, 0, 0, 0.20)',
}

# Animation durations
TRANSITIONS = {
    'fast': '0.15s',
    'normal': '0.3s',
    'slow': '0.5s',
}

# Custom CSS
CUSTOM_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Reset & Base */
    * {{
        font-family: 'Inter', sans-serif !important;
    }}
    
    .main {{
        background: {COLORS['background']};
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Variables CSS */
    :root {{
        --primary: {COLORS['primary']};
        --secondary: {COLORS['secondary']};
        --accent: {COLORS['accent']};
        --background: {COLORS['background']};
        --surface: {COLORS['surface']};
        --text-primary: {COLORS['text_primary']};
        --text-secondary: {COLORS['text_secondary']};
        --border: {COLORS['border']};
        --success: {COLORS['success']};
        --error: {COLORS['error']};
        
        --radius-md: {RADIUS['md']};
        --shadow-sm: {SHADOWS['sm']};
        --shadow-md: {SHADOWS['md']};
        --shadow-lg: {SHADOWS['lg']};
    }}
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: white;
        padding: 0.5rem;
        border-radius: {RADIUS['md']};
        box-shadow: {SHADOWS['sm']};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        background: transparent;
        border-radius: {RADIUS['sm']};
        color: {COLORS['text_secondary']};
        font-weight: 600;
        padding: 0 1.5rem;
        transition: all {TRANSITIONS['normal']} ease;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {COLORS['primary']} !important;
        color: white !important;
        box-shadow: {SHADOWS['sm']};
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: {COLORS['background']};
    }}
    
    /* Buttons */
    .stButton > button {{
        background: {COLORS['primary']};
        color: white;
        border: none;
        border-radius: {RADIUS['md']};
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all {TRANSITIONS['normal']} ease;
        box-shadow: {SHADOWS['sm']};
    }}
    
    .stButton > button:hover {{
        background: #0052A3;
        transform: translateY(-2px);
        box-shadow: {SHADOWS['md']};
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* File Uploader */
    .uploadedFile {{
        background: white;
        border-radius: {RADIUS['md']};
        box-shadow: {SHADOWS['sm']};
        padding: 1rem;
    }}
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {{
        border-radius: {RADIUS['sm']};
        border: 2px solid {COLORS['border']};
        padding: 0.75rem;
        font-size: 1rem;
        transition: all {TRANSITIONS['normal']} ease;
    }}
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div > input:focus {{
        border-color: {COLORS['primary']};
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
    }}
    
    /* Sidebar */
    .css-1d391kg {{
        background: white;
        border-right: 1px solid {COLORS['border']};
    }}
    
    /* Metrics */
    [data-testid="stMetricValue"] {{
        font-size: 2rem;
        font-weight: 700;
        color: {COLORS['primary']};
    }}
    
    /* Success/Error Messages */
    .stSuccess {{
        background: {COLORS['success_light']};
        border-left: 4px solid {COLORS['success']};
        border-radius: {RADIUS['md']};
        padding: 1rem;
    }}
    
    .stError {{
        background: {COLORS['error_light']};
        border-left: 4px solid {COLORS['error']};
        border-radius: {RADIUS['md']};
        padding: 1rem;
    }}
    
    .stWarning {{
        background: {COLORS['warning_light']};
        border-left: 4px solid {COLORS['warning']};
        border-radius: {RADIUS['md']};
        padding: 1rem;
    }}
    
    /* Animations */
    @keyframes fadeIn {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{
            transform: scale(1);
        }}
        50% {{
            transform: scale(1.05);
        }}
    }}
    
    @keyframes spin {{
        to {{
            transform: rotate(360deg);
        }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.5s ease-out;
    }}
    
    /* Glass Card */
    .glass-card {{
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: {RADIUS['md']};
        box-shadow: {SHADOWS['md']};
        padding: 2rem;
        transition: all {TRANSITIONS['normal']} ease;
    }}
    
    .glass-card:hover {{
        transform: translateY(-4px);
        box-shadow: {SHADOWS['lg']};
    }}
    
    /* Result Cards */
    .result-positive {{
        background: {COLORS['gradient_error']};
        border-left: 6px solid {COLORS['error']};
        padding: 2rem;
        border-radius: {RADIUS['md']};
        animation: fadeIn 0.5s ease;
        box-shadow: {SHADOWS['md']};
    }}
    
    .result-negative {{
        background: {COLORS['gradient_success']};
        border-left: 6px solid {COLORS['success']};
        padding: 2rem;
        border-radius: {RADIUS['md']};
        animation: fadeIn 0.5s ease;
        box-shadow: {SHADOWS['md']};
    }}
    
    /* Metric Cards */
    .metric-card {{
        background: white;
        border-radius: {RADIUS['md']};
        padding: 1.5rem;
        box-shadow: {SHADOWS['sm']};
        transition: all {TRANSITIONS['normal']} ease;
        border: 1px solid {COLORS['border']};
    }}
    
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: {SHADOWS['md']};
        border-color: {COLORS['primary']};
    }}
    
    /* Loading Spinner */
    .spinner {{
        border: 4px solid rgba(0, 102, 204, 0.1);
        border-left-color: {COLORS['primary']};
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }}
    
    /* Upload Zone */
    .upload-zone {{
        border: 3px dashed {COLORS['border']};
        border-radius: {RADIUS['lg']};
        padding: 3rem 2rem;
        text-align: center;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        cursor: pointer;
        transition: all {TRANSITIONS['normal']} ease;
    }}
    
    .upload-zone:hover {{
        border-color: {COLORS['primary']};
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        transform: scale(1.01);
    }}
    
    /* Image Info Box */
    .image-info {{
        background: {COLORS['background']};
        padding: 1rem;
        border-radius: {RADIUS['sm']};
        margin-top: 1rem;
        border: 1px solid {COLORS['border']};
    }}
    
    /* Recommendation Box */
    .recommendation-box {{
        padding: 1.5rem;
        border-radius: {RADIUS['md']};
        margin-top: 2rem;
        border-left: 4px solid;
    }}
    
    .recommendation-positive {{
        background: {COLORS['error_light']};
        border-color: {COLORS['error']};
    }}
    
    .recommendation-negative {{
        background: {COLORS['success_light']};
        border-color: {COLORS['success']};
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {COLORS['background']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {COLORS['border']};
        border-radius: {RADIUS['full']};
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS['text_secondary']};
    }}
</style>
"""
