import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.google_page import GooglePage



def test_google_title(driver):
    driver.get("https://www.google.com")
    assert "Google" in driver.title