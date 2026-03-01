def load_css():
    """Load custom CSS styles"""
    
    st.markdown("""
    <style>
        /* Main container */
        .main {
            padding: 0rem 1rem;
        }
        
        /* Headers */
        h1 {
            color: #1E88E5;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        h2 {
            color: #0D47A1;
            font-weight: 500;
            margin-top: 1rem;
        }
        
        /* Buttons */
        .stButton > button {
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Primary button */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #1E88E5 0%, #0D47A1 100%);
            color: white;
        }
        
        /* File uploader */
        .stFileUploader {
            border: 2px dashed #1E88E5;
            border-radius: 10px;
            padding: 1rem;
            background: rgba(30, 136, 229, 0.05);
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background: linear-gradient(90deg, #1E88E5, #64B5F6);
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #f0f2f6;
            border-radius: 8px;
            font-weight: 500;
        }
        
        /* Metrics */
        .stMetric {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stMetric label {
            color: #1E88E5;
            font-weight: 500;
        }
        
        /* Success/Info/Warning boxes */
        .stAlert {
            border-radius: 8px;
            border-left-width: 4px;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        }
        
        /* Text area */
        .stTextArea textarea {
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            transition: all 0.3s;
        }
        
        .stTextArea textarea:focus {
            border-color: #1E88E5;
            box-shadow: 0 0 0 2px rgba(30, 136, 229, 0.2);
        }
        
        /* Cards for results */
        .result-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 1rem 0;
            border-left: 4px solid #1E88E5;
        }
        
        /* Confidence badges */
        .badge-high {
            background: #4CAF50;
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 12px;
            font-size: 0.8rem;
        }
        
        .badge-medium {
            background: #FF9800;
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 12px;
            font-size: 0.8rem;
        }
        
        .badge-low {
            background: #F44336;
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 12px;
            font-size: 0.8rem;
        }
        
        /* File badges */
        .file-badge {
            background: #e3f2fd;
            padding: 0.25rem 0.75rem;
            border-radius: 16px;
            font-size: 0.85rem;
            color: #0D47A1;
            display: inline-block;
            margin: 0.25rem;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease-out;
        }
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .main {
                padding: 0rem 0.5rem;
            }
            
            h1 {
                font-size: 1.8rem;
            }
        }
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            .stMetric {
                background: #1e1e1e;
                color: white;
            }
            
            .result-card {
                background: #2d2d2d;
                color: white;
            }
            
            .streamlit-expanderHeader {
                background-color: #2d2d2d;
                color: white;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def apply_custom_theme():
    
    st.config.set_option('theme.primaryColor', '#1E88E5')
    st.config.set_option('theme.backgroundColor', '#FFFFFF')
    st.config.set_option('theme.secondaryBackgroundColor', '#F0F2F6')
    st.config.set_option('theme.textColor', '#262730')
    st.config.set_option('theme.font', 'sans serif')