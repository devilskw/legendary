import logging

class TxtFileUtils:

  def open(self, filename: str) -> str:
    data = ''
    try:
      with open(filename, 'r', encoding='utf-8') as file:
        data = file.read()
      return data
    except Exception as ex:
      logging.exception(f"Erro ao tentar carregar arquivo {filename}.", ex)

  def save(self, filename: str, data) -> None:
    try:
      with open(filename, 'w', encoding='utf8') as file:
        file.write(data)
    except Exception as ex:
      logging.exception(f"Erro ao tentar salvar arquivo {filename}.", ex)