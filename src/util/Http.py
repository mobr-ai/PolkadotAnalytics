import requests
from requests import Response
from urllib3 import connectionpool, poolmanager

    #pool_connections=100, pool_maxsize=100
def patch_http_connection_pool(**constructor_kwargs):
    """
    This allows to override the default parameters of the 
    HTTPConnectionPool constructor.
    For example, to increase the poolsize to fix problems 
    with "HttpConnectionPool is full, discarding connection"
    call this function with maxsize=16 (or whatever size 
    you want to give to the connection pool)
    """

    class MyHTTPConnectionPool(connectionpool.HTTPConnectionPool):
        def __init__(self, *args,**kwargs):
            kwargs.update(constructor_kwargs)
            super(MyHTTPConnectionPool, self).__init__(*args,**kwargs)

    poolmanager.pool_classes_by_scheme['http'] = MyHTTPConnectionPool

def patch_https_connection_pool(**constructor_kwargs):
    """
    This allows to override the default parameters of the
    HTTPConnectionPool constructor.
    For example, to increase the poolsize to fix problems
    with "HttpSConnectionPool is full, discarding connection"
    call this function with maxsize=16 (or whatever size
    you want to give to the connection pool)
    """

    class MyHTTPSConnectionPool(connectionpool.HTTPSConnectionPool):
        def __init__(self, *args,**kwargs):
            kwargs.update(constructor_kwargs)
            super(MyHTTPSConnectionPool, self).__init__(*args,**kwargs)

    poolmanager.pool_classes_by_scheme['https'] = MyHTTPSConnectionPool

class Http:
    """
    Http Class

    Class to abstract the http protocol funcionalities.

    ...

    Attributes
    ----------
    base_url : str
        the url to access the targeted http server
    """

    base_url = ''

    def __init__(self, base_url='https://127.0.0.1:5000') -> None:
        self.base_url = base_url
        self.session = requests.Session()

    def _send_message(self, method, endpoint, params=None, data=None, headers=None):
        response = None
        try:
            url = self.base_url + endpoint
            response:Response = self.session.request(method, url, params=params, data=data, timeout=30, headers=headers)
            if response.status_code >= 300:
                print (f"url: {url} returned status code {response.status_code} for the method: {method}")
                print (f"    endpoint: {endpoint}. params: {params}. data: {data}. headers: {headers}.")
                print (f"    response: {response.text}.")
                resp_json = dict()

            else:
                resp_json = response.json()

            response.close()

        except Exception as e:
            print ("Http exception: ")
            print (f"url: {url}. method: {method}. endpoint: {endpoint}. params: {params}. data: {data}. headers: {headers}. response: {response}.")
            print (f"exception: {e}")
            resp_json = dict()

        return resp_json

    def _get(self, endpoint, params=None):
        return self._send_message('GET', endpoint, params=params)

    def _put(self, endpoint, params=None, data=None, headers=None):
        return self._send_message('PUT', endpoint, params=params, data=data, headers=headers)

    def _post(self, endpoint, params=None, data=None, headers=None):
        return self._send_message('POST', endpoint, params=params, data=data, headers=headers)

    def _delete(self, endpoint, params=None):
        return self._send_message('DELETE', endpoint, params=params)
