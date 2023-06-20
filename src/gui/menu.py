from tkinter import Tk, Menu

class RootMenu(Menu):
  def __init__(self, root: Tk) -> None:
    super().__init__(root)
    root.config(menu=self)


class FileMenu(Menu):
  file: str

  def __init__(self, parent: Menu) -> None:
    super().__init__(parent, tearoff=0)
    parent.add_cascade(label="Arquivo", menu=self)
    self.add_command(label="Abrir video", command=parent.master.open)
    self.add_command(label="Sair", command=parent.master.quit)