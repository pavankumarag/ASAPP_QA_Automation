""" Login facade containing all operations that can be done in login page"""

import logging
from common.utils.logger import configure_log
from common.config.config import Config
from ui.common.click import Click
from ui.common.input import Input
from ui.locators.login import Login
from ui.locators.store import Store
from ui.common.wait import WaitHelper
from ui.common.element import Element
from selenium.common.exceptions import NoSuchElementException
from api.facade.user_operations import UserActions
from common.utils.exceptions import HTTPError

LOG = configure_log(logging.INFO, __name__, "login_facade.log")

class Login_facade:
    """
    Login Facade
    """
    def __init__(self, driver):
        """
        constructor class for login facade
        Args:
            driver: webdriver object
        """
        self.driver = driver
        self.input = Input(self.driver)
        self.click = Click(self.driver)
        self.wait = WaitHelper(self.driver, timeout=30)
        self.element = Element(driver)

    def login(self, username=None, password=None):
        """
        Logs in to the store
        Args:
            username: Defaults to None, when none, reads from config json
            password: Defaults to None, when none, reads from config json
        """
        LOG.info("logging in to the store")
        config = Config()
        if username is None:
            username = config.get_config()["login"]["USERNAME"]
            check_for_registered = True
        if password is None:
            password = config.get_config()["login"]["PASSWORD"]
            check_for_registered = True
        if check_for_registered:
            user = UserActions()
            try:
                LOG.info("Registering the user {}".format(username))
                user.register(username=username, password=password)
            except HTTPError as e:
                LOG.info(e)
        self.input.textbox(username, Login.USERNAME)
        self.input.textbox(password, Login.PASSWORD)
        self.click.button(Login.LOGIN_BUTTON)
        try:
            self.wait.wait_until_element_present(Store.STORE)
            if self.element.is_element_present(Store.STORE):
                LOG.info("login successful")
                return True
        except NoSuchElementException:
            return False


    def register(self):
        """
        Register new user
        """
        pass

            
		
