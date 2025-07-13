import streamlit as st
import pandas as pd
import joblib
import numpy as np
import data_visualization as dv
import detailed_info as di
import base64
import os

st.set_page_config(layout="wide", page_title="FuturePath AI", page_icon="🎯")

img_path = os.path.join(os.getcwd(), "background.jpg")
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_base64(img_path)

# HTML CODE
html_style="""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gabriola:wght@400;700&display=swap');

/* Global Styles */
* {
    font-family: 'Gabriola', cursive !important;
}

/* Main Container */
.stApp {
    background: linear-gradient(135deg, #1c1f1a 0%, #2a2d26 100%);
    min-height: 100vh;
}

/* Header */
.main-header {
    background-image: url("data:image/jpeg;base64,___IMG_BASE64___");
    padding: 2rem 0;
    margin-bottom: 2rem;
    border-radius: 0 0 30px 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    position: sticky;
    top: 0;
    z-index: 1000;
    height: 300px;
    border: 2px solid rgba(196, 196, 124, 0.5);
}

.main-title {
filter: brightness(1.9);
    color: #ffffff;
    font-size: 6rem;
    font-weight: 700;
    text-align: center;
    font-family: 'Gabriola', cursive;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    background: linear-gradient(45deg, #c4c47c, #a8a060, #8b8b47);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.subtitle {
    color: #e8e8d4;
    font-size: 1.5rem;
    text-align: center;
    font-family: 'Gabriola', cursive;
    margin-top: 0.5rem;
}

/* Tabs */
.stTabs {
    background: transparent;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 5px;
    background: rgba(0, 0, 0, 0.3);
    padding: 10px;
    border-radius: 25px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(196, 196, 124, 0.3);
    margin-bottom: 2rem;
}

.stTabs [data-baseweb="tab"] {
    background: linear-gradient(135deg, rgba(28, 31, 26, 0.8), rgba(42, 45, 38, 0.8));
    color: #e8e8d4;
    border: none;
    border-radius: 20px;
    padding: 15px 25px;
    font-size: 1.2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    backdrop-filter: blur(5px);
    font-family: 'Gabriola', cursive;
}

.stTabs [data-baseweb="tab"]:hover {
    background: linear-gradient(135deg, rgba(139, 139, 71, 0.6), rgba(168, 160, 96, 0.6));
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(139, 139, 71, 0.4);
    color: #ffffff;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #8b8b47, #a8a060) !important;
    color: #ffffff !important;
    box-shadow: 0 5px 20px rgba(139, 139, 71, 0.6);
    transform: translateY(-2px);
}

/* Tab Content */
.stTabs [data-baseweb="tab-panel"] {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(248, 250, 247, 0.98));
    border-radius: 25px;
    padding: 2rem;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(196, 196, 124, 0.2);
    color: #2a2d26;
}

/* Headers */
h1, h2, h3 {
    color: #1c1f1a;
    font-family: 'Gabriola', cursive;
    font-weight: 700;
}

.stHeader {
    color: #1c1f1a;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-align: center;
}

/* Text */
p, .stMarkdown p {
    color: #3a3d33;
    font-size: 1.3rem;
    line-height: 1.6;
    font-family: 'Gabriola', cursive;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1c1f1a, #0f1110);
    color: #e8e8d4;
    border: 2px solid #8b8b47;
    border-radius: 25px;
    padding: 15px 30px;
    font-size: 1.2rem;
    font-weight: 600;
    font-family: 'Gabriola', cursive;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    width: 100%;
    max-width: 300px;
    margin: 10px auto;
    display: block;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #8b8b47, #a8a060);
    color: #ffffff;
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(139, 139, 71, 0.4);
    border-color: #c4c47c;
}

.stButton > button:active {
    transform: translateY(-1px);
    box-shadow: 0 3px 10px rgba(139, 139, 71, 0.3);
}

/* Select Boxes */
.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.95);
    border: 2px solid #a8a060;
    border-radius: 15px;
    font-family: 'Gabriola', cursive;
    font-size: 1.2rem;
    color: #1c1f1a;
    backdrop-filter: blur(5px);
}

.stSelectbox > div > div:focus {
    border-color: #8b8b47;
    box-shadow: 0 0 0 3px rgba(139, 139, 71, 0.2);
}

/* Multi-select */
.stMultiSelect > div > div {
    background: rgba(255, 255, 255, 0.95);
    border: 2px solid #a8a060;
    border-radius: 15px;
    font-family: 'Gabriola', cursive;
    color: #1c1f1a;
    backdrop-filter: blur(5px);
}

/* Text Input */
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.95);
    border: 2px solid #a8a060;
    border-radius: 15px;
    font-family: 'Gabriola', cursive;
    font-size: 1.2rem;
    color: #1c1f1a;
    padding: 12px 15px;
    backdrop-filter: blur(5px);
}

.stTextInput > div > div > input:focus {
    border-color: #8b8b47;
    box-shadow: 0 0 0 3px rgba(139, 139, 71, 0.2);
}

/* Number Input */
.stNumberInput > div > div > input {
    background: rgba(255, 255, 255, 0.95);
    border: 2px solid #a8a060;
    border-radius: 15px;
    font-family: 'Gabriola', cursive;
    font-size: 1.2rem;
    color: #1c1f1a;
    padding: 12px 15px;
    backdrop-filter: blur(5px);
}

.stNumberInput > div > div > input:focus {
    border-color: #8b8b47;
    box-shadow: 0 0 0 3px rgba(139, 139, 71, 0.2);
}

/* Radio Buttons */
.stRadio > div {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 10px;
}

.stRadio > div > label {
    background: rgba(255, 255, 255, 0.9);
    padding: 10px 20px;
    border-radius: 20px;
    border: 2px solid #a8a060;
    color: #1c1f1a;
    font-family: 'Gabriola', cursive;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(5px);
}

.stRadio > div > label:hover {
    background: rgba(196, 196, 124, 0.2);
    border-color: #8b8b47;
}

.stRadio > div > label[data-checked="true"] {
    background: linear-gradient(135deg, #8b8b47, #a8a060);
    color: #ffffff;
    border-color: #c4c47c;
}

/* Success Messages */
.stSuccess {
    background: linear-gradient(135deg, rgba(139, 139, 71, 0.1), rgba(168, 160, 96, 0.1));
    border: 2px solid #a8a060;
    border-radius: 15px;
    color: #1c1f1a;
    font-family: 'Gabriola', cursive;
    font-size: 1.3rem;
    font-weight: 600;
}

/* Warning Messages */
.stWarning {
    background: linear-gradient(135deg, rgba(196, 196, 124, 0.1), rgba(139, 139, 71, 0.1));
    border: 2px solid #c4c47c;
    border-radius: 15px;
    color: #1c1f1a;
    font-family: 'Gabriola', cursive;
    font-size: 1.3rem;
    font-weight: 600;
}

/* DataFrames */
.stDataFrame {
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
}

/* Images */
.stImage {
    border-radius: 15px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
    overflow: hidden;
}

/* Welcome Section */
.welcome-section {
    background: linear-gradient(135deg, rgba(139, 139, 71, 0.15), rgba(168, 160, 96, 0.15));
    padding: 2rem;
    border-radius: 20px;
    border: 2px solid rgba(196, 196, 124, 0.4);
    margin: 1rem 0;
    backdrop-filter: blur(5px);
}

.feature-card {
    background: rgba(255, 255, 255, 0.9);
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    border: 2px solid #e8e8d4;
    transition: all 0.3s ease;
    backdrop-filter: blur(5px);
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(139, 139, 71, 0.3);
    border-color: #a8a060;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #8b8b47, #a8a060);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #c4c47c, #8b8b47);
}

/* Center content */
.center-content {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

/*FINALL CHANGES*/
div[role="tablist"]{
display: flex;
justify-content: space-evenly;
}

#tabs-bui2-tab-0 > div > p,#tabs-bui2-tab-1 > div > p, #tabs-bui2-tab-2 > div > p, #tabs-bui2-tab-3 > div > p,#root > div:nth-child(1) > div.withScreencast > div > div > section > div.stMainBlockContainer.block-container.st-emotion-cache-zy6yx3.en45cdb4 > div > div > div.stElementContainer.element-container.st-emotion-cache-17lr0tt.e1lln2w81 > div > div > div > p ,#tabs-bui2-tabpanel-1 > div > div > div:nth-child(9) > div > button > div > p,#tabs-bui2-tabpanel-2 > div > div > div:nth-child(6) > div > button > div > p,#tabs-bui2-tabpanel-3 > div > div > div:nth-child(9) > div > button > div > p{
    font-family: 'Gabriola', cursive;
    font-size: 1.2rem;
    color: #e8e8d4 !important;
    font-weight: 600;
}
.welcome-section{
text-align: center;
font-weight:600 ;
font-size: 2rem;
padding:0.5rem;
}

.st-c2{
background: linear-gradient(135deg, #8b8b47, #a8a060) ;}

.stAppHeader{
background: linear-gradient(135deg, #8b8b47, #a8a060) !important;
color:black;
width:20%;
height: 10%;
 margin-right: 0; 
  margin-left: auto;
border-radius: 0 20px;
display: flex;
wrap: wrap;
}

.st-emotion-cache-ktz07o:active {
border-color: #8b8b47 !important;
}
.stImage{
margin: auto;
}


</style>

<!-- Fixed Header -->
<div class="main-header">
    <h1 class="main-title">FuturePath AI</h1>
    <p class="subtitle">Your Intelligent Career Navigator</p>
</div>
"""

html_style = html_style.replace("___IMG_BASE64___", img_base64)

# Apply custom CSS
st.markdown(html_style, unsafe_allow_html=True)

#MAIN FILE
input_file = "job_links.csv"
#CLEAN_FILE
cleaned_file="cleaned_data.csv"
# synonym dictionary
Syn_dict={"Wanted skills":"skills",
            "Company":"Company",
            "Location":"Location",
            "Job title":"Job Title",
            "Salary range":"salary"}
#MY SKILLS
my_skills=[
    # Programming & Development
    "Python", "Java", "JavaScript", "C++", "C#", "Go", "Ruby", "PHP", "SQL", "TypeScript", "Swift", "Kotlin",

    # Web Development
    "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "REST API", "GraphQL",

    # Data Science & AI
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn", "NLP", "Computer Vision",
    "Data Analysis", "Big Data", "Hadoop", "Spark", "Data Mining", "Data Visualization", "R", "MATLAB",

    # DevOps & Cloud
    "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud", "CI/CD", "Terraform", "Ansible", "Jenkins",

    # Cybersecurity
    "Penetration Testing", "Network Security", "Firewalls", "Encryption", "SIEM", "Vulnerability Assessment",

    # Embedded & Systems
    "Embedded Systems", "RTOS", "Microcontrollers", "ARM", "FPGA", "Linux", "Unix", "Shell Scripting",

    # Engineering / Core Skills
    "CAD", "SolidWorks", "MATLAB", "ANSYS", "Finite Element Analysis", "Project Management", "Six Sigma",
    "Lean Manufacturing", "AutoCAD", "SCADA", "PLC Programming", "Hydraulics", "Thermodynamics",

    # Soft Skills (optional)
    "Communication", "Leadership", "Teamwork", "Problem Solving", "Critical Thinking", "Adaptability",

    # Others (general technical and professional)
    "Agile", "Scrum", "Kanban", "Git", "Version Control", "Testing", "Quality Assurance", "Automation",

]
#JOB TITELS
job_titles = [ # Software / IT
    "Software Engineer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Engineer",
    "DevOps Engineer",
    "AI Engineer",
    "Data Scientist",
    "Machine Learning Engineer",
    "Embedded Systems Engineer",
    "Cybersecurity Engineer",

    # Core Engineering
    "Mechanical Engineer",
    "Electrical Engineer",
    "Civil Engineer",
    "Industrial Engineer",
        "Chemical Engineer",
    "Structural Engineer",
    "Petroleum Engineer",

    # Specialized / Modern Fields
    "Systems Engineer",
    "Robotics Engineer",
    "Hardware Engineer",
    "Telecommunications Engineer",
    "Mechatronics Engineer",
    "Renewable Energy Engineer",
    "Environmental Engineer",
    "Aerospace Engineer"
]
#MERGED FILE
merged_file = "merged_data.csv"
#FILTERED FILE
filtered_file = "filtered_data.csv"

#TABS
tabs = st.tabs(["Home", "Visualize Data", "Insights", "Predict"])

with tabs[0]:
    st.markdown('<div class="welcome-section">Dear user', unsafe_allow_html=True)
    
    
    st.markdown("## Welcome to FuturePath AI!")
    
    description = """
    Discover your professional potential with our AI-powered career guidance platform. 
    Whether you're a student exploring possibilities, a graduate planning your path, 
    or a professional considering a career change, we're here to illuminate your journey.
    """
    
    st.markdown(description)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
        <div class="feature-card">
            <h3>Career Prediction</h3>
            <p>Leverage advanced AI algorithms to predict your ideal career path based on your unique skill set and salary expectations.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="feature-card">
            <h3>Data Visualization</h3>
            <p>Explore interactive visualizations of job market trends across industries, companies, and geographic locations.</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="feature-card">
            <h3>Deep Insights</h3>
            <p>Access comprehensive job market analysis with detailed filtering options to understand industry demands.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="feature-card">
            <h3>Smart Recommendations</h3>
            <p>Receive personalized recommendations for skill development and career advancement opportunities.</p>
        </div>
        ''', unsafe_allow_html=True)

with tabs[1]:
    st.markdown('<h2 class="stHeader">📊 Visualize Market Relationships</h2>', unsafe_allow_html=True)
    st.write("Filter the dataset based on your criteria, then select two columns to visualize their relationship.")
        
    user_choice = st.selectbox("→ Choose main filter column", ["Wanted skills", "Company", "Location", "Job title", "Salary range"])
    if user_choice == "Salary range":
        value = st.number_input("Enter expected salary", 0)
    elif user_choice == "Wanted skills":
        value =st.radio("→ Choose a skill to filter by",my_skills)
    elif user_choice == "Job title":
        value=st.radio("→ Choose a job title to filter by", job_titles )
    elif user_choice == "Company":
        value = st.text_input("→ Enter company name to filter by", "")
    else:
        value=st.text_input("→ Enter location to filter by", "")
    
    st.markdown("---")
    st.markdown("### What would you like to visualize?")
    
    col1, col2 = st.columns(2)
    with col1:
        y=st.selectbox("Y-axis:",["Wanted skills", "Company", "Location", "Job title", "Salary range"])
    with col2:
        x=st.selectbox("X-axis:",["Wanted skills", "Company", "Location", "Job title", "Salary range"])
    
    
    
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    if st.button("✨ Generate Visualization"):
        df = dv.load_data(cleaned_file,Syn_dict[user_choice],value)
        df = df.sample(n=200, random_state=42) if len(df) > 1000 else df
        plot_path = dv.plot_relationship(df, Syn_dict[x], Syn_dict[y])
        if plot_path:
            st.image(plot_path, caption=f"Relationship between {x} and {y}")
        else:
            st.warning("No data available for the selected filters.")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]:
    st.markdown('<h2 class="stHeader">🔍 Market Intelligence & Insights</h2>', unsafe_allow_html=True)
    st.write("Dive deep into job market analytics with our advanced filtering system. Discover trends, patterns, and opportunities tailored to your preferences.")
    
    parameters_list=st.multiselect("→ Select parameters to analyze:",options=["Wanted skills", "Company", "Location", "Job title", "Salary range"])
    parameters_dict={}
    
    for param in parameters_list:
        if param == "Wanted skills":
            skills_list=st.multiselect("→ Choose skills to analyze:",options=my_skills)
            parameters_dict["skills"] = set(skills_list)
        elif param == "Salary range":
            sal=st.number_input("→ Enter your target salary ($)",min_value=0.0,step=1000.0)
            if sal == 0.0:
                parameters_dict["salaries"] = "not found"
            else:
                parameters_dict["salaries"] = sal
        elif param == "Job title":
            job_title=st.selectbox("→ Select target job title",job_titles)
            parameters_dict["Job Title"] = job_title
        else:
            value=st.text_input(f"→ Enter {param} to analyze", "")
            if value:
                parameters_dict[Syn_dict[param]] = value
    
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    if st.button("🚀 Generate Insights"):
        if not parameters_dict:
            st.warning("Please select at least one parameter to analyze!")
        else:
            di.get_detailed_info(input_file, cleaned_file,merged_file , parameters_dict, filtered_file)
            st.success("Analysis complete! Here are your personalized insights:")
            st.dataframe(pd.read_csv(filtered_file))
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[3]:
    # Load models and encoders
    salary_model = joblib.load("salary_model.pkl")
    dream_career_model = joblib.load("dream_career_model.pkl")
    skills_model = joblib.load("skills_model.pkl")
    mlb = joblib.load("mlb.pkl")
    le = joblib.load("le.pkl")
     
    st.markdown('<h2 class="stHeader">🔮 AI-Powered Career Predictions</h2>', unsafe_allow_html=True)
    st.markdown("### Unlock your potential with cutting-edge artificial intelligence")
    
    prediction_type = st.radio("→ What would you like to discover?", 
                              ["🎯 Dream Career", "💰 Ideal Salary", "🛠️ Required Skills"], 
                              horizontal=True, index=0)
    
    if prediction_type == "🎯 Dream Career":
        st.markdown("#### Discover your perfect career match")
        st.write("Let our AI analyze your skills and salary expectations to find your ideal career path.")
        
        skills = st.multiselect("→ What skills do you possess?",options= my_skills, default=my_skills[:3])
        salary = st.number_input("→ What's your expected salary? ($)", min_value=0.0, step=1000.0, value=0.0)
        
        st.markdown('<div class="center-content">', unsafe_allow_html=True)
        if st.button("🎯 Predict My Dream Career"):
            salary_arr = np.array([salary]).reshape(-1, 1)
            skills_arr = mlb.transform([skills])
            X_input = np.hstack([salary_arr, skills_arr])
            prediction = dream_career_model.predict(X_input)
            decoded = le.inverse_transform(prediction.astype(int).reshape(-1))
            st.success(f"🌟 Your predicted dream career: **{decoded[0]}**")
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif prediction_type == "💰 Ideal Salary":
        st.markdown("#### Discover your market value")
        st.write("Find out what salary you can expect based on your skills and career aspirations.")
        
        skills = st.multiselect("→ What skills do you have?", options=my_skills, default=my_skills[:3])
        dream_career = st.selectbox("→ What's your target career?", job_titles)
        
        st.markdown('<div class="center-content">', unsafe_allow_html=True)
        if st.button("💰 Calculate My Market Value"):
            skills_arr = mlb.transform([skills])
            dream_career_arr = le.transform([dream_career]).reshape(-1, 1)
            X_input = np.hstack([skills_arr, dream_career_arr])
            predicted_salary = salary_model.predict(X_input)[0]
            st.success(f"💎 Your predicted ideal salary: **${predicted_salary:,.2f}**")
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.markdown("#### Discover the skills you need")
        st.write("Find out which skills are most important for your target career and salary range.")
        
        salary = st.number_input("→ What's your target salary? ($)", min_value=0.0, step=1000.0, value=0.0)
        dream_career = st.selectbox("→ What's your target career?", job_titles)
        
        st.markdown('<div class="center-content">', unsafe_allow_html=True)
        if st.button("🛠️ Discover Required Skills"):
            salary_arr = np.array([salary]).reshape(-1, 1)
            dream_career_arr = le.transform([dream_career]).reshape(-1, 1)
            X_input = np.hstack([salary_arr, dream_career_arr])
            predicted_skills = skills_model.predict(X_input)
            encoded_skills_mask=(predicted_skills[0]>= 0.1).astype(int).reshape(1, -1)
            decoded_skills = mlb.inverse_transform(encoded_skills_mask)
            st.success(f"🎯 Essential skills for your path: **{', '.join(decoded_skills[0])}**")
        st.markdown('</div>', unsafe_allow_html=True)