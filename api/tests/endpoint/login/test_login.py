"""Tests for login endpoint"""
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
test_params = generate_test_params(__file__)
LOG.info("Test params {}".format(test_params))


class TestLoginEndpoint(object):

	@pytest.mark.parametrize(["testcase","req", "response"], test_params)
	def test_login(self, rest, testcase, req, response):
		"""
		Test method for login endpoint
		Args:
			rest: REST fixture
			testcase: testcase name
			req: request from data.json
			response: response from data.json
		"""
		if response["code"] == "200":
			LOG.info("For valid login, we are making sure that the user is already registered")
			user_actions = UserActions(rest)
			try:
				user_actions.register(username=req["username"], password=req["password"])
			except HTTPError as e:
				LOG.info(e)

		headers = {'Content-Type': 'application/json'}
		relative_url = config.get_config()['endpoints']["LOGIN_USER"]
		res = rest.post(relative_url=relative_url, headers=headers, data=req, raw_response=True)
		LOG.info("Login test {}".format(res.json()))
		assert str(res.status_code) == response["code"]
		assert response["message"] in res.text.strip()