import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class TMDBSeleniumScraper:
    def __init__(self):
        self.driver = self._getDriver()
        self.driver.maximize_window()
        self.url = "https://www.themoviedb.org/movie"
        self.movies_data = []

    def _getDriver(self):
        return webdriver.Chrome()

    def _navigateToUrl(self):
        self.driver.get(self.url)
        time.sleep(5)

    def _acceptCookies(self):
        try:
            cookie_button = self.driver.find_element(
                By.CSS_SELECTOR, "#onetrust-close-btn-container > button"
            )
            cookie_button.click()
            time.sleep(1)
        except Exception as e:
            print(f"Cookies button error: {e}")

    def _changeLanguageToEn(self):
        try:
            print("worked")
            languageButton = self.driver.find_element(
                By.CSS_SELECTOR,
                "body > div.page_wrap.movie_wrap > header > div.content > div > div.flex > ul > li.translate > div",
            )
            languageButton.click()
            time.sleep(1)

            LanguageOptions = self.driver.find_element(
                By.XPATH,
                '//*[@id="default_language_popup_label"]/span[2]/button',
            )
            LanguageOptions.click()
            time.sleep(1)

            input = self.driver.find_element(
                By.XPATH,
                "/html/body/div[19]/div/div/div[4]/div/div/div[1]/span/input",
            )
            input.send_keys("en-US")
            time.sleep(1)
            input.send_keys(Keys.ENTER)
            time.sleep(1)

            reloadButton = self.driver.find_element(
                By.XPATH,
                "/html/body/div[19]/div/div/div[1]/section/div/div/form/fieldset/p/a",
            )
            reloadButton.click()
            time.sleep(1)
        except Exception as e:
            print(e)

    def _clickLoadMore(self):
        try:
            load_more_button = self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/main/section/div/div/div/div[2]/div[2]/div/section/div/div/div[24]/p/a",
            )
            load_more_button.click()
            time.sleep(3)
        except Exception as e:
            print(f"Load more button error: {e}")

    def _scrollAndCollectLinks(self, limit):
        movie_links = []
        while len(movie_links) < limit:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(2)

            movies = self.driver.find_elements(By.CSS_SELECTOR, ".card.style_1 a.image")
            for movie in movies:
                link = movie.get_attribute("href")
                if link not in movie_links:
                    movie_links.append(link)

        return movie_links[:limit]

    def _extractMovieData(self, link):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(link)
        time.sleep(2)

        try:
            title = self.driver.find_element(By.CSS_SELECTOR, "h2 > a").text
            release_date = self.driver.find_element(By.CSS_SELECTOR, "h2 > span").text
            overview = self.driver.find_element(By.CLASS_NAME, "overview").text
            release = self.driver.find_element(By.CLASS_NAME, "release").text
            genres = self.driver.find_element(By.CLASS_NAME, "genres").text
            runtime = self.driver.find_element(By.CLASS_NAME, "runtime").text

            return {
                "title": title,
                "releaseDate": release_date.replace("(", "").replace(")", ""),
                "overview": overview,
                "release": release,
                "genres": genres,
                "runtime": runtime,
            }
        except Exception as e:
            print(f"Error while processing {link}: {e}")
            return None
        finally:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

    def getData(self, limit):
        try:
            self._navigateToUrl()
            self._acceptCookies()
            self._changeLanguageToEn()
            self._clickLoadMore()

            movie_links = self._scrollAndCollectLinks(limit)
            for link in movie_links:
                movie_data = self._extractMovieData(link)
                if movie_data:
                    self.movies_data.append(movie_data)
        except Exception as e:
            print(f"Scraping error: {e}")
        finally:
            self.driver.quit()
            return self.movies_data
