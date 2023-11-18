import requests
from bs4 import BeautifulSoup
import lxml
import openpyxl

user = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
header = {"User-Agent": user}
s = requests.Session()

book = openpyxl.Workbook()

sheet = book.active

sheet["A1"] = "Title company"
sheet["B1"] = "sum"
sheet["C1"] = "coments"
count = 2
with open("televizory.txt", "a", encoding="utf-8") as file:
    for i in range(1, 26):
        print(f"page = {i}")
        url = f"https://allo.ua/ua/televizory/page={i}"
        res = s.get(url, headers=header)

        # if res.status_code == 200:
        soup = BeautifulSoup(res.text, "lxml")

        all_products = soup.find_all("div", class_="product-card")
            # print(all_products)
            # print(len(all_products))
        for product in all_products:
            if product.find("div", class_="v-pb__old"):
                title = product.find("a", class_="product-card__title")
                price = product.find("span", class_="sum")
                try:
                    otz = product.find("span", class_="review-button__text review-button__text--count")
                except AttributeError:
                    otz.append(0)
                    print("Нема видгуку")

                file.write(f"{title.text} Сума {price.text} Вiдгуки {otz.text}\n")
                sheet[f"A{count}"] = title.text
                sheet[f"B{count}"] = price.text
                sheet[f"C{count}"] = otz.text
                count += 1

            print(product)


book.save("televizory.xlsx")

book.close()