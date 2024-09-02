from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
from selenium.webdriver.chrome.options import Options
# import pandas as pd
import psycopg2
# import os
# from dotenv import load_dotenv

# Chamando load_dotenv
# load_dotenv()

# Obter a data e hora atual
dataAtual = datetime.now()

# Convertendo para String
dataConvertida = dataAtual.strftime('%Y-%m-%d')
horaAtual = dataAtual.strftime('%H:%M:%S')

print('Data atual: ', dataConvertida)
print('Hora atual: ', horaAtual)

# Entrando no site
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.google.com.br/search?q=d%C3%B3lar")
sleep(2)

# Pegando o valor do dólar
dolar = driver.find_element(By.CSS_SELECTOR, ('.DFlfde.SwHCTb'))
dolar_site = dolar.text
dolar_site = float(dolar_site.replace(",","."))
print('Dólar: ', dolar_site)



# Conectando com o DB
conexao = psycopg2.connect(database = "dbCotacao",
                           host = "pg-3f7b996d-muriloolimora971.f.aivencloud.com",
                           user = "avnadmin",
                           password = "AVNS_BjsAizQig1olY9q0atk",
                           port = "23734")

print(conexao.info)
print(conexao.status)

# Conexão com o cursor
cursor = conexao.cursor()

# Acionando Procedure
cursor.execute("call inserir_cotacao_dolar(%s, %s, %s)", (dataConvertida, horaAtual, dolar_site))

# Comitando
conexao.commit()
print("Dados inseridos")

# Desligando a conexão com o banco
cursor.close()
conexao.close()

# Fechando navegador
driver.quit()
