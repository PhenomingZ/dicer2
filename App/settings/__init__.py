from App.settings.Config import Config

config = Config()


def init_config(app):
    new_config = Config()
    new_config.ELASTICSEARCH_HOST = app.config["ELASTICSEARCH_HOST"]
    print(f"ELASTICSEARCH_HOST = {new_config.ELASTICSEARCH_HOST}")

    new_config.MINIMAL_LINE_LENGTH = app.config["MINIMAL_LINE_LENGTH"]
    print(f"MINIMAL_LINE_LENGTH = {new_config.MINIMAL_LINE_LENGTH}")

    new_config.JACCARD_THRESHOLD_VALUE = app.config["JACCARD_THRESHOLD_VALUE"]
    print(f"JACCARD_THRESHOLD_VALUE = {new_config.JACCARD_THRESHOLD_VALUE}")

    new_config.IMAGE_HAMMING_THRESHOLD_VALUE = app.config["IMAGE_HAMMING_THRESHOLD_VALUE"]
    print(f"IMAGE_HAMMING_THRESHOLD_VALUE = {new_config.IMAGE_HAMMING_THRESHOLD_VALUE}")

    global config
    config = new_config


def get_config():
    global config
    return config
