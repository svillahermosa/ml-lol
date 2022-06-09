import pandas as pd

from check_smurf import get_model_trained

lista_jugadores = ['elmi uwu69', 'HandSoIo', 'PEŁUK1NG', 'SK Eckas', 'vladi1v9', '1keduii1', 'FakeRookie1', 'Jonah Falcon', 'El Hookeru']

dic_df_jugadores = {}

df_full = pd.read_csv(fr"extracts/full_prepared2.tsv", sep='\t')
columns = list(df_full.columns)

model = get_model_trained()

for jugador in lista_jugadores:
    df = pd.read_csv(fr"extracts/{jugador}.tsv", sep='\t')
    predictions = model.predict(df)
    total_score = 0
    for pred in predictions:
        total_score += pred
    print(
        f'Probabilidad de ser smurf para el usuario {jugador}: {100 * total_score / len(predictions)} (basado en {len(predictions)} partidas)')
    dic_df_jugadores[jugador] = 100 * total_score / len(predictions)

print(dic_df_jugadores)


