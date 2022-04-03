import json


class Config:
    def __init__(self, json_path):
        config_file = open(json_path, 'r')
        params = json.loads(config_file.read())
        config_file.close()

        self.db_path = params["sqlite_db_path"]


config = Config("config/config.json")
