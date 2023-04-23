"""Locators for Cart page"""
from selenium.webdriver.common.by import By

class Cart:
    CURRENT_PRODUCT_QUANTITY= By.XPATH, "//td[text()='{product_name}']/../td[2]"
    BUY = By.XPATH, "//span[text()='BUY!']"
    BUY_SUCCESS_MSG = By.XPATH, "//h2[text()='Thank you!']"