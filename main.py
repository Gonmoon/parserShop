import requests
import asyncio
from time import sleep
from bs4 import BeautifulSoup


# -----Avito-----
async def parseAvito(url: str, data: list) -> None:
    soup = BeautifulSoup(requests.get(url).text, features="lxml")
    for block in soup.find_all("div", class_="listing-item__about"):
        data.append("https://moto.av.by" + block.find("a", class_="listing-item__link").get("href"))

# -----Kufar-----
async def parseKufar(url:str, data:list) -> None:
    for link in BeautifulSoup(requests.get(url).text, features="html.parser").find_all("a"):
        data.append(link.get("href"))

async def parseData() -> list:
    data = []
    # -----Honda(Kufar)-----
    await parseKufar("https://auto.kufar.by/l/skuter-honda?cur=BYR", data)
    # -----Suzuki(Kufar)-----
    await parseKufar("https://auto.kufar.by/l/skuter-suzuki?cur=BYR", data)
    # -----Yamaha(Kufar)-----
    await parseKufar("https://auto.kufar.by/l/skuter-yamaha?cur=BYR", data)

    # -----Honda(Avito)-----
    await parseAvito("https://moto.av.by/scooter/honda", data)
    # -----Suzuki(Avito)-----
    await parseAvito("https://moto.av.by/scooter/suzuki", data)
    # -----Yamaha(Avito)-----
    await parseAvito("https://moto.av.by/scooter/yamaha", data)

    return data

def start():
    new_data = asyncio.run(parseData())
    with open("data.txt", "r+") as data_file:
        data = data_file.read().split("\n")
        # -----Сравнение-----
        if new_data != data:
            new_ads = list(set(new_data) - set(data))
            for item in new_ads:
                data_file.write(item + "\n")
                # requests.post("https://api.telegram.org/bot" + str(item))

if __name__ == "__main__":
    start()
