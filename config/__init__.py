import json


class Config:
    def __init__(self, json_path):
        config_file = open(json_path, "r")
        params = json.loads(config_file.read())
        config_file.close()

        self.db_path = params["sqlite_db_path"]
        self.keys_files_path = params["keys_files_path"]
        self.vpn_endpoint = params["vpn_endpoint"]
        self.server_public_key_path = params["server_public_key_path"]


config = Config("config/config.json")
