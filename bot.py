import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from googletrans import Translator
import requests


get_dir_path = os.getcwd()
chrome_options = Options()
chrome_options.add_argument(r'user-data-dir=' + os.path.join(get_dir_path, 'profile/wpp'))
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://web.whatsapp.com/')

agent = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.41 Safari/537.36'}
api_response = requests.get('https://editacodigo.com.br/index/api-whatsapp/i276fY5YuyRKL3gHFCNqieRJENUxEJFN', headers=agent)
api = api_response.text.split('.n.')
notification = api[3].strip()
msg_client = api[6].strip()
msg_box = api[5].strip()



def translate_text(text, src_lang='pt', dest_lang='en'):
    translator = Translator()
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated_text.text

def bot():
    try:
        # Clicar na notificação
        notification_ball = driver.find_elements(By.CLASS_NAME, notification)
        click_notification = notification_ball[-1]
        notification_action = webdriver.common.action_chains.ActionChains(driver)
        notification_action.move_to_element_with_offset(click_notification, 0, -20)
        notification_action.click()
        notification_action.perform()
        notification_action.click()
        notification_action.perform()
        
        all_msg = driver.find_elements(By.CLASS_NAME, msg_client)
        all_text_msg = [i.text for i in all_msg]
        msg = all_text_msg[-1]
        greeting_messages = ['oi', 'olá', 'boa tarde', 'boa noite', 'bom dia']
        
        time.sleep(1)
    
        text_to_translate = msg
        if msg.lower() in greeting_messages:
            apresentation = '\
                Olá, sou o Bot de Tradução PT-EN! Meu objetivo é ajudá-lo a traduzir frases do Português\
                para o Inglês de forma rápida e eficiente. Com minha ajuda, você poderá superar barreiras linguísticas e comunicar-se com pessoas que falam Inglês sem problemas.\
                Como usar:\nBasta digitar uma frase em Português que deseja traduzir para o Inglês.\
                Eu processarei sua frase e, em questão de segundos, apresentarei a tradução para você.\n\n \
                Sinta-se à vontade para usar o Bot de Tradução PT-EN sempre que precisar de assistência com traduções do Português para o Inglês\
                Estou aqui para ajudar a facilitar suas conversas internacionais e tornar sua experiência de comunicação mais agradável e acessível.\
                '
            text_field = driver.find_element(By.XPATH, msg_box)
            text_field.click()
            time.sleep(1)
            text_field.send_keys(apresentation, Keys.ENTER)      
            time.sleep(2)
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform() 
        else:
            translated_text = translate_text(text_to_translate, src_lang='pt', dest_lang='en')
            
            text_field = driver.find_element(By.XPATH, msg_box)
            text_field.click()
            time.sleep(1)
            text_field.send_keys(f"*texto Original*: {text_to_translate} \n *Texto Traduzido*: {translated_text}", Keys.ENTER)
            time.sleep(2)
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    except Exception as e:
        print("Erro:", str(e))
        print("Buscando novas notificações")

while True:     
    bot()
