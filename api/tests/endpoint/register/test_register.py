"""Tests for register endpoint"""
import pytest
import json
import os
import time
import logging
from common.config.config import Config
from common.utils.logger import configure_log
from common.utils.common import generate_test_params
from api.facade.user_operations import UserActions
from common.utils.exceptions import HTTPError

LOG = configure_log(logging.DEBUG, __name__, "register_test_{}.log".format(time.time()))
config = Config()
test_params = generate_test_params(__file__)
LOG.info("Test params {}".format(test_params))


class TestRegisterEndpoint(object):

	@pytest.mark.parametrize(["testcase","req", "response"], test_params)
	def test_register(self, rest, testcase, req, response):
		"""
		Test method for register endpoint
		Args:
			rest: REST fixture
			testcase: testcase name
			req: request from data.json
			response: response from data.json
		"""
		if response["code"] == "200" or testcase == "Empty password":
			LOG.info("To simulate new user always appending epoch to username")
			req["username"] = req["username"] + str(time.time())
		headers = {'Content-Type': 'application/json'}
		relative_url = config.get_config()['endpoints']["REGISTER_USER"]
		res = rest.post(relative_url=relative_url, headers=headers, data=req, raw_response=True)
		LOG.info("Register test {}".format(res.json()))
		assert str(res.status_code) == response["code"]
		if response["code"] == "409":
			LOG.info("Populating specific user for 409 case for asserting purpose")
			response["message"] = response["message"].format(username=req["username"])
		assert response["message"] in res.text