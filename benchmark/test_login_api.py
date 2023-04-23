"""Benchmaring login API"""
import pytest
import time
import logging
from common.config.config import Config
from common.utils.logger import configure_log
from common.utils.common import generate_test_params
from api.facade.user_operations import UserActions
from common.utils.exceptions import HTTPError

LOG = configure_log(logging.DEBUG, __name__, "login_test_{}.log".format(time.time()))
config = Config()

def login(rest, relative_url, headers, req):
    """
    Login method to benchmark
    Args:
        rest: REST pbject
        relative_url: REST endpoint
        headers: headers
        req: data for REST endpoint
    """
    response = rest.post(relative_url=relative_url, headers=headers, data=req, raw_response=True)
    return response
          

def test_benchmark_login_api(benchmark, rest):
    """
    Benchmark method 
    Args:
        benchmark: Inbuilt benchmark fixture
        rest: rest fixture
    """
    username = config.get_config()["login"]["USERNAME"]
    password = config.get_config()["login"]["PASSWORD"]
    LOG.info("Making sure user is registered")
    user = UserActions(rest=rest)
    try:
        user.register(username==username, password=password)
    except HTTPError as e:
        LOG.info(e)
    req = {"username": username, "password": password}
    headers = {'Content-Type': 'application/json'}
    relative_url = config.get_config()['endpoints']["LOGIN_USER"]
    res = benchmark.pedantic(login, args=(rest, relative_url, headers, req),
                             iterations=10, 
                             rounds=100)
    assert str(res.status_code) == "200"