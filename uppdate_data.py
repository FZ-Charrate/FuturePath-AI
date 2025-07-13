import clean_data as cd
import ai_model as am


#MAIN FILE
input_file = "job_links.csv"
#CLEAN_FILE
cleaned_file="cleaned_data.csv"
# Clean the data
cd.clean_data(input_file,cleaned_file)
#TRAIN MODELS
am.main(cleaned_file)
