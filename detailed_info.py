import pandas as pd
import ast
import re




def fix_salary_matches(salary_match):
    if len(salary_match)==0:
        return "not found"
    elif len(salary_match)==1:
        return salary_match[0]
    else:
        return f"from {salary_match[0]} to {salary_match[1]}"


def merge_with_original(original_file, cleaned_file, output_file):
    original_df = pd.read_csv(original_file)
    cleaned_df = pd.read_csv(cleaned_file)
    cleaned_df = cleaned_df[['salary_matches', 'skills','original_index','salary']]
    cleaned_df['salaries']=cleaned_df['salary_matches'].apply(lambda x: fix_salary_matches(ast.literal_eval(x)))

    cleaned_df['original_index'] = cleaned_df['original_index'].astype(int)
    merged_df = pd.merge(original_df, cleaned_df, left_index=True, right_on='original_index')
    merged_df['skills'] = merged_df['skills'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else set())
    merged_df.drop(columns=['original_index'], inplace=True)
    merged_df.to_csv(output_file, index=False)
    print(f"Data merged and saved to {output_file}")
    return output_file





def filter_by_parameters(input_file, parameters_dict,filtered_file):

    filtered = pd.read_csv(input_file)
    for param in parameters_dict:
        if param =="skills":
            skills=filtered['skills'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else set())
            filtered=filtered[skills.apply(lambda x: parameters_dict[param].issubset(x))]
        elif param == "salaries":
            salaries=filtered['salary'].apply(lambda x: ast.literal_eval(x))
            if parameters_dict[param] == "not found":
                filtered=filtered[filtered[param]==parameters_dict[param]]
            else:
                def f(salaries_list,salary):
                    if len(salaries_list)==0:
                        return False
                    elif len(salaries_list)==1:
                        return 0.8 * salaries_list[0] <= salary <= 1.2 * salaries_list[0]
                    else:
                        return salary>=salaries_list[0] and salary<= salaries_list[1]
                filtered=filtered[salaries.apply(lambda x: f(x,parameters_dict[param]))]


        else:
            pattern = r'\b' + re.escape(parameters_dict[param]) + r'\b'
            filtered = filtered[filtered[param].str.contains(pattern, case=False, na=False)]


    filtered.drop(columns=['salary'], inplace=True)
    filtered.drop(columns=['salary_matches'], inplace=True)
    for col in filtered.columns:
        filtered[col]=filtered[col].apply(lambda x: 'not found' if not x or  pd.isna(x) or x == '' or x == '[]' or x == 'set()' or x == set() or x=="None" else x)
    
    print(f"Filtered data saved to {filtered_file}")
    return filtered.to_csv(filtered_file, index=False)

def get_detailed_info(input_file, cleaned_file,merged_file , parameters_dict, filtered_file):
    """Extract detailed information from the dataset."""
    merged_file=merge_with_original(input_file, cleaned_file, merged_file)
    filter_by_parameters(merged_file, parameters_dict,filtered_file)
    



if __name__ == "__main__":

    original_file = "job_links.csv"
    cleaned_file="cleaned_data.csv"
    merged_file=merge_with_original(original_file, cleaned_file, "merged_data.csv")
    parameters = {
        'skills': {'Python'},
        "Job Title": "Software Engineer",
    }
    filter_by_parameters(merged_file, parameters,"filtered_data.csv")


