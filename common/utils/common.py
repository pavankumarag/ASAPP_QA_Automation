"""common helper methods"""
import json
import os
from common.config.config import Config
config = Config()

def generate_test_params(filename=__file__):
	"""
	To generate test params from data.json of the respective folder
	Args:
        filename: filename to read data.json, defaults to __file__
    Returns:
        test_params: python list of tuples adhering to pytest parameterise 
    """
	fpath = os.path.abspath(filename)
	dir = os.path.dirname(fpath)
	fp = open("{0}/data.json".format(dir))
	jdata = json.load(fp)
	test_params = []
	for testcase in jdata["tests"]:
		test_params.append((testcase["testcase"], testcase["request"], testcase["response"]))
	return test_params

def generate_default_rest_config():
	"""
    Generates default rest config
    Returns:
        username: username
        password: password
        port: port
        ip: ip
    """
	username = config.get_config()["login"]["USERNAME"]
	password = config.get_config()["login"]["PASSWORD"]
	port = config.get_config()["login"]["port"]
	ip = config.get_config()["login"]["ip"]
	return (username, password, port, ip)