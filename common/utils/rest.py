"""
Python module for initiating and executing commands via REST API.
"""

import time
import json
import requests
import logging
from common.utils.exceptions import HTTPError, CommandExecutionError
from common.utils.logger import configure_log


LOG = configure_log(logging.INFO, __name__, "test")

class REST(object):
  """REST class for invoking REST calls GET, POST, PUT, DELETE.
  """

  # Constants representing REST API keys.
  HEADERS = "headers"
  DATA = "data"

  # Constants representing type of REST request
  GET = "get"
  PATCH = "patch"
  POST = "post"
  PUT = "put"
  DELETE = "delete"



  def __init__(self, **kwargs):
    """This class defines methods to invoke REST calls.

    Args:
      ip(str): IP address.
      username(str, optional): Username to be used for authentication.
        Default: 'admin'.
      password(str, optional): Password to be used for authentication.
        Default: 'nutanix/4u'.
      port(int,optional): Port to connect for sending REST calls. Default: 9440.
      base_uri(str,optional): URI for sending REST calls to.
        Default: Prism gateway URI.

    Returns
      Returns REST object instance.
    """
    self._ip = kwargs.get('ip', None)
    if not self._ip:
      raise ValueError("Invalid IP address '%s'." % self._ip)

    self._username = kwargs.get('username', 'pavan')
    self._password = kwargs.get('password', 'pavan123')
    self._port = kwargs.get('port', 9440)
    base_url = 'http://{0}:{1}'.format(self._ip, self._port)
    self._base_uri = kwargs.get('base_uri', base_url)

    # Disable HTTPS certificate warning.
    requests.packages.urllib3.disable_warnings()

  def delete(self, relative_url, **kwargs):
    """This routine is used to invoke DELETE call for REST API.

    Args:
      relative_url(str): Relative URL for the particular API call.
      kwargs:
        headers(str, optional): Custom headers for making the REST call.
          Default: {}.
        data(str, optional): Data to be send for making the REST call.
          Default: {}.

    Returns:
      str: response text.
    """
    kwargs["operation"] = REST.DELETE
    return self.__perform_operation(relative_url, **kwargs)

  def get(self, relative_url, **kwargs):
    """This routine is used to invoke GET call for REST API.

    Args:
      relative_url: Relative URL for the particular API call.
      kwargs:
        headers(dict, optional): Custom headers for making the REST call.
          Default: {}
        data(dict, optional): Data to be send for making the REST call.
          Default: {}

    Returns:
      str: response text.
    """
    kwargs["operation"] = REST.GET
    return self.__perform_operation(relative_url, **kwargs)

  def patch(self, relative_url, **kwargs):
    """This routine is used to invoke PATCH call for REST API.

    Args:
      relative_url(str): Relative URL for the particular API call.
      kwargs:
        headers(str, optional): Custom headers for making the REST call.
          Default: {}
        data(str, optional): Data to be send for making the REST call.
          Default: {}

    Returns:
      str: response text.
    """
    kwargs["operation"] = REST.PATCH
    return self.__perform_operation(relative_url, **kwargs)

  def post(self, relative_url, **kwargs):
    """This routine is used to invoke POST call for REST API.

    Args:
      relative_url(str): Relative URL for the particular API call.
      kwargs:
        headers(str, optional): Custom headers for making the REST call.
          Default: {}
        data(str, optional): Data to be send for making the REST call.
          Default: {}

    Returns:
      str: response text.
    """
    kwargs["operation"] = REST.POST
    return self.__perform_operation(relative_url, **kwargs)


  def put(self, relative_url, **kwargs):
    """This routine is used to invoke PUT call for REST API.

    Args:
      relative_url(str): Relative URL for the particular API call.
      kwargs:
        headers(str, optional): Custom headers for making the REST call.
          Default: {}
        data(str, optional): Data to be send for making the REST call.
          Default: {}

    Returns:
      str: response text.
    """
    kwargs["operation"] = REST.PUT
    return self.__perform_operation(relative_url, **kwargs)

  def __perform_operation(self, relative_url, **kwargs):
    """
    Private Method which can be used to perform operations like post, get,
    patch, delete and put.

    Returns:
      str: Response text.

    """
    custom_headers = kwargs.get(REST.HEADERS, {})
    custom_data = kwargs.get(REST.DATA, {})
    raw_response = kwargs.pop("raw_response", False)
    max_retries = kwargs.get('max_retires', 3)
    main_uri = "".join([self._base_uri, relative_url])
    if "operation" not in kwargs:
      raise ValueError("Operation value not specified.")
    operation = kwargs.get("operation")

    # Encode(Serialize) the data using json.dumps
    data = json.dumps((custom_data), indent=2)
    auth = (self._username, self._password)
    response = self.__send_request(req_type=operation, main_uri=main_uri,
                                   headers=custom_headers, verify=False,
                                   data=data, auth=auth,
                                   max_retries=max_retries, raw_response=raw_response)
    return response

  def __send_request(self, **kwargs):
    """
       Private Method which can be used to send any kind of
       HTTP request with custom retries
    """
    req_type = kwargs.pop("req_type", None)
    if not req_type:
      raise ValueError("REST request type not specified.")

    main_uri = kwargs.pop("main_uri", None)
    if not main_uri:
      raise ValueError("REST reuest URL not specified.")

    headers = kwargs.pop("headers", {})
    data = kwargs.pop("data", {})
    auth = kwargs.pop("auth", {})
    raw_response = kwargs.pop("raw_response", False)

    max_retries = kwargs.pop("max_retries", 3)
    verify = kwargs.pop("verify", False)
    timeout = kwargs.pop("timeout", 60)

    retry_count = 1
    LOG.debug(">> %s: %s, headers=%s, data=%s, authenticaion=%s" \
                 % (req_type.upper(), main_uri, headers, data, auth))
    while retry_count <= max_retries:
      method_to_call = getattr(requests, req_type)
      response = method_to_call(main_uri, headers=headers, verify=verify,
                                data=data, auth=auth, timeout=timeout)
      if raw_response:
         return response

      if response.status_code == requests.codes.OKAY:

        # Decode(Deserialize) the json object using json.loads
        return_val = json.loads(response.text)
        LOG.debug("<< %s" % json.dumps(return_val, indent=2))
        return return_val

      if response.status_code == requests.codes.UNAUTHORIZED:
        LOG.debug("UNAUTHORIZED ERROR(%s:%s). Please check given credentials: %s"\
              % (response.status_code, response.text, auth))
        raise HTTPError("(%s) Credential used are %s" %
                              (response.status_code, auth))

      if response.status_code == requests.codes.BAD_REQUEST:
        api_used = "req_type= %s, url=%s, headers=%s, data=%s, auth=%s"\
                   % (req_type, main_uri, headers, data, auth)
        LOG.debug("BAD REQUEST(%s): api = %s" % (response.status_code, api_used))
        raise HTTPError("(%s) Check the api content: %s"\
                              % (response.status_code, api_used))

      if response.status_code == requests.codes.UNSUPPORTED_MEDIA_TYPE:
        message = "%s: Check if the request has been serialized before sending"\
                   %response.status_code
        LOG.debug("UNSUPPORTED MEDIA TYPE %s" % message)
        raise HTTPError(message)

      if response.status_code == requests.codes.INTERNAL_SERVER_ERROR:
        message = "[%s:%s]." % (response.status_code, response.text)
        LOG.debug("INTERNAL SERVER ERROR %s" % message)
        raise CommandExecutionError(message)

      if retry_count == max_retries:
        LOG.debug("RESTError: %s response: %s" % (req_type, response.text))
        raise CommandExecutionError("Reached max retries: %s "
                                             "waiting for proper %s response. "
                                             "Response:[%s:%s] " %
                                             (max_retries, req_type,
                                              response.status_code,
                                              response.text))
      retry_count = retry_count + 1
      time.sleep(5)