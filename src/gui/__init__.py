from tkinter.filedialog import askopenfilename
from gui.root import RootGui
from gui.menu import RootMenu, FileMenu
from gui.video import *
from gui.transcription import *
from legend import *
from config import TxtFileUtils


class AppView(RootGui):

  txt_utils: TxtFileUtils
  #menu
  menu_root: RootMenu
  menu_file: FileMenu

  #video file
  file: str

  #video
  frame_vp_root: VideoPlayerFrame

  frame_vp_vw: VideoFrame
  video: VideoPlayer

  frame_vp_ctrl: VideoControlFrame
  btn_stop: VideoStopButton
  btn_rw: VideoRwButton
  btn_ff: VideoFfButton
  btn_pause: VideoPauseButton

  frame_vr_bottom_ctrl: VideoBottomControlFrame
  txt_time: VideoTimelapseText
  slid_time: VideoTimelapseSlider

  #transcription
  frame_sub: SubtitleFrame

  frame_sub_vw: TranscriptionFrame
  txtarea_sub: TranscriptionText
  legend: LegendControl

  frame_sub_ctrl: TranscriptionControlFrame
  btn_save: TranscriptionSaveButton
  chk_auto_save: TranscriptionAutoSaveCheckbox

  # auto save value ( 0 = disabled / 1 = enabled)
  chk_auto_save_value: int = 0

  # video
  def on_video_upd_duration(self, event):
    video_duration = self.video.video_info()['duration']
    self.slid_time['to'] = video_duration
    if video_duration <= 120:
      self.slid_time['tickinterval']=10
    elif video_duration <= 300:
      self.slid_time['tickinterval']=20
    elif video_duration <= 600:
      self.slid_time['tickinterval']=60
    elif video_duration <= 1200:
      self.slid_time['tickinterval']=120
    else:
      self.slid_time['tickinterval']=300

  def on_video_upd_time(self, event):
    self.slid_time.set(self.video.current_duration())
    self.txt_time.set_value(self.txt_time.to_str(self.video.current_duration()))
    tag = self.__get_tag__(self.video.current_duration())
    self.txtarea_sub.highlight_text(tag.start_line, tag.end_line)#todo

  def on_video_finished(self, event):
    self.slid_time.set_value(self.slid_time["to"])
    self.txt_time.set_value(self.txt_time.to_str(self.slid_time["to"]))

  # timelapse slide
  def on_slide_changed(self, event):
    second = int(self.slid_time.get())
    self.video.seek(int(second))
    self.txt_time.set_value(self.txt_time.to_str(second))

  # timelapse text
  def on_timelapse_text_changed(self):
    try:
      second = self.txt_time.to_seconds(self.txt_time.get_value())
      self.slid_time.set(second)
      self.video.seek(second)
    except Exception as ex:
      print(ex)
      self.slid_time.set(self.video.current_duration())
      self.txt_time.set_value(self.txt_time.to_str(self.video.current_duration()))

  # video control
  def on_btn_stop_click(self):
    self.video.stop()
    self.slid_time.set_value(0)
    self.txt_time.set_value(self.txt_time.to_str(0))

  def on_btn_rw_click(self):
    tm = int(self.slid_time.get_value()) - 5
    self.video.seek(tm)
    self.slid_time.set(tm)
    self.txt_time.set_value(self.txt_time.to_str(tm))

  def on_btn_ff_click(self):
    tm = int(self.slid_time.get_value()) + 5
    self.video.seek(tm)
    self.slid_time.set(tm)
    self.txt_time.set_value(self.txt_time.to_str(tm))

  def on_btn_pause_click(self):
    self.video.play_or_pause()
    self.frame_vp_vw['text'] = 'Video - paused' if self.video.is_paused() else 'Video'

  # transcriptions
  def on_btn_save_click(self):
    self.__save__transcription__(self.txtarea_sub.get_text())

  def on_txtarea_sub_modified(self, event):
    if self.chk_auto_save_value > 0:
      self.__save__transcription__(self.txtarea_sub.get_text())

  def __open_subtitle__(self):
    if self.file:
      value = self.txt_utils.open(self.file.replace(".mp4", ".srt"))
      self.txtarea_sub.set_text(value)
      self.legend = LegendControl(value)

  def __save__transcription__(self, value):
    if self.file:
      self.txt_utils.save(self.file.replace(".mp4", ".srt"), value)
      self.legend = LegendControl(value)

  def __init__(self) -> None:
    super().__init__()
    self.txt_utils = TxtFileUtils()
    self.__setup_menus__()
    self.__setup_videoplayer__()
    self.__setup_transcription__()

  def __get_tag__(self, duration_seconds: float):
    for item in self.legend.legends:
        if duration_seconds >= item.start  and duration_seconds <= item.stop:
          return item
    return None

  # general

  def show(self):
    self.mainloop()

  def open(self) -> str:
    self.file = askopenfilename()
    if self.file:
      self.video.load(self.file)
      self.slid_time.set_value(0)
      self.txt_time.set_value('00:00:00.000')
      self.__open_subtitle__()
      self.video.play()
    return self.file

  def __setup_menus__(self):
    self.menu_root = RootMenu(self)
    self.menu_file = FileMenu(self.menu_root)

  def __setup_videoplayer__(self):
    self.frame_vp_root = VideoPlayerFrame(self)

    self.frame_vp_vw = VideoFrame(self.frame_vp_root)
    self.video = VideoPlayer(self.frame_vp_vw)
    self.video.bind_duration(self.on_video_upd_duration)
    self.video.bind_update_time(self.on_video_upd_time)
    self.video.bind_finished(self.on_video_finished)

    self.frame_vp_ctrl = VideoControlFrame(self.frame_vp_root)
    self.btn_stop = VideoStopButton(self.frame_vp_ctrl, command=self.on_btn_stop_click)
    self.btn_rw = VideoRwButton(self.frame_vp_ctrl, command=self.on_btn_rw_click)
    self.btn_ff = VideoFfButton(self.frame_vp_ctrl, command=self.on_btn_ff_click)
    self.btn_pause = VideoPauseButton(self.frame_vp_ctrl, command=self.on_btn_pause_click)

    self.frame_vr_bottom_ctrl = VideoBottomControlFrame(self.frame_vp_root)
    self.txt_time = VideoTimelapseText(self.frame_vr_bottom_ctrl, command=self.on_timelapse_text_changed)
    self.slid_time = VideoTimelapseSlider(self.frame_vr_bottom_ctrl)
    self.slid_time.bind_change_slider(self.on_slide_changed)

  def __setup_transcription__(self):
    self.frame_sub      = SubtitleFrame(self)

    self.frame_sub_vw   = TranscriptionFrame(self.frame_sub)
    self.txtarea_sub = TranscriptionText(self.frame_sub_vw)
    self.txtarea_sub.bind_text_modified(self.on_txtarea_sub_modified)

    self.frame_sub_ctrl = TranscriptionControlFrame(self.frame_sub)
    self.btn_save = TranscriptionSaveButton(self.frame_sub_ctrl, command=self.on_btn_save_click)
    self.chk_auto_save = TranscriptionAutoSaveCheckbox(self.frame_sub_ctrl, variable=self.chk_auto_save_value)