# FuturePath AI

**FuturePath AI** is an AI-powered career guidance platform designed to help students, graduates, and professionals explore career options, predict ideal salaries, and identify required skills based on real-world job market data.

---

## Features

- **Career Prediction:**
    
    Predict your ideal career path using AI models based on your skills and salary expectations.
    
- **Salary Estimation:**
    
    Estimate your market value salary given your skills and desired job title.
    
- **Skill Recommendations:**
    
    Discover key skills required for your target career and salary goals.
    
- **Data Visualization:**
    
    Explore interactive visualizations of job market trends by filtering companies, skills, locations, and job titles.
    
- **Deep Insights:**
    
    Get comprehensive analytics with advanced filtering options to understand industry demands.
    
---

## Project Structure

- `app.py` — Streamlit app serving as the user interface.  
- `clean_data.py` — Script for cleaning raw scraped job data.  
- `detailed_info.py` — Filtering and detailed insights extraction.  
- `data_visualization.py` — Functions for plotting market relationship visualizations.  
- `ai_model.py` — AI model training, prediction, and saving.  
- `job_links.csv` — Raw scraped job data.  
- `cleaned_data.csv` — Cleaned and processed job data.  
- `merged_data.csv` — Merged original and cleaned data with additional features.  
- `filtered_data.csv` — Output of filtered data based on user queries.  
- `salary_model.pkl`, `skills_model.pkl`, `dream_career_model.pkl` — Trained AI models.  
- `mlb.pkl`, `le.pkl` — Pre-trained encoders for skills and job titles.  
- `background.jpg` — Background image used in the app header.  

---

## Installation

1. Clone this repository:
    
    ```bash
    git clone https://github.com/FZ-Charrate/futurepath-ai.git
    cd futurepath-ai
    ```
    
2. Install dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
    
3. Make sure you have `job_links.csv` with raw scraped data.  
4. Run the update script to clean data and train models:
    
    ```bash
    python update_data.py
    ```
    
5. Run the Streamlit app:
    
    ```bash
    streamlit run app.py
    ```
    
---

## Usage

### Home Tab

Welcome page with project description and key features.

### Visualize Data Tab

Filter job market data by skills, company, location, job title, or salary and visualize relationships between different job attributes.

### Insights Tab

Apply advanced filters to extract detailed market intelligence and download or view filtered data.

### Predict Tab

Use AI-powered models to:

- Predict your dream career based on your skills and expected salary.  
- Estimate your ideal salary based on your skills and career goals.  
- Discover essential skills required for a target career and salary.  

---

## AI Models

- **Salary Prediction:** Random Forest Regressor trained to estimate salary.  
- **Skills Prediction:** Random Forest Regressor to predict important skills.  
- **Dream Career Prediction:** Random Forest Regressor to recommend career paths.  

Encoders:

- MultiLabelBinarizer for skills.  
- LabelEncoder for job titles.  

Models and encoders are saved as `.pkl` files and loaded by the app.

---

## Contributing

Feel free to open issues or submit pull requests for improvements, bug fixes, or new features.

---

## License

MIT License

---

## Contact

For questions or collaboration, please contact facharrate@gmail.com .

# FuturePath-AI
