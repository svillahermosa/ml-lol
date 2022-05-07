from util import get_data_from_account
import pandas as pd


if __name__ == '__main__':
    accounts = ["gg fructis"]#, "ChicoRebelde","TheBoySavior 69","no tiene sendito","LambOrnnGinyin","KOI ÄITANA","Pyke Wazowskii", "KeyboardWRLD999", "Adryos Lepido","2023 Tercera","Amadeu Carvalho", "elmi uwu69", "PEŁUK1NG", "egirls above all", "ELMILLOR IS BACK", "IamDiamond", "Remember me mom", "abby me arruinó", "EL GRÁFICAS", "Laccek", "Aesenardo", "IreliaCosplayer", "Berri Vuelve Xfa", "KOI TheGrefg", "Barriga Humana", "heyy olviyonna", "Goku que", "Cabeza de Huevo", "MOTONAMl", "Ladguillos69", "Monje Shacolínn", "DuaLLipa", "CaiQi fangirl", "Weakside Jayce", "Beep bop SIUUUUU", "DevuelvanEl0ro", "TetelOl EnjoyeR"]
    # accounts = ['SanadinoPepino']
    df_final = pd.DataFrame()
    for account in accounts:
        print(f'INIT - Obteniendo datos de: {account}')
        df = get_data_from_account(account)
        df_final = pd.concat([df_final, df])
        df_final.to_csv(r"C:\Users\Alfonso\Documents\IA\ProyectoLOL\yoya.csv", sep='\t')
        print(f'END - Obteniendo datos de: {account}')
    print(f"Total de datos conseguidos de {len(accounts)} cuentas: \n - {df_final.shape[0]} participantes \n - {int(df_final.shape[0]/10)} partidas \n - {df_final.shape[1]} columnas ")
