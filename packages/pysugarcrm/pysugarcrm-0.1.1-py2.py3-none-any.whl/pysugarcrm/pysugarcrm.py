# -*- coding: utf-8 -*-
import urllib
import urlparse
import requests
import json


class SugarCRM(object):
    """
    Sugar CRM API for v10
    """

    def __init__(
        self, url, username, password, client_id="sugar",
        login_path="/rest/v10/oauth2/token",
        base_path="/rest/v10/"
    ):
        """
        Updates secret token to start making requests
        """

        parsed_url = list(urlparse.urlparse(url))
        self.scheme, self.netloc = parsed_url[:2]
        parsed_url[2] = login_path
        login_url = urlparse.urlunparse(parsed_url)
        self.base_path = base_path
        if not self.base_path.endswith('/'):
            self.base_path += '/'

        # Build login data
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": client_id,
            "platform": "api",
        }

        response = requests.post(login_url, data=json.dumps(data)).json()

        # Retrieve auth token
        try:
            self.secret_token = response["access_token"]
        except KeyError:
            raise ValueError('No access token received')

        # Start requests session
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "OAuth-Token": self.secret_token,
            }
        )

    def _api_request(
        self, method, path, params='', query='', fragment='', *args, **kwargs
    ):
        """
        Low level API request to SugarCRM
        """

        url = urlparse.urlunparse((
            self.scheme,
            self.netloc,
            self.base_path + path.lstrip('/'),
            params,
            query,
            fragment
        ))
        return self.session.request(method, url, *args, **kwargs)

    @property
    def me(self):
        """
        Returns current user
        """

        return self._api_request("GET", "/me").json()

    def get(self, path, query_params=None):
        """
        Generic GET API call
        """

        return self._api_request(
            "GET", path, query=urllib.urlencode(query_params or {})
        ).json()
