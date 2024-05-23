from dataclasses import dataclass
import csv
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By


@dataclass
class Product:
    title: str
    price: float


@dataclass
class Amazon:

    def get_data(self, name: str) -> list[Product]:
        count = 1
        page = 0
        add_page = 15
        maximum = 15
        product_list = []
        options = Options()
        service = Service(executable_path="./resources/geckodriver.exe")
        browser = Firefox(service=service, options=options)
        browser.maximize_window()
        while len(product_list) < maximum:
            try:
                if count > add_page or page == 0:
                    count = 1
                    page = page + 1
                    url = f"https://www.amazon.com.br/s?k={name}&page={str(page)}"
                    browser.get(url=url)
                    browser.set_page_load_timeout(100)
                for i in range(1, 3):
                    try:
                        title_path = f"/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{str(count+1)}]/div/div/span/div/div/div[{3 if count==1 else 2}]/div[{i}]/h2/a/span"
                        title = browser.find_element(by=By.XPATH, value=title_path)
                        break
                    except Exception as e:
                        pass
                title_text = title.get_attribute("innerHTML").splitlines()[0]
                price_whole_path = f"/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{str(count+1)}]/div/div/span/div/div/div[{3 if count==1 else 2}]/div[{4 if i == 2 else 3}]/div/div[1]/a/span/span[2]/span[2]"
                price_decimal_path = f"/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{str(count+1)}]/div/div/span/div/div/div[{3 if count==1 else 2}]/div[{4 if i == 2 else 3}]/div/div[1]/a/span/span[2]/span[3]"

                price_whole = browser.find_element(
                    by=By.XPATH, value=price_whole_path
                ).text.replace(".", "")
                price_decimal = browser.find_element(
                    by=By.XPATH, value=price_decimal_path
                ).get_attribute("innerHTML")

                price = float(price_whole + "." + price_decimal)
                product = Product(title_text, price)
                product_list.append(product)
                count += 1

            except Exception as e:
                print(e)
                break
        browser.close()
        return product_list


if __name__ == "__main__":
    amazon = Amazon()
    products = amazon.get_data("moto g53")
    with open("products.csv", "w", newline="", encoding="utf-8") as file:
        data = csv.writer(file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for product in products:
            data.writerow([product.title, product.price])
