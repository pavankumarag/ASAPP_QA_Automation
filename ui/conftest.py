import pytest
import logging
import os
import sys
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.core.utils import ChromeType
from common.config.config import Config

from common.utils.logger import configure_log


LOG = configure_log(logging.INFO, __name__, "ui_conftest.log")

@pytest.fixture(scope='function')
def driver(request):
	"""
	Conftest to Initialize Selenium Webdriver tests.
	1. Opens the browser.
	2. Opens URL.
	3. Maximizes browser window.
	Args:
	request (object): gives access to the requesting test context.
	Raises: NA
	Returns: selenium webdriver instance
	"""
	#display = Display(visible=0, size=(1680, 1050))
	#display.start()
	config = Config()
	hub_host = config.get_config()["ui"]["GRID_HOST_NAME"]
	if os.getenv("browser") is None or os.getenv("browser") == "chrome":
		chrome_options = webdriver.ChromeOptions()
		#chrome_options.add_argument('--headless')
		chrome_options.add_argument("--no-sandbox")
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument("disable-infobars")
		chrome_options.add_argument("enable-automation")
		#wdriver = webdriver.Remote(command_executor="http://{}:4444".format(hub_host), options=chrome_options)
		wdriver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=chrome_options)
		
		#wdriver.set_window_size(1680, 1050)
	else:
		fp = webdriver.FirefoxProfile()
		fp.set_preference("dom.max_chrome_script_run_time", 60)
		fp.set_preference("dom.max_script_run_time", 60)
		#wdriver = webdriver.Firefox(firefox_profile=fp)
		firefox_options = webdriver.FirefoxOptions()
		#firefox_options.add_argument('--headless')
		firefox_options.add_argument("--no-sandbox")
		firefox_options.add_argument("--disable-extensions")
		firefox_options.add_argument("disable-infobars")
		firefox_options.add_argument("enable-automation")
		firefox_options.accept_insecure_certs = True

		fp = webdriver.FirefoxProfile()
		fp.accept_untrusted_certs = True
		firefox_options.profile = fp
	
		wdriver = webdriver.Remote(command_executor="http://{}:4444".format(hub_host),
			     desired_capabilities={'browserName': 'firefox', 'javascriptEnabled': True,'acceptSslCerts': True,'acceptInsecureCerts':True}, 
				 options=firefox_options)

	wdriver.maximize_window()
	wdriver.set_page_load_timeout(50)
	wdriver.implicitly_wait(10)
	wdriver.set_script_timeout(10)
	product_url = config.get_config()["ui"]["PRODUCT_UI_URL"]
	wdriver.get("http://{product_url}:3000".format(product_url=product_url))
	def end():
		wdriver.quit()
		#display.stop()
	request.addfinalizer(end)
	return wdriver

