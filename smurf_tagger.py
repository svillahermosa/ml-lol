import pandas as pd
from config import LOL_DIVISIONS

if __name__ == '__main__':
    df = pd.read_csv(r"C:\DevelopmentLaLiga\ml-lol\extracts\full.tsv", sep='\t')
    df_2 = df.sort_values('ts_fecha').groupby('jugador').tail(1)
    current_player_division = {}
    for index, row in df_2.iterrows():
        current_player_division[row['jugador']] = row['rango'].strip()


    for index, row in df.iterrows():
        if LOL_DIVISIONS[row['rango'].strip()] + 2 <= LOL_DIVISIONS[current_player_division[row['jugador']]]:
            df.loc[index, 'smurf'] = 1
        else:
            df.loc[index, 'smurf'] = 0
    df['smurf'] = df['smurf'].astype(int)
    df.to_csv(r"C:\DevelopmentLaLiga\ml-lol\extracts\full.tsv", sep='\t')
