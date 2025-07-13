import pandas as pd
import numpy as np
import re





def extract_job_titles(title):
    keyword_map = {
        r"\bsoftware\b": "Software Engineer",
        r"\bfrontend\b": "Frontend Developer",
        r"\bbackend\b": "Backend Developer",
        r"\bfull\s*stack\b": "Full Stack Engineer",
        r"\bdev\s*ops\b": "DevOps Engineer",
        r"\bai\b": "AI Engineer",
        r"\bdata\s*scientist\b": "Data Scientist",
        r"\bmachine\s*learning\b": "Machine Learning Engineer",
        r"\bembedded\b": "Embedded Systems Engineer",
        r"\bcyber\b": "Cybersecurity Engineer",
        r"\bmechanical\b": "Mechanical Engineer",
        r"\belectrical\b": "Electrical Engineer",
        r"\bcivil\b": "Civil Engineer",
        r"\bindustrial\b": "Industrial Engineer",
        r"\bchemical\b": "Chemical Engineer",
        r"\bstructural\b": "Structural Engineer",
        r"\bpetroleum\b": "Petroleum Engineer",
        r"\bsystems\b": "Systems Engineer",
        r"\brobotics\b": "Robotics Engineer",
        r"\bhardware\b": "Hardware Engineer",
        r"\btelecommunications\b": "Telecommunications Engineer",
        r"\bmechatronics\b": "Mechatronics Engineer",
        r"\brenewable\b": "Renewable Energy Engineer",
        r"\benvironmental\b": "Environmental Engineer",
        r"\baerospace\b": "Aerospace Engineer"
    }
    title_lower = title.lower()
    for keyword_pat in keyword_map:
        if re.search(keyword_pat , title_lower):
            return keyword_map[keyword_pat]
    return "other"



def extract_salary(description):
    if not isinstance(description, str):
        return [],[]
    """Extract salary information from the job description."""
    salary_pattern =  r'\$\d{4,}(?:,\d{3})*(?:\.\d+)?|\b\d{1,3}k\b'
    matches = re.findall(salary_pattern, description)
    numeric_salaries = []
    for match in matches:
        if 'k' in match:
            numeric_salaries.append(float(match.replace('k',"").replace(',', ''))*1000)
        else:
            numeric_salaries.append(float(match.replace('$','').replace(',', '')))
    return numeric_salaries ,matches 

def extract_skills(description, skill_list):
    if not isinstance(description, str):
        return set()
    """Extract skills from the job description."""
    found_skills = set()
    for skill in skill_list:
        pattern= r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, description, re.IGNORECASE) :
            found_skills.add(skill)

    return found_skills 



def clean_data(input_file, output_file):
    """Clean the dataset and extract salary and skills."""
    # Load the dataset
    df = pd.read_csv(input_file)
    new_df = pd.DataFrame()

    # Predefined skill list
    skills = [
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
    

    # Extract salary and skills
    new_df['salary'] = df['description'].apply(lambda x: extract_salary(x)[0])
    new_df['salary_matches'] = df['description'].apply(lambda x: extract_salary(x)[1])
    new_df['skills'] = df['description'].apply(lambda x: extract_skills(x, skills))

    # Add a reference column to link to the original dataset
    new_df['original_index'] = df.index
    
    new_df['Job Title'] = (df['Job Title'].fillna("")).apply(extract_job_titles)
    new_df['Company'] = df['Company'].fillna("") 
    new_df['Location'] = df['Location'].fillna("") 
    new_df['description'] = df['description'].fillna("") 

    # Save the cleaned dataset
    new_df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")

if __name__ == "__main__":
    clean_data("sample_data.csv", "cleaned_sample_data.csv")
