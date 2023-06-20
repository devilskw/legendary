import logging
from .json import JsonUtils
from .singleton import SingletonMeta
from .txtfile import TxtFileUtils

JSON_FILE = 'assets/config.json'


class Config(metaclass=SingletonMeta):
  json: JsonUtils
  root = {}

  def __init__(self) -> None:
    self.json = JsonUtils()
    self.__load__variables__(self.__load_json__())

  def __load_json__(self) -> dict:
    return self.json.load(JSON_FILE)

  def __load__variables__(self, data):
    try:
      Config.root["width"] = int(data["root"]["width"])
      Config.root["height"] = int(data["root"]["height"])
      Config.root["title"] = str(data["root"]["title"])
    except Exception as ex:
      logging.exception(f"Erro nos dados do arquivo de configuração. data: {str(data)}.", ex)
