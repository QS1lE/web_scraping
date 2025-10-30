# Используя Selenium распарсить электронную почту (получить данные о входящих и отправленных сообщениях)


from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import  time
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
from datetime import datetime


driver = webdriver.Firefox()


try:
    # Открытие страницы входа Mail.ru
    driver.get('https://mail.ru/')
    
    # Ожидание появления кнопки входа и клик по ней
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//a[(@href='//account.mail.ru/login?from=main&rf=auth.mail.ru&app_id_mytracker=58519')]"))
    ).click()
    
    time.sleep(5)
    
    # Поле логина и запись данных в него
    login_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "email")))
    print("Поле логина найдено по ID")

    my_login = "Login" #Cюда нужно ввести логин

    login_field.clear()
    login_field.send_keys(my_login)
    print(f"Введен логин: {my_login}")

    time.sleep(5)

    # Нажатие кнопки - Войти
    continue_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='continue-button']"))
    )
    continue_btn.click()
    print("Кнопка 'Войти' нажата")

    time.sleep(5)

    # Нажатие кнопки - Войти другим способом
    change_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='bind-screen-vkid-change-restore-type-btn']"))
    )
    change_btn.click()
    print("Кнопка 'Войти другим способом' нажата")

    time.sleep(5)

    # Нажатие кнопки - Пропустить
    cancel_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='vkid-bind-extra-screen-vkid_is_not_vkontakte-cancel']"))
    )
    cancel_btn.click()
    print("Кнопка 'Пропустить' нажата")

    time.sleep(5)

    # ЖДЕМ И ПЕРЕКЛЮЧАЕМСЯ В IFRAME С ПАРОЛЕМ
    password_iframe = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "pass"))
    )
    print("Iframe с паролем найден")
    

    # Переключаемся в iframe
    driver.switch_to.frame(password_iframe)
    print("Переключились в iframe")

    
    # Заполнение паароля и нажатие кнопки - войти
    password_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "password")))
    print("Поле pass найдено по ID")

    my_pass = "password" #Cюда нужно ввести пароль

    password_field.clear()
    password_field.send_keys(my_pass)
    print(f"Введен пароль")

    time.sleep(5)


    # Возвращаемся в основной контент
    driver.switch_to.default_content()
    print("Вернулись в основной контент")

    submit_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='submit']"))
    )
    submit_btn.click()
    print("Кнопка 'Войти' нажата после пароля")


    time.sleep(5)
    
    # Парсинг отправленных сообщении
    print("Переходим в отправленные сообщения")
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/sent/')]"))
    ).click()
    time.sleep(3)

    sent_messages = driver.find_elements(By.CSS_SELECTOR, '.llc')
    # Или альтернативный селектор:
    # sent_messages = driver.find_elements(By.CSS_SELECTOR, '.js-letter-list-item')

    print(f'Количество отправленных сообщений равно {len(sent_messages)}')

    messages_list = []

    for i, message in enumerate(sent_messages):
        try:
            # Получаем полный текст сообщения
            full_text = message.text
            print(f"Сообщение {i+1}: {full_text}")
            
            # Извлекаем отдельные части (если нужно)
            lines = full_text.split('\n')
            recipient = lines[0] if len(lines) > 0 else "Неизвестно"
            subject = lines[1] if len(lines) > 1 else "Без темы" 
            date = lines[2] if len(lines) > 2 else "Дата не указана"
            
            messages_list.append({
                'recipient': recipient,
                'subject': subject,
                'date': date,
                'href': message.get_attribute('href'),
            })
            
        except Exception as e:
            print(f"Ошибка при обработке сообщения {i+1}: {str(e)}")
            # Сохраняем хотя бы базовую информацию
            messages_list.append({
                'text_preview': message.text
            })
            continue

    # Сохраняем в файл
    with open('sent_messages_simple.json', 'w', encoding='utf-8') as f:
        json.dump(messages_list, f, ensure_ascii=False, indent=2)

    print(f"Список сообщений сохранен в sent_messages_simple.json")
    print(f"Успешно обработано {len(messages_list)} из {len(sent_messages)} сообщений")



    # Парсинг входящих сообщении
    print("Переходим во входящие сообщения")

    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/inbox/')]"))
    ).click()
    time.sleep(3)

    inbox_messages = driver.find_elements(By.XPATH, '//a[contains(@href, "/inbox/")]')
    # inbox_messages = driver.find_elements(By.XPATH, '//a[contains(@href, "/inbox/") and @data-uidl-id]')
    print(f'Количество входящих сообщений равно {len(inbox_messages)}')

    messages_list = []

    for i, message in enumerate(inbox_messages):
        try:
            # Получаем полный текст сообщения
            full_text = message.text
            print(f"Сообщение {i+1}: {full_text}")
            
            # Извлекаем отдельные части
            lines = full_text.split('\n')
            sender = lines[0] if len(lines) > 0 else "Неизвестно"
            subject = lines[1] if len(lines) > 1 else "Без темы" 
            preview = lines[2] if len(lines) > 2 else ""
            date = lines[3] if len(lines) > 3 else "Дата не указана"
            
            # Получаем атрибуты
            href = message.get_attribute('href')
            data_id = message.get_attribute('data-uidl-id')
            
            messages_list.append({
                'sender': sender,
                'subject': subject,
                'preview': preview,
                'date': date,
                'href': href
            })
            
        except Exception as e:
            print(f"Ошибка при обработке сообщения {i+1}: {str(e)}")
            # Сохраняем хотя бы базовую информацию
            messages_list.append({
                'text_preview': message.text,
            })
            continue

    # Сохраняем в файл
    with open('inbox_messages.json', 'w', encoding='utf-8') as f:
        json.dump(messages_list, f, ensure_ascii=False, indent=2)

    print(f"Список входящих сообщений сохранен в inbox_messages.json")
    print(f"Успешно обработано {len(messages_list)} из {len(inbox_messages)} сообщений")

    
    time.sleep(3)

finally:
    # Закрытие браузера
    driver.quit()

