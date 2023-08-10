import random
# auto-py-to-exe # for exe
import pvporcupine
import struct
import json
from pvrecorder import PvRecorder
from vosk import Model, KaldiRecognizer
import time
########### my scripts ###########
import testMicro

########### PORCUPINE ###########
porcupine = pvporcupine.create(
    model_path=r'C:\Users\roman\JARVIS\venv\Lib\site-packages\pvporcupine\porcupine_params_zh.pv',
    access_key='V2WsFLhPHNO8cO/Qj80jH9Pq8LRDTk2/C+eQN9cH9j5tIOF4wNsgCA==',
    keywords=['nihao'])
#porcupine.delete()

########### VOSK ###########
vosk_model_small = Model(r'C:\Users\roman\JARVIS\venv\Lib\site-packages\vosk\vosk-model-small-ru-0.22') # full path to the model
kaldi_rec = KaldiRecognizer(vosk_model_small, 16000) # 16000\44100 for my micro, and for small model VOSK

# -1 -> default micro index
recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
recorder.start()

timer = time.time()
while True:
    try:
        pcm = recorder.read()
        keyword_index = porcupine.process(pcm) # detected key-word

        if keyword_index >= 0:
            print('Yes.')

            recorder.stop()
            testMicro.play(random.choice(['Что для вас?', 'Да, сэр.', 'Слушаю вас', 'Нихао', 'Как воживаете?', 'Я тут', 'Что желаете спросить?', 'Подгружаю интеллект', 'Я вас слышу', 'Чё каво', 'И вам', 'Каничува', 'Привет', 'Здравствуй', 'Напрягаю нейроны']))
            recorder.start()

            timer = time.time() + 10 # second for read

        while timer - time.time() > 0:
            pcm = recorder.read() # raw bytes 1234 4321..
            sp = struct.pack('h' * len(pcm), *pcm) # pack bytes \x12\..

            if kaldi_rec.AcceptWaveform(sp): # for [vosk] read 8000 frequency Hz
                result = json.loads(kaldi_rec.Result())['text']
                if result != '' and result != ' ':
                    print('Я:', result)

                    recorder.stop()
                    testMicro.play(f'Обрабатываю: {result}...')
                    testMicro.askGPT(result)
                    recorder.start()

                    timer = time.time() + 10
                    break

    except Exception as err:
        print(f'Unexpected {err=}, {type(err)=}')
        raise

