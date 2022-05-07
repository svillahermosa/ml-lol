from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium.webdriver import ActionChains
import time


def get_info_from_match(match_name, na_team_local, na_team_away):
    # Crear una sesión de Firefox
    driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe')
    driver.implicitly_wait(10)
    driver.maximize_window()

    # Acceder a la aplicación web
    driver.get("https://www.leagueofgraphs.com/es/summoner/euw/gg+fructis")

    # Localizar cuadro de busqueda
    # flag_ver_mas = 1
    # while flag_ver_mas:
    #     try:
    #
    #         search_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "see_more_ajax_button")))
    #         ActionChains(driver).click(search_field).perform()
    #     except:
    #         flag_ver_mas = 0


    # Indicar y confirmar término de búsqueda
    tabla_partidas = driver.find_element(By.CLASS_NAME, value="data_table.relative.recentGamesTable.inverted_rows_color")
    elems = tabla_partidas.find_elements(By.XPATH, value='//a[contains(@href,"/es/match/euw")]')
    list_href_partidas = []
    for elem in elems:
        list_href_partidas.append(elem.get_attribute("href"))
    list_href_partidas = set(list_href_partidas)
    # pinchamos en el partido para obtener mas info
    boton_mas_info = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='PUDfGe S3PB2d']")))
    boton_mas_info.click()
    boton_alineaciones = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-tab_type='SOCCER_LINEUPS']")))
    boton_alineaciones.click()

    # Obtener la lista de jugadores

    jugadores_titulares = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@class='lrvl-pc imso-loa']")))
    jugadores_banquillo = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@class='lr-imso-ls-t']")))
    jugadores_banquillo = jugadores_banquillo[0].find_elements(By.TAG_NAME, "td")

    df_players = get_players_from_selenium(jugadores_titulares, jugadores_banquillo, na_team_local, na_team_away)

    # Cerrar la ventana del navegador
    driver.quit()

    return  df_players

def add_player_to_dict(dict, id_team, na_player, nu_jersey):
    dict['equipo_google'].append(id_team)
    dict['jugador_google'].append(na_player)
    try:
        dict['dorsal_google'].append(int(nu_jersey))
    except Exception as error:
        dict['dorsal_google'].append(0)
        print(error)



def get_players_from_selenium(jugadores_titulares, jugadores_banquillo, na_team_local, na_team_away):
    dict_to_df = {'equipo_google': [], 'jugador_google': [], 'dorsal_google': []}
    i = 0
    while i < len(jugadores_banquillo):
        if jugadores_banquillo[i].accessible_name != '' and jugadores_banquillo[i + 3].accessible_name != '':
            add_player_to_dict(dict_to_df, na_team_local, jugadores_banquillo[i + 1].accessible_name, jugadores_banquillo[i].accessible_name)
            add_player_to_dict(dict_to_df, na_team_away, jugadores_banquillo[i + 3].accessible_name, jugadores_banquillo[i + 4].accessible_name)
            i += 5
        elif jugadores_banquillo[i].accessible_name != '' and jugadores_banquillo[i + 3].accessible_name == '':
            add_player_to_dict(dict_to_df, na_team_local, jugadores_banquillo[i + 1].accessible_name, jugadores_banquillo[i].accessible_name)
            i += 4
        elif jugadores_banquillo[i].accessible_name == '' and jugadores_banquillo[i + 2].accessible_name != '':
            add_player_to_dict(dict_to_df, na_team_away, jugadores_banquillo[i + 2].accessible_name, jugadores_banquillo[i + 3].accessible_name)
            i += 4
    i = 0
    while i < len(jugadores_titulares):
        jugador = jugadores_titulares[i].accessible_name.split(" ")
        if i < 11:
            add_player_to_dict(dict_to_df, na_team_local, jugador[1], jugador[0])
        else:
            add_player_to_dict(dict_to_df, na_team_away, jugador[1], jugador[0])
        i += 1

    return pd.DataFrame().from_dict(dict_to_df)



get_info_from_match('levante-real sociedad', 'levante', 'real sociedad')