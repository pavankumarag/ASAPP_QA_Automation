""" conftest to define fixtures"""
import sys
import os

sys.path.insert(0,os.path.dirname(__file__))

import pytest
import logging
from common.utils.rest import REST
from common.config.config import Config
from common.utils.logger import configure_log

LOG = configure_log(logging.INFO, __name__, "test")

@pytest.fixture(scope='function')
def rest(request):
    """
    REST fixture to be used by any test method 
    """
    config = Config()
    username = config.get_config()["login"]["USERNAME"]
    password = config.get_config()["login"]["PASSWORD"]
    port = config.get_config()["login"]["port"]
    ip = config.get_config()["login"]["ip"]
    rest = REST(ip=ip, username=username, password=password, port=port)
    return rest