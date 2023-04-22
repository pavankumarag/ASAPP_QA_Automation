""" product operations facade like get_products, get_cart_info etc"""

from common.config.config import Config
from common.utils.rest import REST
from api.facade.user_operations import UserActions
from common.utils.common import generate_default_rest_config

class ProductActions:
    """ ProductActions class to implememt all product methods"""
    def __init__(self, rest=None):
        """
        Init method
        Args:
            rest: rest client to further use in all methods, defaults to None
        """
        self._config = Config()
        if rest is None:
            # This is to run these methods independent of pytest framework
            (username, password, port, ip) = generate_default_rest_config()
            self._rest = REST(ip=ip, username=username, password=password, port=port)
        else:
            self._rest = rest
        user_actions = UserActions(self._rest)
        user_actions.login()
    
    def get_all_products(self, username=None):
        """
        Get all the product in the inventory
        Args:
            username: Defaults to None, when none username in config json is used
         Returns:
            res: Response
        """
        if username is None:
            username = self._config.get_config()["login"]["USERNAME"]
        relative_url = self._config.get_config()['endpoints']["GET_PRODUCTS"].format(username=username)
        res = self._rest.get(relative_url=relative_url)
        return res
    
    def get_product(self,  username=None, product_name=None):
        """
        Get specific product in the inventory
        Args:
            username: Defaults to None, when none username in config json is used
            product_name: Defaults to None, when none, exception is raised
        Returns:
            res: Response
        """
        if username is None:
            username = self._config.get_config()["login"]["USERNAME"]
        if product_name is None:
            raise Exception("get_product methods needs specific product name to specify")
        relative_url = self._config.get_config()['endpoints']["GET_PRODUCTS"].format(username=username, product_name=product_name)
        res = self._rest.get(relative_url=relative_url)
        return res
    
    def get_current_cart_info(self, username=None):
        """
        Get currenrt cart info
        Args:
            username: Defaults to None, when none username in config json is used
         Returns:
            res: Response
        """
        if username is None:
            username = self._config.get_config()["login"]["USERNAME"]
        relative_url = self._config.get_config()['endpoints']["GET_CART"].format(username=username)
        res = self._rest.get(relative_url=relative_url)
        return res
    
    def add_to_cart(self, username=None, product_name=None, quantity=None):
        """
        Add product of specific quantity to the cart
        Args:
            username: Defaults to None, when none username in config json is used
            product_name: Defaults to None, when none, exception is raised
            quantity: Defaults to None, when none, exception is raised
        Returns:
            res: Response
        """
        if username is None:
            username = self._config.get_config()["login"]["USERNAME"]
        if product_name is None:
            raise Exception("add_to_cart methods needs specific product name to specify")
        if quantity is None:
            raise Exception("add_to_cart methods needs specific quantity to add")
        headers = {'Content-Type': 'application/json'}
        req = {"quantity": quantity}
        relative_url = self._config.get_config()['endpoints']["ADD_TO_CART"].format(username=username, product_name=product_name)
        res = self._rest.post(relative_url=relative_url, headers=headers, data=req)
        return res

    def remove_from_cart(self, username=None, product_name=None):
        """
        Remove product of specific quantity to the cart
        Args:
            username: Defaults to None, when none username in config json is used
            product_name: Defaults to None, when none, exception is raised
        Returns:
            res: Response
        """
        
        if username is None:
            username = self._config.get_config()["login"]["USERNAME"]
        if product_name is None:
            raise Exception("remove_from_cart methods need specific product name to specify")
        headers = {'Content-Type': 'application/json'}
        req = {}
        relative_url = self._config.get_config()['endpoints']["REMOVE_FROM_CART"].format(username=username, product_name=product_name)
        res = self._rest.post(relative_url=relative_url, headers=headers, data=req)
        return res
    
    def checkout_from_cart(self, username=None):
        """
        Checkout from the cart
        Args:
            username: Defaults to None, when none username in config json is used
        Returns:
            res: Response
        """
        if username is None:
            username = self._config.get_config()["login"]["USERNAME"]
        headers = {'Content-Type': 'application/json'}
        req = {}
        relative_url = self._config.get_config()['endpoints']["CHECKOUT_CART"].format(username=username)
        res = self._rest.post(relative_url=relative_url, headers=headers, data=req)
        return res
        