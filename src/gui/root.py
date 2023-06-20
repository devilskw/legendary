from config import Config
from tkinter import Tk


class RootGui(Tk):
  cfg: Config
  root_title: str
  root_width: int
  root_height: int

  def __init__(self) -> None:
    super().__init__()
    self.cfg = Config()
    self.__setup_default_data__()
    self.__setup_gui__()

  def __setup_default_data__(self):
    self.root_title = self.cfg.root["title"]
    self.root_width = self.cfg.root["width"]
    self.root_height = self.cfg.root["height"]

  def __setup_gui__(self):
    self.geometry(f'{self.root_width}x{self.root_height}+0+0')
    self.title(self.root_title)

