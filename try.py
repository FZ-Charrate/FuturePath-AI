

import pandas as pd
df=pd.read_csv("job_links.csv")
df_small = df.head(20000)
df_small.to_csv("Sample_job_data.csv", index=False)
