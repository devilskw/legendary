from tkinter import Frame, LabelFrame, Label, Button, Checkbutton, Scrollbar, Tk, Text, HORIZONTAL, BOTH, END, GROOVE, LEFT, RIGHT, Y


class SubtitleFrame(Frame):
  def __init__(self, root: Tk, bd=1, bg='#e68609') -> None:
    super().__init__(root, bd=bd, bg=bg)
    self.place(relwidth=0.5, relheight=1, relx=0.5)


class TranscriptionFrame(LabelFrame):
  def __init__(self, parent: SubtitleFrame, text='Transcrição', font=('arial', 10, 'bold'), bd=1, fg='Black', bg='#e68609') -> None:
    super().__init__(parent, text=text, font=font, bd=bd, fg=fg, bg=bg)
    self.place(relx=0, rely=0, relwidth=1, relheight=0.9)

TAG_NAME = "destaque"
TAG_BKGND_COLOR = "#e68609"

class TranscriptionText(Text):
  yscroll: Scrollbar

  def __init__(self, parent: TranscriptionFrame) -> None:
    super().__init__(parent, )
    self.pack(side=LEFT)
    self.place(relx=0, rely=0, relwidth=0.9, relheight=1)
    self.yscroll = Scrollbar(self)
    self.yscroll.pack(side=RIGHT, fill=Y)
    self.yscroll.config(command=self.yview)
    self.configure(yscrollcommand=self.yscroll.set)
    self.tag_config('color', background=TAG_BKGND_COLOR)
    self.tag_configure(TAG_NAME, background=TAG_BKGND_COLOR)

  def set_text(self, text: str):
    self.delete(1.0, END)
    self.insert(END, text)

  def get_text(self) -> str:
    return self.get(1.0, "end-1c")

  def bind_text_modified(self, event_handler):
    self.edit_modified(False) #reset flag that indicates the textarea was modified
    self.bind("<<Modified>>", event_handler)

  def highlight_text(self, start_line: int, end_line: int):
    #self.tag_delete(TAG_NAME)
    self.tag_add(TAG_NAME, f'{start_line}.0', f'{end_line}.200') #todo validar

  def remove_highlights(self) -> bool:
    for tag in self.tag_names():
      self.tag_delete(tag)
    return True


class TranscriptionControlFrame(Frame):
  def __init__(self, parent: SubtitleFrame, bd=1, bg='#e68609') -> None:
    super().__init__(parent, bd=bd, bg=bg)
    self.place(rely=0.9, relx=0, relwidth=1, relheight=0.1)


class TranscriptionSaveButton(Button):
  def __init__(self, parent: TranscriptionControlFrame, command: any = None, text='Save', width=20, font=('arial', 10, 'bold'), bd=1, relief=GROOVE) -> None:
    super().__init__(parent, text=text, font=font, bd=bd, width=width, relief=relief, command=command)
    self.grid(row=0, column=0, padx=(125,5), pady=10)

class TranscriptionAutoSaveCheckbox(Checkbutton):
  def __init__(self, parent: TranscriptionControlFrame, variable=0, text='auto-save', width=20, font=('arial', 10, 'bold'), bd=1, relief=GROOVE) -> None:
    super().__init__(parent, text=text, font=font, bd=bd, width=width, relief=relief, variable=variable)
    self.grid(row=0, column=1, padx=5, pady=10)

  def is_checked(self) -> bool:
    return self.getboolean()
