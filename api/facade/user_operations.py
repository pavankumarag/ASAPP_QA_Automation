""" user operations facade like login, register, logout"""
import logging
import time
from common.config.config import Config
from common.utils.rest import REST
from common.utils.common import generate_default_rest_config
from common.utils.exceptions import HTTPError
from common.utils.logger import configure_log

LOG = configure_log(logging.DEBUG, __name__, "facade_user_operations_{}.log".format(time.time()))
config = Config()

class UserActions:
    """ UserActions class to implememt all user methods"""
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

    def login(self, username=None, password=None, check_register=False):
        """
        User login operation
        Args:
            username: Defaults to None, when None it will be read from config json file
            password: Defaults to None, when None it will be read from config json file
            check_register: check explicitly for register, defaults to False
        Returns:
            res: Response of REST post call
        """
        if username is None:
            username = self._config.get_config()["login"]["USERNAME"]
        if password is None:
            password = self._config.get_config()["login"]["PASSWORD"]
        if check_register:
            try:
                self.register(username=username, password=password)
            except HTTPError as e:
                LOG.info(e)
        headers = {'Content-Type': 'application/json'}
        relative_url = self._config.get_config()['endpoints']["LOGIN_USER"]
        req = {"username":username, "password": password}
        res = self._rest.post(relative_url=relative_url, headers=headers, data=req)
        return res

    def register(self, username=None, password=None):
        """
        User register operation
        Args:
            username: Defaults to None, when None it will be read from config json file
            password: Defaults to None, when None it will be read from config json file
        Returns:
            res: Response of REST post call
        """
        if username is None:
            username = self._config.get_config()["login"]["USERNAME"]
        if password is None:
            password = self._config.get_config()["login"]["PASSWORD"]
        headers = {'Content-Type': 'application/json'}
        relative_url = self._config.get_config()['endpoints']["REGISTER_USER"]
        req = {"username":username, "password": password}
        res = self._rest.post(relative_url=relative_url, headers=headers, data=req)
        return res

    def logout(self, username=None):
        """
        User logout operation
        Args:
            username: Defaults to None, when None it will be read from config json file
        Returns:
            res: Response of REST post call
        """
        if username is None:
            username = self._config.get_config()["login"]["USERNAME"]
        headers = {'Content-Type': 'application/json'}
        relative_url = self._config.get_config()['endpoints']["LOGOUT_USER"]
        req = {"username":username}
        res = self._rest.post(relative_url=relative_url, headers=headers, data=req)
        return res