import tomllib


with open("config.toml", "rb") as f:
    config = tomllib.load(f)

custom_browsers = config["browsers"]
custom_rules = config["rules"]["custom"]