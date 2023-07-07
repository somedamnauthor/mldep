from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape
import glob
import random
import base64


class UserTasks(TaskSet):

    @task
    def classify_image(self):

        image_files = glob.glob('data/images/*.jpg') 
        image_path = random.choice(image_files)

        with open(image_path, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            payload = {'data': encoded_image}
            response = self.client.post('/predict', data=payload)
            print(response.text)


# class User(HttpUser):
#     wait_time = constant(0)
#     tasks = [UserTasks]
#     host = "http://localhost:5000"


class UserA(HttpUser):
    wait_time = constant(1)
    tasks = [UserTasks]
    host = "http://localhost:5000"


class UserB(HttpUser):
    wait_time = constant(1)
    tasks = [UserTasks]
    host = "http://localhost:5000"

class UserC(HttpUser):
    wait_time = constant(1)
    tasks = [UserTasks]
    host = "http://localhost:5000"


class UserD(HttpUser):
    wait_time = constant(1)
    tasks = [UserTasks]
    host = "http://localhost:5000"


class UserE(HttpUser):
    wait_time = constant(1)
    tasks = [UserTasks]
    host = "http://localhost:5000"


class UserF(HttpUser):
    wait_time = constant(1)
    tasks = [UserTasks]
    host = "http://localhost:5000"

class UserG(HttpUser):
    wait_time = constant(0.5)
    tasks = [UserTasks]
    host = "http://localhost:5000"


class UserH(HttpUser):
    wait_time = constant(1)
    tasks = [UserTasks]
    host = "http://localhost:5000"



class StagesShape(LoadTestShape):
    """
    A simply load test shape class that has different user and spawn_rate at
    different stages.

    Keyword arguments:

        stages -- A list of dicts, each representing a stage with the following keys:
            duration -- When this many seconds pass the test is advanced to the next stage
            users -- Total user count
            spawn_rate -- Number of users to start/stop per second
            stop -- A boolean that can stop that test at a specific stage

        stop_at_end -- Can be set to stop once all stages have run.
    """

    # stages = [
    #     {"duration": 1, "users": 3, "spawn_rate": 3},
    #     {"duration": 2, "users": 5, "spawn_rate": 5},
    #     {"duration": 3, "users": 1, "spawn_rate": 1},
    #     {"duration": 4, "users": 1, "spawn_rate": 1},
    #     {"duration": 5, "users": 2, "spawn_rate": 2},
    #     {"duration": 6, "users": 1, "spawn_rate": 1},
    #     {"duration": 7, "users": 3, "spawn_rate": 3},
    #     {"duration": 8, "users": 5, "spawn_rate": 5},
    #     {"duration": 9, "users": 1, "spawn_rate": 1},
    #     {"duration": 10, "users": 1, "spawn_rate": 1},
    #     {"duration": 11, "users": 2, "spawn_rate": 2},
    #     {"duration": 12, "users": 1, "spawn_rate": 1}
    # ]


    stages = [
        {"duration": 1, "users": 3, "spawn_rate": 3, "user_classes": [UserA, UserB, UserC]},
        {"duration": 2, "users": 5, "spawn_rate": 5, "user_classes": [UserD, UserE, UserF, UserG, UserH]},
        {"duration": 3, "users": 1, "spawn_rate": 1, "user_classes": [UserA]},
        {"duration": 4, "users": 1, "spawn_rate": 1, "user_classes": [UserB]},
        {"duration": 5, "users": 2, "spawn_rate": 2, "user_classes": [UserC, UserD]},
        {"duration": 6, "users": 1, "spawn_rate": 1, "user_classes": [UserE]},
        {"duration": 7, "users": 3, "spawn_rate": 3, "user_classes": [UserF, UserG, UserH]},
        {"duration": 8, "users": 5, "spawn_rate": 5, "user_classes": [UserA, UserB, UserC, UserD, UserE]},
        {"duration": 9, "users": 1, "spawn_rate": 1, "user_classes": [UserF]},
        {"duration": 10, "users": 1, "spawn_rate": 1, "user_classes": [UserG]},
        {"duration": 11, "users": 2, "spawn_rate": 2, "user_classes": [UserA, UserB]},
        {"duration": 12, "users": 1, "spawn_rate": 1, "user_classes": [UserC]},
    ]


    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None