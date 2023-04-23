"""Locators for store page"""
from selenium.webdriver.common.by import By

class Store:
    STORE = By.XPATH, "//span[text()='Store']"
    CART = By.XPATH, "//span[text()='Cart']"
    LOG_OUT = By.XPATH, "//span[text()='Log Out']"
    SPECIFIC_PRODUCT_SELECT_QUANTITY_DROPDOWN = By.XPATH, "//div[@data-test-name='product-card']//h2[text()='{product_name}']/../../..//input/../div"
    CHOOSE_QUANTITY = By.XPATH, "//li[@data-value='{product_quantity}']"
    ADD_TO_CART = By.XPATH, "//span[text()='Add to Cart']"
    ADD_TO_CART_SUCCESS_MSG = By.XPATH, "//span[text()='Product Added to Cart']"
    ADD_TO_CART_VERIFY = By.XPATH, "//input[@value='{quantity}']"