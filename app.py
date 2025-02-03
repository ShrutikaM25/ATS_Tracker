import streamlit as st
import ats_tracker
import career_roadmap
import market_analysis

st.set_page_config(page_title="Career Hub AI", layout="wide")

# Enhanced CSS for a Modern UI
st.markdown("""
    <style>
        /* Global Styles */
        body {
            background: linear-gradient(135deg, #0D1117, #1A1F25);
            color: white;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }
        
        /* Main Title Styling */
        .main-title {
            text-align: center;
            font-size: 52px;
            font-weight: 800;
            background: linear-gradient(120deg, #6E45E2, #88D3CE, #6E45E2);
            background-size: 200% auto;
            color: transparent;
            background-clip: text;
            -webkit-background-clip: text;
            animation: gradient 3s ease infinite;
            margin: 40px 0 20px;
        }
        
        /* Subtitle Enhancement */
        .sub-title {
            text-align: center;
            font-size: 22px;
            color: #A0AEC0;
            margin-bottom: 40px;
            font-weight: 400;
            letter-spacing: 0.5px;
        }
        
        /* Feature Cards */
        .feature-card {
            padding: 30px;
            margin-bottom: 10px;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .feature-card:hover {
            transform: translateY(-8px);
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 12px 48px rgba(110, 69, 226, 0.2);
        }
        
        /* Button Styling */
        .feature-button {
            background: linear-gradient(135deg, #6E45E2, #88D3CE);
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            display: block;
            width: 100%;
            margin-top: 20px;
        }
        
        .feature-button:hover {
            background: linear-gradient(135deg, #88D3CE, #6E45E2);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(110, 69, 226, 0.3);
        }
        
        /* Card Icons */
        .feature-icon {
            font-size: 60px;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #6E45E2, #88D3CE);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: white;
        }
        
        /* Card Title */
        .feature-title {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 16px;
            color: #FFFFFF;
        }
        
        /* Card Description */
        .feature-description {
            font-size: 16px;
            color: #A0AEC0;
            line-height: 1.6;
            margin-bottom: 20px;
        }
        
        /* Footer Enhancement */
        .footer {
            text-align: center;
            font-size: 14px;
            color: #A0AEC0;
            padding: 20px;
            margin-top: 40px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Animations */
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="main-title">Career Hub AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Elevate Your Career Journey with AI-Powered Insights</div>', unsafe_allow_html=True)

# Navigation State
if "page" not in st.session_state:
    st.session_state.page = "home"

# Home Page
if st.session_state.page == "home":
    st.markdown("### 🎯 Transform Your Career Path")

    col1, col2 = st.columns([3, 1])  # Adjusting column width to align button right
    with col2:
        if st.button("Begin Your Journey", key="get_started", help="Explore our AI-powered career tools"):
            st.session_state.page = "features"

    st.write("Leverage AI-driven tools to optimize your career decisions and maximize your potential.")


# Features Page
elif st.session_state.page == "features":
    st.markdown("## Discover Your Career Tools")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="feature-card">
                <div>
                    <div class="feature-icon">📑</div>
                    <div class="feature-title">ATS Tracker</div>
                    <div class="feature-description">
                        Advanced resume optimization using AI to maximize your application success rate. Get detailed insights and recommendations.
                    </div>
                </div>
        """, unsafe_allow_html=True)
        if st.button("Optimize Resume", key="ats_tracker", help="Optimize your resume for ATS"):
            st.session_state.page = "ats_tracker"
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="feature-card">
                <div>
                    <div class="feature-icon">🧭</div>
                    <div class="feature-title">Career Roadmap</div>
                    <div class="feature-description">
                        Personalized career progression planning with AI insights. Map your journey and identify growth opportunities.
                    </div>
                </div>
        """, unsafe_allow_html=True)
        if st.button("Plan Your Path", key="career_roadmap", help="Plan your career path with AI insights"):
            st.session_state.page = "career_roadmap"
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="feature-card">
                <div>
                    <div class="feature-icon">📊</div>
                    <div class="feature-title">Market Analysis</div>
                    <div class="feature-description">
                        Real-time industry insights and salary benchmarks to help you make informed career decisions.
                    </div>
                </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Trends", key="market_analysis", help="Stay updated with job trends & salary insights"):
            st.session_state.page = "market_analysis"
        st.markdown("</div>", unsafe_allow_html=True)

# Page Navigation
elif st.session_state.page == "ats_tracker":
    ats_tracker.main()
elif st.session_state.page == "career_roadmap":
    career_roadmap.main()
elif st.session_state.page == "market_analysis":
    market_analysis.main()

# Enhanced Footer
st.markdown("""
    <div class="footer">
        <div>💼 Powered by Advanced AI Technology</div>
        <div style="margin-top: 8px;">© 2025 Career Hub AI - Empowering Career Growth</div>
    </div>
""", unsafe_allow_html=True)