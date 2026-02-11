from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class GooglePage(BasePage):

    SEARCH_INPUT = (By.NAME, "q")
    #RESULTS = (By.CSS_SELECTOR, "div[data-testid='result']")
    #RESULTS = (By.XPATH, "(//h3)[1]")
    RESULTS = (By.XPATH, "//h3")

    def search(self, text):
        search_box = self.wait_for_element(self.SEARCH_INPUT)
        search_box.send_keys(text)
        search_box.submit()

    def results_are_displayed(self):
        results = self.wait.until(
            lambda d: d.find_elements(*self.RESULTS)
        )
        return len(results) > 0

    def result_contains_word(self, word: str) -> bool:
       titles = self.wait.until(
           lambda d: d.find_elements(*self.RESULTS)
       )

       for title in titles:
           if word.lower() in title.text.lower():
               return True

       return False