# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 10:12:26 2024

@author: Rolando Gonzàlez
"""

import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import git

def scrape_data():
    # Define la URL de la página principal de donde se van a extraer los datos.
    PAGINA_PRINCIPAL = "https://www.scrapethissite.com/pages/simple/"

    # Inicializa el navegador Firefox.
    navegador = webdriver.Firefox()
    navegador.get(PAGINA_PRINCIPAL)  # Abre la página web especificada por la URL.
    navegador.implicitly_wait(10)  # Establece una espera implícita de 10 segundos para que los elementos se carguen.

    datos = []  # Inicializa una lista vacía para almacenar los datos.

    try:
        # Espera explícita de hasta 10 segundos para que los elementos con el selector '.country' estén presentes.
        paises = WebDriverWait(navegador, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.country'))
        )

        # Itera sobre cada país encontrado en la página.
        for pais in paises:
            # Encuentra los elementos correspondientes a la capital, población y superficie del país.
            nombre = pais.find_element(By.CSS_SELECTOR, ".country-name").text
            capital = pais.find_element(By.CSS_SELECTOR, ".country-capital").text
            poblacion = pais.find_element(By.CSS_SELECTOR, ".country-population").text
            superficie = pais.find_element(By.CSS_SELECTOR, ".country-area").text
            # Agrega la información del país a la lista de datos en forma de diccionario.
            datos.append({
                'nombre': nombre,
                'capital': capital,
                'poblacion': poblacion,
                'superficie': superficie
            })

    except Exception as e:
        # Si ocurre una excepción durante la espera, la lanza para ser manejada posteriormente.
        raise e
    finally:
        navegador.quit()  # Cierra el navegador.

    # Convierte la lista de datos en un DataFrame de pandas.
    df = pd.DataFrame(datos)
    return df

def save_to_csv(df):
    # Obtener la ruta del directorio actual.
    directorio_actual = os.getcwd()
    # Concatenar la ruta del directorio con el nombre del archivo CSV.
    ruta_csv = os.path.join(directorio_actual, "paises_exportados.csv")
    # Guarda el DataFrame como un archivo CSV sin incluir el índice.
    df.to_csv(ruta_csv, index=False)
    print(df)  # Imprime el DataFrame (para propósitos de depuración).
    return ruta_csv

def push_to_github(file_path):
    # Configura el repositorio de Git
    repo_path = '/ruta/al/repositorio/'  # Reemplaza con la ruta a tu repositorio local
    repo = git.Repo(repo_path)
    repo.git.add(file_path)
    repo.index.commit("Añadir datos de países exportados")
    origin = repo.remote(name='origin')
    origin.push()
    print('Datos subidos a GitHub')

if __name__ == "__main__":
    df = scrape_data()
    file_path = save_to_csv(df)
    print('LISTO!')  # Imprime un mensaje indicando que el proceso ha finalizado
    
    
    ### Reflesion###
# 1 aprendo que  se puede resiclar el codigo
# 2 que hay que revisar cuidadosamente puntos comas y enespecial en mi caso tener cuidado en no momerme las letras
# 3 que me sta costando demasiado Quarto y hacelo PDF
# 4 no porque reutilice el codigo que usamos en clases