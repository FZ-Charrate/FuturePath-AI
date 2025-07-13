import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
import joblib
import ast

def preprocess_data(df):
    """Preprocess the data for training."""
    # Encode skills using MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    skills_encoded = mlb.fit_transform(df['skills'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else set()))

    # Encode dream career using LabelEncoder
    le = LabelEncoder()
    df['dream_career_encoded'] = le.fit_transform(df['Job Title'])

        # Target columns
    y_salary = df['salary'].apply(lambda x:np.mean(x) if len(x) > 0 else 0).to_numpy().reshape(-1, 1)
    y_skills = skills_encoded
    y_dream_career = df[['dream_career_encoded']].to_numpy() 

    # input features
    x_salary = np.hstack([
        y_skills,  
        y_dream_career,                                                            
    ])

    x_skills = np.hstack([
        y_salary,
        y_dream_career,                                                            
    ])

    x_dream_career = np.hstack([
        y_salary,
        y_skills,                                                            
    ])



    return x_salary,x_skills,x_dream_career, y_salary, y_skills, y_dream_career, mlb, le

def train_models(x_salary,x_skills,x_dream_career, y_salary, y_dream_career,y_skills):
    """Train the AI models."""
    # Train salary prediction model
    salary_model = RandomForestRegressor()
    salary_model.fit(x_salary, y_salary)

        # Train skills prediction model
    skills_model = RandomForestRegressor()
    skills_model.fit(x_skills, y_skills)

    # Train dream career prediction model
    dream_career_model = RandomForestRegressor()
    dream_career_model.fit(x_dream_career, y_dream_career)



    return salary_model,skills_model, dream_career_model

def main(cleaned_file):
    # Load the cleaned dataset
    df = pd.read_csv(cleaned_file)
    # Convert salary from string representation to list
    df["salary"]= df["salary"].apply(lambda x: ast.literal_eval(x))
    x_salary,x_skills,x_dream_career, y_salary, y_skills, y_dream_career, mlb, le = preprocess_data(df)
    # Train the models
    salary_model,skills_model, dream_career_model = train_models(x_salary,x_skills,x_dream_career, y_salary, y_dream_career,y_skills)
    # Save the models and encoders
    joblib.dump(salary_model, "salary_model.pkl")
    joblib.dump(skills_model, "skills_model.pkl")
    joblib.dump(dream_career_model, "dream_career_model.pkl")
    joblib.dump(mlb, "mlb.pkl")
    joblib.dump(le, "le.pkl")
    print("Models trained and saved!")




if __name__ == "__main__":
    # Load the cleaned dataset
    df = pd.read_csv("cleaned_sample_data.csv")
    df["salary"]= df["salary"].apply(lambda x: ast.literal_eval(x))

    # Preprocess the data
    x_salary,x_skills,x_dream_career, y_salary, y_skills, y_dream_career, mlb, le = preprocess_data(df)

    # Train the models
    salary_model,skills_model, dream_career_model = train_models(x_salary,x_skills,x_dream_career, y_salary, y_dream_career,y_skills)

    # Save the models and encoders
    joblib.dump(salary_model, "salary_model.pkl")
    joblib.dump(skills_model, "skills_model.pkl")
    joblib.dump(dream_career_model, "dream_career_model.pkl")
    joblib.dump(mlb, "mlb.pkl")
    joblib.dump(le, "le.pkl")
    print("Models trained and saved!")