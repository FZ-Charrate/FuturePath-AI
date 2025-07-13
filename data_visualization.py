import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import re
import ast

def load_data(input_file,user_choice,value):
    df = pd.read_csv(input_file)
    df['skills']= df['skills'].apply(lambda x: ast.literal_eval(x))
    df["salary"]=df['salary'].apply(lambda x: ast.literal_eval(x))
    df["salary"]=df['salary'].apply(lambda x:np.mean(x) if len(x) > 0 else 0)
    #mean_val = df.loc[df['salary'] != 0, 'salary'].mean()  # mean without zeros
    #df.loc[df['salary'] == 0, 'salary'] = mean_val
    
    if user_choice == "skills":
        mask=[value in i  for i in df[user_choice]]
    elif user_choice == "salary":
        mask=((df["salary"]>=value*0.8 )& (df["salary"]<=value*1.2) & (df["salary"]!=0) )
    else:
        pattren= r'\b' + re.escape(value) + r'\b'
        mask = [re.search(pattren, i,re.IGNORECASE) is not None if isinstance(i, str) else False for i in df[user_choice]] 
    
    return df[mask].explode("skills")


def plot_relationship(df, x, y, save_path="plot.png"):
    

    if x=="salary" or y=="salary":
        df=df[df["salary"]!=0]
    if len(df[x]) == 0 or len(df[y]) == 0:
        print(f"No data available for {x} or {y}.")
        return None

    fig_width =  len(df[x]) *0.1 +1
   

    fig_height = len(df[y])*0.1 +1
    plt.figure(figsize=(fig_width, fig_height))

    x_type = df[x].dtype
    y_type = df[y].dtype
    
    # Define if categorical (object or category dtype) or numerical
    is_x_cat = pd.api.types.is_categorical_dtype(df[x]) or x_type == 'object'
    is_y_cat = pd.api.types.is_categorical_dtype(df[y]) or y_type == 'object'
    
    if not is_x_cat and not is_y_cat:
        # Numerical vs Numerical
        sns.scatterplot(data=df, x=x, y=y)
        plt.title(f"Scatterplot of {x} vs {y}")

    elif is_x_cat and not is_y_cat:
        # Categorical (x) vs Numerical (y)
        sns.boxplot(data=df, x=x, y=y)
        plt.title(f"Boxplot of {y} by {x}")

    elif not is_x_cat and is_y_cat:
        # Numerical (x) vs Categorical (y) — swap axes, boxplot
        sns.boxplot(data=df, x=y, y=x)
        plt.title(f"Boxplot of {x} by {y}")

    else:
        # Categorical vs Categorical — heatmap of counts
        # Create a contingency table (cross-tab)
        ct = pd.crosstab(df[x], df[y])
        
        sns.heatmap(ct, annot=True, fmt="d", cmap="YlGnBu")
        plt.title(f"Heatmap of counts between {x} and {y}")
        plt.xlabel(y)
        plt.ylabel(x)

    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    plt.close()
    return save_path



if __name__ == "__main__":
    df = load_data("cleaned_data.csv","Job Title","Software Engineer")
    plot_path = plot_relationship(df, "Company", "skills")
    print(f"Plot saved to {plot_path}")
