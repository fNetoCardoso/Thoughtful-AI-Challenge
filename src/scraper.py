from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
import os
import re
from utils import save_to_excel, download_image

class NewsScraper:
    def __init__(self, config, button_selector, input_selector, select_id_selector, result_selector, title_selector, query_search, filter_option, submit_search_button_selector, description_selector, date_selector, image_selector):
        self.browser = Selenium()
        self.config = config
        self.browser.set_download_directory(config.OUTPUT_DIR)
        self.button_selector = button_selector
        self.input_selector = input_selector
        self.select_id_selector = select_id_selector
        self.result_selector = result_selector
        self.title_selector = title_selector
        self.query_search = query_search
        self.filter_option = filter_option
        self.submit_search_button_selector = submit_search_button_selector
        self.description_selector = description_selector
        self.date_selector = date_selector
        self.image_selector = image_selector
        self.news = []
    
    def open_site(self):
        self.browser.open_available_browser(self.config.BASE_URL)
        self.browser.set_window_size(1920, 1080)
        html_code = self.browser.get_source()
        with open('teste.txt', 'w', encoding='utf-8') as file:
            file.write(html_code)
    
    def search_news(self, phrase):
        self.browser.input_text("css:input[name='q']", phrase)
        self.browser.press_keys("css:input[name='q']", "RETURN")

    def click_search_button(self):
        try:
            wait = WebDriverWait(self.browser.driver, 15)
            button_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.button_selector)))
            
            button_element.click()
            
            print("Botão de busca clicado com sucesso.")
            
        except Exception as e:
            print(f"Erro ao clicar no botão de busca: {e}")
    
    def submit_search_button(self):
        try:
            wait = WebDriverWait(self.browser.driver, 15)
            button_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.submit_search_button_selector)))
            
            button_element.click()
            
            print("Botão de busca clicado com sucesso.")
            
        except Exception as e:
            print(f"Erro ao clicar no botão de busca: {e}")

    def fill_search_input(self):
        try:
            wait = WebDriverWait(self.browser.driver, 20)
            input_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.input_selector)))
            
            input_element.clear()
            input_element.send_keys(self.query_search)
            
            print("Campo de entrada preenchido com sucesso.")
        except Exception as e:
            print(f"Erro ao preencher o campo de entrada: {e}")

    def select_option(self):
        try:
            wait = WebDriverWait(self.browser.driver, 20)
            select_element = wait.until(EC.visibility_of_element_located((By.ID, self.select_id_selector)))
            
            select = Select(select_element)
            
            select.select_by_value(self.filter_option)
            
            print(f"Opção '{self.filter_option}' selecionada com sucesso.")
        except Exception as e:
            print(f"Erro ao selecionar a opção: {e}")

    def get_all_results(self):
        try:
            wait = WebDriverWait(self.browser.driver, 20)
            parent_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.result_selector)))
            
            children_elements = parent_element.find_elements(By.XPATH, "./*")
            
            # Itera e imprime informações sobre os filhos encontrados
            print(f"Encontrados {len(children_elements)} filhos.")
            for index, child in enumerate(children_elements):
                if child.tag_name.lower() == "article":
                    title = self.get_title(index, child)
                    description = self.get_description(index, child)
                    date = self.get_date(index, child)
                    img = self.get_image(index, child)
                    object_new = self.create_object_new(title, description, date, img)
                    self.add_to_array_news(object_new)
                    
        except Exception as e:
            print(f"Erro ao obter filhos: {e}")

    def get_title(self, index, child):
        try:
            title_element = child.find_element(By.CSS_SELECTOR, self.title_selector)
            
            a_element = title_element.find_element(By.TAG_NAME, "a")
            
            span_element = a_element.find_element(By.TAG_NAME, "span")
            span_text = span_element.text
            print(f"Filho {index + 1}:")
            print(f"Conteúdo do <span>: {span_text}")
            return span_text
            
        except Exception as e:
            print(f"Erro ao processar o filho {index + 1}: {e}")
            return ''

    def get_description(self, index, child):
        try:
            description_element = child.find_element(By.CSS_SELECTOR, self.description_selector)
            
            p_element = description_element.find_element(By.TAG_NAME, "p")    
            p_text = p_element.text
            print(f"Filho {index + 1}:")
            print(f"Conteúdo do <p>: {p_text}")
            return p_text

        except Exception as e:
            print(f"Erro ao processar o filho {index + 1}: {e}")
            return ''

    def get_date(self, index, child):
        try:
            date_element = child.find_element(By.CSS_SELECTOR, self.date_selector)
            div_element = date_element.find_element(By.TAG_NAME, "div")
            children = div_element.find_elements(By.TAG_NAME, "span")
            if children:
                date_text = children[1].text
                print(f"Filho {index + 1}:")
                print(f"Conteúdo do <span>: {date_text}")
                return date_text
            return ''
        except Exception as e:
            print("Data não encontrada.")
            return ''

    def get_image(self, index, child):
        try:
            image_element = child.find_element(By.CSS_SELECTOR, self.image_selector)
            div_element = image_element.find_element(By.TAG_NAME, "div")
            responsive_div_element = div_element.find_element(By.TAG_NAME, "div")
            img_element = responsive_div_element.find_element(By.TAG_NAME, "img")
            image = img_element.get_attribute("src")
            print(f"Filho {index + 1}:")
            print(f"Conteúdo do <img>: {image}")
            return image
        except Exception as e:
            print("Imagem não encontrada.")
            return ''
        
    def create_object_new(self, title, description, date, img):
        obj_new = {
            'title':title,
            'description':description,
            'date':date,
            'picture_filename':img
        }
        return obj_new
    
    def add_to_array_news(self, obj):
        self.news.append(obj)

    def run(self):
        self.open_site()
        self.click_search_button()
        self.fill_search_input()
        self.submit_search_button()
        self.select_option()
        self.get_all_results()
        save_to_excel(self.news, './output')
    
    def close(self):
        self.browser.close_browser()
