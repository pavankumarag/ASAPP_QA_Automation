"""Tests for multiple end to end workflow"""
import pytest
import time
import logging
from common.config.config import Config
from common.utils.logger import configure_log
from api.facade.user_operations import UserActions
from api.facade.product_operations import ProductActions

LOG = configure_log(logging.DEBUG, __name__, "workflows_{}.log".format(time.time()))
config = Config()



class TestWorkflow(object):

	def test_add_to_cart(self, rest):
		"""
		Test method for add to cart workflow
		Args:
			rest: REST fixture
		"""
		user_actions = UserActions(rest=rest)
		product_actions = ProductActions(rest=rest)
		LOG.info("login to the portal")
		user_actions.login()
		LOG.info("Add product of some quantity of the product to the cart")
		product_actions.add_to_cart(product_name="ASAPP Pens", quantity=1)

	def test_checkout_from_cart(self, rest):
		"""
		Test method for checkout from the cart workflow
		Args:
			rest: REST fixture
		"""
		user_actions = UserActions(rest=rest)
		product_actions = ProductActions(rest=rest)
		LOG.info("login to the portal")
		user_actions.login()
		LOG.info("Add product of some quantity of the product to the cart")
		product_actions.add_to_cart(product_name="ASAPP Pens", quantity=1)
		LOG.info("Checking out from the cart")
		product_actions.checkout_from_cart()
	