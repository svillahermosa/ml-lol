import pandas as pd
from check_smurf import get_calculated_fields, get_model_trained

df2 = pd.read_csv(r"extracts/full2.tsv", sep='\t')
df2 = df2.loc[df2.summonerName == 'gg fructis']

df_bueno = get_calculated_fields(df2)

model = get_model_trained()


