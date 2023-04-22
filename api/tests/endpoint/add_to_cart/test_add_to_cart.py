"""Tests for add to cart endpoint"""
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

LOG = configure_log(logging.DEBUG, __name__, "add_to_cart_test_{}.log".format(time.time()))
config = Config()
test_params = generate_test_params(__file__)
LOG.info("Test params {}".format(test_params))


class TestAddToCartEndpoint(object):

	@pytest.mark.parametrize(["testcase","req", "response", "metadata"], test_params)
	def test_add_to_cart(self, rest, testcase, req, response, metadata):
		"""
		Test method for add to cart endpoint
		Args:
			rest: REST fixture
			testcase: testcase name
			req: request from data.json
			response: response from data.json
			metadata: metadata for the test
		"""
		headers = {'Content-Type': 'application/json'}
		relative_url = config.get_config()['endpoints']["ADD_TO_CART"].format(username=metadata["username"], product_name=metadata["product"])
		res = rest.post(relative_url=relative_url, headers=headers, data=req, raw_response=True)
		LOG.info("Add to cart test {}".format(res.json()))
		assert str(res.status_code) == response["code"]
		assert response["message"] in res.text