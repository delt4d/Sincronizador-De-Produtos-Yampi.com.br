from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

login = "your_email"
password = "your_password"

def abrir_navegador() -> WebDriver:
    print("Abrindo navegador")
    nav = webdriver.Chrome()
    return nav

def efetuar_login(nav: WebDriver):
    # entra na página de login
    nav.get("https://app.yampi.com.br/login")

    # preenche o formulário de login
    sleep(1)
    input_email = nav.find_element(By.NAME, "email")
    input_email.send_keys(login)
    input_password = nav.find_element(By.NAME, "password")
    input_password.send_keys(password)

    # loga no sistema
    nav.execute_script("document.querySelector('form button').click()")

def obter_links_produtos(nav: WebDriver, page: int) -> list[str]:
    nav.get(f"https://app.yampi.com.br/catalog/products?limit=10&page={page}")
    sleep(3)

    # adiciona classe {itens-links-navegar} aos links de cadaproduto
    print("executando script...")
    nav.execute_script("[...document.querySelectorAll('main table tr td:nth-child(4) a')].forEach(el => el.classList.add('itens-links-navegar'))")

    # encontra os elementos à partir da classe
    sleep(1)
    links = [*map(lambda item : item.get_attribute('href'), nav.find_elements(By.CLASS_NAME, "itens-links-navegar"))] # o map é passado para uma lista, pq ele é um iterador (trabalha on demand)
    print(f"Os links são: {links}")

    return links


def main():
    # inicia o navegador
    nav = abrir_navegador()

    # efetua o login
    efetuar_login(nav)
    sleep(4)

    # obtém a primeira página de produtos
    page = 1
    links = obter_links_produtos(nav, page)

    sleep(1)
    links_paginas = nav.find_elements(By.CLASS_NAME, "number")
    numero_paginas = int(links_paginas[-1].text)

    print(f"O número de páginas é: {numero_paginas}")

    # para cada página
    while page <= numero_paginas:
        # para cada link na página
        for link in links:
            # entra no link
            print(f"abrindo link ...{link}")
            nav.get(link)

            # sincroniza o produto
            sleep(6)
            print("sincronizando produto...")
            nav.execute_script("document.querySelectorAll('button[type=submit]')[5].click()")
            sleep(3.5)

        # faz o mesmo para outra página
        page += 1
        links = obter_links_produtos(nav, page)

    print("FINALIZADO.")
    nav.close()

if __name__ == '__main__':
    main()