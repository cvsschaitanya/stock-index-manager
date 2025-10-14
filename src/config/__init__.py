import os

config = {}

def load_config(json_config_file=""):
    # config["POLYGON_API_KEY"] = os.getenv("POLYGON_API_KEY", "KtckQgpk1yzTo5MpCYSKCJsQXGiUncoo")

    if json_config_file and os.path.exists(json_config_file):
        import json
        with open(json_config_file, 'r') as f:
            file_config = json.load(f)
            config.update(file_config)