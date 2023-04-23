"""Cart Facade"""
from selenium.common.exceptions import NoSuchElementException
from ui.common.element import Element
from ui.locators.cart import Cart

class Cart_facade:
    """
    Cart Facade
    """
    def __init__(self, driver):
        """
        constructor class for Cart facade
        Args:
            driver: webdriver object
        """
        self.driver = driver
        self.element = Element(driver)

    def get_current_quantity_in_cart(self, product_name=None):
        """
        Gets the current quantity of {product_name} from cart
        Args:
            product_name: Defaults to None, when None, raises exception
        Returns:
            current_value_in_cart: Current value in cart
        """
        if product_name is None:
            raise Exception("Product name is needed to get quantity in cart")
         
        product_ele_in_cart = (Cart.CURRENT_PRODUCT_QUANTITY[0],
                               Cart.CURRENT_PRODUCT_QUANTITY[1].format(product_name=product_name))
        try:
            current_value_in_cart = self.element.get_text(product_ele_in_cart)
        except NoSuchElementException:
            current_value_in_cart = 0
            return current_value_in_cart
        return current_value_in_cart