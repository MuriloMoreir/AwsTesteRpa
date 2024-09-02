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

driver.get("https://www.google.com.br/search?q=dolar&sca_esv=419ad3eaf305d86b&sca_upv=1&hl=pt-BR&sxsrf=ADLYWII3evl_Bti9qwQpzCOP84sjR5siTA%3A1725270974087&source=hp&ei=vovVZsHwAqLL1sQPgvzGsAQ&iflsig=AL9hbdgAAAAAZtWZzmICfID4mMoOYwSl1RmIjY5B2NVU&ved=0ahUKEwjBx7Kc_6OIAxWipZUCHQK-EUYQ4dUDCBc&uact=5&oq=dolar&gs_lp=Egdnd3Mtd2l6IgVkb2xhcjIKECMYgAQYJxiKBTIIEAAYgAQYsQMyCBAAGIAEGLEDMggQABiABBixAzIIEAAYgAQYsQMyCBAAGIAEGLEDMggQABiABBixAzIIEAAYgAQYsQMyCBAAGIAEGLEDMggQABiABBixA0ipBVAAWNEDcAB4AJABAJgBogGgAYoEqgEDMC40uAEDyAEA-AEBmAIEoAKvBMICBBAjGCfCAgsQLhiABBjRAxjHAcICBRAAGIAEwgIOEAAYgAQYsQMYgwEYigXCAgsQABiABBixAxiDAcICDhAuGIAEGLEDGNEDGMcBmAMAkgcDMC40oAejHw&sclient=gws-wiz")
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
