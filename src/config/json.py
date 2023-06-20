import json
import logging

class JsonUtils:

  def load(self, jsonfile: str) -> dict:
    data = {}
    try:
      with open(jsonfile) as file:
        data = json.loads(file.read())
      return data
    except Exception as ex:
      logging.exception(f"Erro ao tentar carregar arquivo {jsonfile}.", ex)

  def save(self, jsonfile: str, data) -> None:
    try:
      with open('filename', 'w', encoding='utf8') as json_file:
        json.dumps(data, json_file, indent=2, allow_nan=False)
    except Exception as ex:
      logging.exception(f"Erro ao tentar salvar arquivo {jsonfile}.", ex)