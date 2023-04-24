import time
import logging
import json
from locust import HttpUser, task, between
from api.facade.user_operations import UserActions
from common.utils.exceptions import HTTPError
from common.utils.logger import configure_log

from common.config.config import Config
config = Config()

LOG = configure_log(logging.INFO, __name__, "perf_login_test_{}.log".format(time.time()))

class UserLogin(HttpUser):
    host="http://localhost:5000"
    wait_time = between(1, 5)

    '''
    def on_start(self):
        """
        On start making sure user is registered
        """
        LOG.info("Making sure user is registered before login")
        user = UserActions()
        self.username = config.get_config()["login"]["USERNAME"]
        self.password = config.get_config()["login"]["PASSWORD"]
        try:
            user.register(username=self.username, password=self.password)
        except HTTPError as e:
            LOG.info(e)
    '''

    @task
    def valid_login(self):
        """
        Login endpoint under load test
        """
        self.username = config.get_config()["login"]["USERNAME"]
        self.password = config.get_config()["login"]["PASSWORD"]
        req_json = {"username": self.username, "password": self.password}
        headers = {'Content-Type': 'application/json'}
        self.client.post("/users/login", headers=headers, json=req_json)