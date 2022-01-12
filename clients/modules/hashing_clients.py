import os
from json import dumps
import random
import string
import requests
from concurrent.futures.thread import ThreadPoolExecutor
import subprocess
from clients.modules.base_client import BaseClient
from config import BASE_URL, url, port
import base64
import hashlib


class HashingClient(BaseClient):
    def __init__(self):
        super().__init__()

        self.base_url = BASE_URL
        # self.request = APIRequest()
        self.request = requests

    def starting_server(self):
        os.environ["PORT"] = port
        print("Checking if the site is available on the specified PORT....")
        if os.environ.get("PORT") == port:
            print("Set to the correct port: ", port)
        try:
            page_response = self.request.get(f"{BASE_URL}")
            print(f"Connected to the specified PORT {page_response}")
        except:
            print("Connected to the server ")
            my_file = (
                r"C:\Users\Nastracha\projects\broken-hashserve\broken-hashserve_win.exe"
            )
            subprocess.Popen(my_file)
        return f'server running on port{port}'

    def create_hash_password(self, endpoint, body=None):
        """

        :param endpoint: hashor stats
        :param body: dictionary value to test when invalid value is sent
        :return:
        """
        endpoint = endpoint
        original_password, response_code, job_id = self.__generate_unique_password(
            endpoint, body
        )

        return original_password, response_code, job_id

    def __generate_unique_password(self, endpoint, body=None):
        if body is None:
            pass_word = "".join(
                random.SystemRandom().choice(string.ascii_letters + string.digits)
                for _ in range(10)
            )
            payload = dumps({"password": pass_word})
        else:
            pass_word = body['password']
            pass_word = body["username"]
            payload = dumps(body)

        response = self.request.post(
            f"{self.base_url}/{endpoint}", headers=self.headers, data=payload
        )
        return pass_word, response.status_code, response.text

    def simultaneous_post(self, number_runs):
        def post_url(args):
            return requests.post(args[0], data=args[1])

        form_data = '{"password":"passes"}'

        list_of_urls = [(f"{self.base_url}/hash", form_data)] * number_runs

        with ThreadPoolExecutor(max_workers=number_runs) as pool:
            response_list = list(pool.map(post_url, list_of_urls))
            # print(response_list)
            return response_list

    def graceful_shutdown(self, endpoint):
        payload = "shutdown"
        return self.request.post(
            f"{self.base_url}/{endpoint}", headers=self.headers, data=payload
        )

    def get_hash_by_id(self, job_id):
        """

        :param job_id: job id received from successful post
        :return:
        """
        url = f"{BASE_URL}/hash/{job_id}"
        return self.request.get(url)

    def get_hash_server_stats(self):
        ur = f"{BASE_URL}/stats"
        return self.request.get(ur)

    def post_request(self):
        data = '{"password":"testtest"}'
        return requests.post(
            f"{self.base_url}/stats", headers=self.headers, data=data
        )

    def hash_validator(self, string_to_check):
        hash_obj = hashlib.sha512(string_to_check.encode())
        return base64.b64encode(hash_obj.digest()).decode()