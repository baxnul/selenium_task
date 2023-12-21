#!/usr/bin/env python
# coding: utf-8

# In[124]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time
import os
import requests
import re
import math


# In[125]:


def convert_bytes_to_mb(bytes_size):
            mb_size = bytes_size / (1024.0 * 1024)
            return round(mb_size, 2)


# In[126]:


def test_task1():
    with webdriver.Chrome() as browser:
        link = "https://sbis.ru/"
        browser.implicitly_wait(30) # искать каждый элемент в течение 5 секунд
        browser.get(link)
        
        overlay = WebDriverWait(browser, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "preload-overlay")))
        
        # overlay исчез, можено кликнуть на ссылку
        link_contacts = browser.find_element(By.XPATH, '//a[@href="/contacts"]')
        link_contacts.click()
        
        
        tensor_img = browser.find_element(By.XPATH, '//*[@alt="Разработчик системы СБИС — компания «Тензор»"]')
        tensor_img.click()
        
        
        
        overlay = WebDriverWait(browser, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "preload-overlay")))
        browser.switch_to.window(browser.window_handles[-1]) # Переключиться на последнюю вкладку
        elements_with_text = browser.find_elements(By.XPATH, "//*[contains(text(), 'Сила в людях')]")
        
        # Проверяем, есть ли хотя бы один элемент с указанным текстом
        assert elements_with_text, "Текст 'Сила в людях' не найден на странице"
        
        
        link_about = browser.find_element(By.XPATH, '//a[@href="/about"]')
        browser.execute_script("return arguments[0].scrollIntoView(true);", link_about)
        link_about.click()
        
        overlay = WebDriverWait(browser, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "preload-overlay")))
        
        browser.switch_to.window(browser.window_handles[-1]) # Переключиться на новую вкладку
        # elements = browser.find_element(By.CSS_SELECTOR, ".tensor_ru-About__block3-image.new_lazy.loaded")
        elements = browser.find_elements(By.CSS_SELECTOR, ".tensor_ru-About__block3-image-wrapper>img")
        
        # # Получаем значения атрибутов width и height
        width = None
        height = None
        for element in elements:
            width_value = element.get_attribute("width")
            height_value = element.get_attribute("height")
            if width == None and height == None:
                width = width_value
                height = height_value
            assert width == width_value and height == height_value, "В разделе \"Работаем\" картинки разных размеров"


# In[127]:


def test_task2():
    with webdriver.Chrome() as browser:
        link = "https://sbis.ru/"
        browser.implicitly_wait(5) # искать каждый элемент в течение 5 секунд
        browser.get(link)
    
    
        overlay = WebDriverWait(browser, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "preload-overlay"))) # overlay исчез, можено кликнуть на ссылку
        
        link_contacts = browser.find_element(By.XPATH, '//a[@href="/contacts"]') # Перейти на страницу Контакты
        link_contacts.click()
    
        time.sleep(2)
        contact_url_before = browser.current_url # URL до смены региона
    
        list_partner = browser.find_element(By.XPATH, '//*[@name="viewContainer"]')
        text_before_reg = browser.find_element(By.ID, 'city-id-2').text # Регион до внесения изменений
        assert list_partner, "Список партнеров на странице не найден"
    
        current_region = browser.find_element(By.CSS_SELECTOR, ".sbis_ru-Region-Chooser__text.sbis_ru-link")
        assert current_region, "Ваш Регион на странице не определился"
        overlay = WebDriverWait(browser, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "preload-overlay"))) # overlay исчез, можено кликнуть на ссылку
        current_region.click()
        
        edit_region = browser.find_element(By.XPATH, '//*[@title="Камчатский край"]')
        edit_region.click()
        
        time.sleep(5)
        find_new_region = browser.find_element(By.CSS_SELECTOR, ".sbis_ru-Region-Chooser__text.sbis_ru-link").text
        assert str(find_new_region) == 'Камчатский край', "Регион Камчатский край не выбран"
    
        text_after_reg = browser.find_element(By.ID, 'city-id-2').text # Регион после внесения изменений
        assert text_before_reg != text_after_reg, "Во вкладке партнеры Регион не изменился"
    
        contact_url_after = browser.current_url # URL после смены региона
        url_find = contact_url_before.find(contact_url_after) # Текущий URL есть в старом URL?
        assert url_find == -1, "URL не изменился после смены Региона"
        
        assert str(find_new_region) in browser.title, "Title на странице не поменялся"


# In[128]:


def test_task3():
    with webdriver.Chrome() as browser:
        link = "https://sbis.ru/"
        browser.implicitly_wait(10) # искать каждый элемент в течение 10 секунд
        browser.get(link)
        
        overlay = WebDriverWait(browser, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "preload-overlay")))
        transit_download = browser.find_element(By.XPATH, '//a[@href="/download?tab=ereport&innerTab=ereport25"]')
        browser.execute_script("return arguments[0].scrollIntoView(true);", transit_download)
        transit_download.click()
    
        tab_buttons = browser.find_elements(By.CLASS_NAME, "controls-tabButton__overlay")
        time.sleep(10)
        tab_plugin = tab_buttons[1] # Выбираем ВТОРОЙ элемент "Сбис Плагин" из списка
        tab_plugin.click()
    
        windows_window = browser.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/span")
        windows_window.click()
    
        download_file = browser.find_element(By.XPATH, '//a[@href="https://update.sbis.ru/Sbis3Plugin/master/win32/sbisplugin-setup-web.exe"]') # Скачать файл для windows 
        text_weight_file_url = download_file.text # Получаем текст с размером файла написанный на сайте
        
        file_url = download_file.get_attribute("href")# Получаем URL файла
    
        current_dir = os.path.abspath(os.path.dirname("__file__"))    # получаем путь к директории текущего исполняемого файла 
        
        file_name = os.path.basename(file_url) # Определяем имя файла по URL
    
        save_path =  f'{current_dir}/{file_name}' # Определяем путь для сохранения файла (в текущей директории)
        print(f'save path: {save_path}')
        
        response = requests.get(file_url) # Скачиваем файл
        assert response.status_code == 200, 'Не удалось скачать файл'
    
        # Сохраняем файл
        with open(save_path, 'wb') as file:
            file.write(response.content)
            print(f"Файл успешно сохранен в {save_path}")
        # time.sleep(10)
    
        reg = r'\d+.\d+' 
        match_text_fsize_url = (re.search(reg, text_weight_file_url)).group(0) # Получаем Вес при помощи регулярки
        file_size_bytes = os.path.getsize(save_path) # Получаем размер скаченного файла в байтах
    
        file_size_mb = convert_bytes_to_mb(file_size_bytes)
        assert float(match_text_fsize_url) == float(file_size_mb), "Размер файла указанный на Сайте и размер скаченного файла отличаются"

