from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium.webdriver import ActionChains
import time


def get_info_from_match(summoner_name):
    # Crear una sesión de Firefox
    driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe')
    driver.implicitly_wait(10)
    driver.maximize_window()

    summoner_name = summoner_name.replace(' ', '+')

    driver.get(f"https://www.leagueofgraphs.com/es/summoner/euw/{summoner_name}")

    flag_ver_mas = 1
    while flag_ver_mas:
        try:

            search_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "see_more_ajax_button")))
            ActionChains(driver).click(search_field).perform()
        except:
            flag_ver_mas = 0

    tabla_partidas = driver.find_element(By.CLASS_NAME, value="data_table.relative.recentGamesTable.inverted_rows_color")
    elems = tabla_partidas.find_elements(By.XPATH, value='//a[contains(@href,"/es/match/euw")]')
    list_href_partidas = []
    for elem in elems:
        list_href_partidas.append(elem.get_attribute("href"))
    list_href_partidas = set(list_href_partidas)
    partidas_jugadores_rango = {'pk_partida': [], 'jugador': [], 'rango': []}
    for url in list_href_partidas:
        driver.get(url)
        box = driver.find_element(By.CLASS_NAME, 'data_table.matchTable')
        jugadores = box.find_elements(By.XPATH, '//a[contains(@href,"/es/summoner/euw")]')
        jugadores_rango = {}
        for i in range(1,20,2):
            jugador = jugadores[i]
            nombre = jugador.find_element(By.CLASS_NAME, 'name').text
            clasi = jugador.find_element(By.CLASS_NAME, 'subname').text
            jugadores_rango[nombre] = clasi
        partida_pk = list(jugadores_rango.keys())
        partida_pk.sort()
        partida_pk = '_'.join(partida_pk)
        for jugador, rango in jugadores_rango.items():
            partidas_jugadores_rango['pk_partida'].append(partida_pk)
            partidas_jugadores_rango['jugador'].append(jugador)
            partidas_jugadores_rango['rango'].append(rango)

    return pd.DataFrame().from_dict(partidas_jugadores_rango)



df = get_info_from_match('gg fructis')
