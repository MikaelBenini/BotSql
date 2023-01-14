import time
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By

# prefixo do link
link_prefix = "https://ev.braip.com/vendas/obrigado/"

# configuração da conexão com o banco de dados
config = {
    'user': 'senhafacil',
    'password': 'Reimisterio145',
    'host': 'mysql.senhafacil.net.br',
    'database': 'senhafacil'
}

# inicializar o driver do navegador
driver = webdriver.Chrome()

# conectar ao banco de dados
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# recuperar links da tabela de links
query = "SELECT codigos FROM Codigo"
cursor.execute(query)
results = cursor.fetchall()
link_count = 0
total_links = len(results)
link_counter = 0

for (codigo,) in results:
    link = link_prefix + codigo
    driver.execute_script(f"window.open('{link}', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    # pausa de 10 segundos
    time.sleep(10) 
    # mudar o contexto para o iframe
    iframe = driver.find_elements(By.TAG_NAME, "iframe")[0]
    driver.switch_to.frame(iframe)


    # encontrar a tag do botão
    button = driver.find_element(By.TAG_NAME, 'button')
    # clicar no botão
    button.click()
    # mudar o contexto de volta para o contexto principal
    driver.switch_to.default_content()
    # switch back to the main window
    driver.switch_to.window(driver.window_handles[0])
    # Apaga o link
    cursor.execute("DELETE FROM Codigo WHERE codigos = '{}'".format(codigo))
    cnx.commit()
    link_count += 1
    if link_count == total_links:
        driver.quit()

    link_counter += 1
    if link_counter == 20:
        driver.delete_all_cookies()
        link_counter = 0
    
cursor.close()
cnx.close()


