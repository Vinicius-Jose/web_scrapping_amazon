import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def disconnect_wpp(browser: webdriver.Remote) -> None:
    # Open options menu
    browser.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/div/div/div[2]/div[3]/header/header/div/span/div/span/div[2]/div",
    ).click()
    time.sleep(1)
    # Click on disconnect
    browser.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/div/div/div[2]/div[3]/header/header/div/span/div/span/div[2]/span/div/ul/li[5]/div",
    ).click()
    # Confirm disconnect pop up
    browser.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/div/div/span[2]/div/div/div/div/div/div/div[3]/div/button[2]/div/div",
    ).click()
    time.sleep(2)
    browser.close()


def user_chat(browser: webdriver.Remote, name_user: str) -> None:
    chat_new = browser.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div[1]",
    )
    chat_new.click()
    user_chat = browser.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div",
    )
    user_chat.send_keys(name_user)

    try:
        user = browser.find_element(by=By.XPATH, value=f'//span[@title="{name_user}"]')
        user.click()
    except Exception as e:
        print(f"User {name_user} not found")
    finally:
        disconnect_wpp(browser)


if __name__ == "__main__":
    options = webdriver.FirefoxOptions()
    service = webdriver.FirefoxService(executable_path="./resources/geckodriver.exe")
    browser = webdriver.Firefox(service=service, options=options)
    browser.get("https://web.whatsapp.com")

    time.sleep(20)
    user_chat(browser, "Test")
