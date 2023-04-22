"""Tests for login endpoint"""
import pytest
import json
import os
import logging
from common.config.config import Config
from common.utils.logger import configure_log
from common.utils.common import generate_test_params
from api.facade.user_operations import UserActions
from common.utils.exceptions import CommandExecutionError

LOG = configure_log(logging.DEBUG, __name__, "test.log")
config = Config()
test_params = generate_test_params(__file__)


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
			user_actions = UserActions(rest)
			try:
				user_actions.register(username=req["username"], password=req["password"])
			except CommandExecutionError as e:
				LOG.info(e)

		headers = {'Content-Type': 'application/json'}
		relative_url = config.get_config()['endpoints']["LOGIN_USER"]
		res = rest.post(relative_url=relative_url, headers=headers, data=req, raw_response=True)
		LOG.info("Login test {}".format(res.json()))
		assert res.status_code, response["code"]
		assert res.text, response["message"]