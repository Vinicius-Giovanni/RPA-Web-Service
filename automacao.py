from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def emitir_relatorio():

    driver = webdriver.Chrome()

    driver.get("https://google.com")

    time.sleep(5)

    print("Relatório emitido")

    driver.quit()