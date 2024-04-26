import speech_recognition as sR
import os
def recognizeAudio(filename, duration=None):
  AUDIO_FILE = os.path.join(filename) # задаем путь к аудиофайлу
  r = sR.Recognizer() # создаем объект класса Recognizer
  with sR.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source, duration=duration) # считываем аудиофайл

  return r.recognize_google(audio, language='ru') # запускаем распознавание