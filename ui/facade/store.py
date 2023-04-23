""" Store facade containing all operations that can be done in Store page"""

import logging
from selenium.common.exceptions import NoSuchElementException
from common.utils.logger import configure_log
from common.config.config import Config
from ui.common.click import Click
from ui.common.input import Input
from ui.locators.cart import Cart
from ui.locators.store import Store
from ui.locators.cart import Cart
from ui.common.wait import WaitHelper
from ui.common.element import Element
from ui.common.dropdown import Dropdown




LOG = configure_log(logging.INFO, __name__, "login_facade.log")

class Store_facade:
    """
    Store Facade
    """
    def __init__(self, rest, driver):
        """
        constructor class for Store facade
        Args:
            driver: webdriver object
        """
        self.driver = driver
        self.input = Input(self.driver)
        self.click = Click(self.driver)
        self.wait = WaitHelper(self.driver, timeout=30)
        self.element = Element(driver)
        self.dropdown = Dropdown(driver)
        self.rest = rest

    def add_to_cart(self, product_name=None, quantity=None):
        """
        Adds to the cart
        Args:
            product_name: Defaults to None, when None, raises Exception
            quantity: Defaults to None, when None, raises Exception
        """
        if product_name is None:
            raise Exception("Product name is must for to add to cart")
        if quantity is None:
            raise Exception("Quantity is must for add to cart")
        product_ele = (Store.SPECIFIC_PRODUCT_SELECT_QUANTITY_DROPDOWN[0], 
                       Store.SPECIFIC_PRODUCT_SELECT_QUANTITY_DROPDOWN[1].format(product_name=product_name))
        quantity_ele = (Store.CHOOSE_QUANTITY[0], 
                        Store.CHOOSE_QUANTITY[1].format(product_quantity=quantity))
        self.dropdown.select_by_label_xpath(product_ele, quantity_ele)
        self.click.button(Store.ADD_TO_CART)
        self.element.is_element_present(Store.ADD_TO_CART_SUCCESS_MSG)
    
    def navigate_to_cart(self):
        """
        Navigates to Cart page
        """
        self.click.button(Store.CART)
    
    def navigate_to_store(self):
        """
        Navigates to Store page
        """
        self.click.button(Store.STORE)

    def navigate_to_logout(self):
        """
        Navigates to logout page
        """
        self.click.button(Store.LOG_OUT)



        
        