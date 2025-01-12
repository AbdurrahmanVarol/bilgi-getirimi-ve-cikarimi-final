from scrapers.IScraper import IScraper
from scrapers.selenium.TMDBSeleniumScraper import TMDBSeleniumScraper
import os
import pandas as pd


def isDataExist(fileName="data.csv"):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, fileName)
    return os.path.isfile(file_path)


def saveToCsv(data, fileName="data.csv"):
    df = pd.DataFrame(data)
    current_directory = os.getcwd()
    json_file_path = os.path.join(current_directory, fileName)
    df.to_csv(json_file_path, index=False)


def checkData():
    if not isDataExist():
        print("Veriler bulunamadı. Veriler yükleniyor...")
        scraper: IScraper = TMDBSeleniumScraper()
        data = scraper.getData(10)
        saveToCsv(data)
        print("Veriler kaydedildi.")
    else:
        print("veriler bulundu")


if __name__ == "__main__":
    checkData()
