from locust import HttpUser, task, between
from locust.exception import StopUser
from testing import response
import uuid


class Testing(HttpUser):
    wait_time = between(1, 6)
    def on_start(self):
        self.login()
    def login(self):
        payload = {"email": "chenyingshu1234@gmail.com",
                   "pw": "Chenxh1031!"}
        with self.client.post("login", data=payload, catch_response=True) as response:
            if "gone wrong" in response.text:
                response.failure("Not working")
                raise StopUser()
            else:
                print(f"login status: {response.status_code}")
    @task
    def index(self):
        self.client.get("/")

    @task
    def login_page(self):
        self.client.get("/login")

    @task
    def add_test(self):
        title = f"{uuid.uuid4()}_test"
        payload = {
            'title': title,
            'in_greek': '',
            'birth': 'test',
            'death': 'test',
            'reign': 'test',
            'life': "test",
            'dynasty': "test",
            'reign_start': 1,
            'ascent_to_power': 'test',
            'references': 'test',
            'edit': -1
        }
        with self.client.post("/add_new_emperor", data=payload, catch_response=True) as response:
            if response.status_code != 200 and response.status_code != 302:
                if "gone wrong" in response.text:
                    response.failure("Not working")
            else:
                    response.success()
    @task
    def edit_test(self):
        title = f"{uuid.uuid4()}_test"

        payload = {
            'title': title,
            'in_greek': '',
            'birth': 'test',
            'death': 'test',
            'reign': 'test',
            'life': "test",
            'dynasty': "test",
            'reign_start': 1,
            'ascent_to_power': 'test',
            'references': 'test',
            'edit': 1
        }
        with self.client.post(f"/edit_emperor/{1}", data=payload, catch_response=True) as response:
            if response.status_code != 200 and response.status_code != 302:
                if "gone wrong" in response.text:
                    response.failure("Not working")
            else:
                    response.success()






