# https://github.com/openai/whisper
import whisper
from datetime import *

TIME_FORMAT = '{hour:02d}:{min:02d}:{sec:02d}.{mili:03d}'
DEFAULT_LANG = "pt"
MODEL_COMPLEXITY = 'medium'


class Transcription:

  def transcript(self, mediafile: str, lang: str = None) -> str:
    model = whisper.load_model(MODEL_COMPLEXITY)
    result = model.transcribe(mediafile, verbose=True, language=DEFAULT_LANG if lang == None else lang, fp16=False)
    return self.format_to_subtitle(result["segments"])

  def format_to_subtitle(self, segments, vtt = False) -> str:
    srt_text = ""
    if vtt:
      srt_text += "WEBVTT \n\n"
    for segment in segments:
      start = self.format_time(int(segment['start']))
      end = self.format_time(int(segment['end']))
      text: segment['text']
      srt_id = segment['id']+1
      srt_text += f"{srt_id}\n{start} --> {end}\n{text[1:] if str(text[0]).isspace() and len(text) > 0 else text}\n\n"
    return srt_text

  def format_time(self, total_seconds: float) -> str:
    tm_hour, total_seconds = divmod(total_seconds, 3600)
    tm_min, total_seconds = divmod(total_seconds, 60)
    tm_sec, total_seconds = divmod(total_seconds, 1)
    tm_mili, total_seconds = divmod(total_seconds, 0.0001)
    return TIME_FORMAT.format(hour=int(tm_hour), min=int(tm_min), sec=int(tm_sec), mili=int(tm_mili))


class LegendControlItem:
  id: int
  start: float
  stop: float
  msg: list[str]
  start_line: int = -1
  end_line: int = 9999999

  def __init__(self, id: int, str_sub: str) -> None:
    self.id=id
    self.__prepare_legend__(id, str_sub)

  def __prepare_legend__(self, id: int, str_sub: str):
    lines = []
    index = -1
    for ln in str_sub.splitlines(keepends=False):
      index+=1
      if ln == str(id):
        self.start_line = index+2
        continue
      if self.start_line < 0:
        continue
      if ln == str(id+1):
        self.end_line = index-2
        break
      if index >= self.start_line and index <= self.end_line:
        lines.append(ln)
      if self.start_line-1 == index:
        self.__extract_times__(ln)
    if not self.end_line:
      self.end_line = index-1

  def __extract_times__(self, str_line: str):
    str_times = str_line.split(' --> ')
    t = datetime.strptime(str_times[0], '%H:%M:%S.%f').time()
    self.start = (t.hour * 60 + t.minute) * 60 + t.second + (t.microsecond / 1000)
    t = datetime.strptime(str_times[1], '%H:%M:%S.%f').time()
    self.stop = (t.hour * 60 + t.minute) * 60 + t.second + (t.microsecond / 1000)


class LegendControl:
  legends: list[LegendControlItem] = []
  sub_total_id = 0
  tag_id = 0

  def __init__(self, sub: str) -> None:
    self.sub_total_id = 0
    for ln in sub.splitlines(keepends=False):
      if ln == str(self.sub_total_id + 1):
        self.sub_total_id+=1
        self.legends.append(LegendControlItem(self.sub_total_id, sub))7
