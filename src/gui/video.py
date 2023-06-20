# https://github.com/PaulleDemon/tkVideoPlayer/blob/master/examples/sample_player.py
import time
from tkinter import Frame, LabelFrame, Button, Tk, Entry, Scale, HORIZONTAL, BOTH, END, GROOVE
from tkVideoPlayer import TkinterVideo

TIME_FORMAT = '{hour:02d}:{minute:02d}:{second:02d}.{microsecond:03d}'

class VideoPlayerFrame(Frame):
  def __init__(self, root: Tk, bd=1, bg='#e68609') -> None:
    super().__init__(root, bd=bd, bg=bg)
    # self.place(width=int(root.__getattribute__("root_width"))/2, height=int(root.__getattribute__("root_height")))
    self.place(relwidth=0.5, relheight=1, relx=0) #  relwidth=0.5, relheight=int(root.__getattribute__("root_height")))

class VideoFrame(LabelFrame):
  def __init__(self, parent: VideoPlayerFrame, text='Video', font=('arial', 8, 'bold'), bd=1, fg='Black', bg='#e68609') -> None:
    super().__init__(parent, text=text, font=font, bd=bd, fg=fg, bg=bg)
    self.place(relwidth=0.80, relheight=0.9, relx=0, rely=0)

class VideoControlFrame(LabelFrame):
  def __init__(self, parent: VideoPlayerFrame, text='Controls', font=('arial', 8, 'bold'), bd=1, fg='Black', bg='#e68609') -> None:
    super().__init__(parent, text=text, font=font, bd=bd, fg=fg, bg=bg)
    self.place(relwidth=0.2, relheight=0.9, relx=0.8, rely=0)

class VideoBottomControlFrame(LabelFrame):
  def __init__(self, parent: VideoPlayerFrame, text='Timelapse Controls', font=('arial', 8, 'bold'), bd=1, fg='Black', bg='#e68609') -> None:
    super().__init__(parent, text=text, font=font, bd=bd, fg=fg, bg=bg)
    self.place(relwidth=1, relheight=0.1, relx=0, rely=0.9)

class VideoStopButton(Button):
  def __init__(self, parent: VideoControlFrame, command: any = None, text='Stop', width=20, font=('arial', 10, 'bold'), bd=1, relief=GROOVE) -> None:
    super().__init__(parent, text=text, font=font, bd=bd, width=width, relief=relief, command=command)
    self.place(relwidth=0.8, height=30, relx=0.1, rely=0.05)

class VideoRwButton(Button):
  def __init__(self, parent: VideoControlFrame, command: any = None, text='<<', width=20, font=('arial', 10, 'bold'), bd=1, relief=GROOVE) -> None:
    super().__init__(parent, text=text, font=font, bd=bd, width=width, relief=relief, command=command)
    self.place(relwidth=0.8, height=30, relx=0.1, rely=0.30)

class VideoFfButton(Button):
  def __init__(self, parent: VideoControlFrame, command: any = None, text='>>', width=20, font=('arial', 10, 'bold'), bd=1, relief=GROOVE) -> None:
    super().__init__(parent, text=text, font=font, bd=bd, width=width, relief=relief, command=command)
    self.place(relwidth=0.8, height=30, relx=0.1, rely=0.55)

class VideoPauseButton(Button):
  def __init__(self, parent: VideoControlFrame, command: any = None, text='Play/Pause', width=20, font=('arial', 10, 'bold'), bd=1, relief=GROOVE) -> None:
    super().__init__(parent, text=text, font=font, bd=bd, width=width, relief=relief, command=command)
    self.place(relwidth=0.8, height=30, relx=0.1, rely=0.80)

class VideoTimelapseText(Entry):
  def __init__(self, parent: VideoBottomControlFrame, command: any = None, textvariable='00:00:00.000', width=30, font=('arial', 10, 'bold'), bd=1, relief=GROOVE) -> None:
    super().__init__(parent, textvariable=textvariable, font=font, bd=bd, width=width, relief=relief, validate='focusout' ,validatecommand=command)
    #todo self.grid(row=1, column=0, padx=5, pady=10)
    self.place(relwidth=0.2, relheight=1, relx=0.8, rely=0)

  def to_str(self, seconds: float) -> str:
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

  def to_seconds(self, formatted_time: str) -> float:
    hour, minutes, sec = formatted_time.split(':')
    return int(hour)*3600+int(minutes)*60+int(sec)

  def set_value(self, value: str):
    self.delete(0, END)
    self.insert(0, value)

  def get_value(self) -> str:
    return self.get()

class VideoTimelapseSlider(Scale):
  def __init__(self, parent: VideoBottomControlFrame, width=10, min_val=0.0, max_val=600.0, tickinterval=60.0, orient=HORIZONTAL) -> None:
    super().__init__(parent, width=width, from_=min_val, to=max_val, tickinterval=tickinterval, orient=orient )
    self.place(relwidth=0.8, relheight=1, relx=0, rely=0)

  def get_value(self) -> float:
    return self.get()

  def set_value(self, total_seconds: float):
    self.set(total_seconds)

  def bind_change_slider(self, event_handler):
    self.bind("<ButtonRelease-1>", event_handler)

class VideoPlayer(TkinterVideo):
  def __init__(self, parent: VideoFrame, scaled: bool = True, consistant_frame_rate: bool = True, keep_aspect: bool = True, *args, **kwargs):
    super().__init__(parent, scaled, consistant_frame_rate, keep_aspect, *args, **kwargs)
    self.place(relwidth=1, relheight=1, relx=0, rely=0)

  def load(self, file: str):
    super().load(file)
    self.pack(fill=BOTH, expand=True)
    self.update()
    self.play()

  def play_or_pause(self) -> bool:
    self.play() if self.is_paused() else self.pause()
    self.update()
    return not self.is_paused()

  def bind_duration(self, event_handler):
    self.bind("<<Duration>>", event_handler)

  def bind_update_time(self, event_handler):
    self.bind("<<SecondChanged>>", event_handler)

  def bind_finished(self, event_handler):
    self.bind("<<Ended>>", event_handler)