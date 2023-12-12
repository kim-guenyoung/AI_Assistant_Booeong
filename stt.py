from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
import pyaudio
from pydub import AudioSegment
from pydub.playback import play
import io
import json
import spidev
import time
import os
import pygame
import re
import RPi.GPIO as GPIO
import random
from datetime import datetime
import requests
import subprocess
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
from board import SCL, SDA
import busio
import time

text_to_speech = "/home/pi/lunch/iconic-aloe-403811-80800b7d7bd7.json"
speech_to_text = "/home/pi/lunch/iconic-aloe-403811-fef393854188.json"

# Google Cloud Speech-to-Text 및 Text-to-Speech API 인증 설정
client_stt = speech.SpeechClient.from_service_account_file(speech_to_text)
client_tts = texttospeech.TextToSpeechClient.from_service_account_file(text_to_speech)


# 교직원 식당
professor = "/home/pi/lunch/menu_faculty.json"
with open(professor, 'r', encoding='utf-8') as file:
    professor_data = json.load(file)

# Convert the JSON data to a string (you can modify this based on your JSON structure)
json_text = json.dumps(professor_data, ensure_ascii=False)

# 오늘의 백반
student = "/home/pi/lunch/menu_student.json"
with open(student, 'r', encoding='utf-8') as file:
    student_data = json.load(file)



def extract_numeric_part(text):
    # Use regular expression to extract numeric part from the text
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return match.group(1)
    return None



# 음성 파일에서 텍스트 추출(STT)
def transcribe_audio(data):
    audio = speech.RecognitionAudio(content=data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='ko-KR',
    )

    response = client_stt.recognize(config=config, audio=audio)
    for result in response.results:
        return result.alternatives[0].transcript.lower()

# 텍스트를 음성 파일로 변환(TTS)
def generate_audio(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code='ko-KR',
        name='ko-KR-Wavenet-A',
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
    )

    response = client_tts.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    return response.audio_content

def main():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 3.5

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* 녹음을 시작합니다. 3.5 초간 말하세요.")

    while True:
        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* 녹음이 완료되었습니다.")

        stream.stop_stream()

        # Convert the recorded audio to bytes
        audio_data = b''.join(frames)

        # Transcribe the recorded audio
        transcript = transcribe_audio(audio_data)
        print("인식된 텍스트:", transcript)

        if "부엉" in transcript:
            print("네")

            # Generate the audio response
            audio_response = generate_audio("네에에")
            sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
            play(sound)


        if "월요일" in transcript:
            if "라면" in transcript or "라면타임" in transcript or "간식" in transcript or "간식류" in transcript:
                print("월요일 라면타임&간식류 메뉴입니다.")
                audio_response = generate_audio("월요일 라면타임과 간식류 메뉴는 " + str(student_data[0]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                    

            if "단품코너" in transcript or "단품" in transcript:
                print("월요일 단품코너 메뉴입니다.")
                audio_response = generate_audio("월요일 단품코너 메뉴는 " + str(student_data[5]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)

            if "오늘의 백반" in transcript or "백반" in transcript:
                print("월요일 오늘의 백반 메뉴입니다.")
                audio_response = generate_audio("월요일 오늘의 백반 메뉴는 " + str(student_data[10]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                

            if "교직원 식당" in transcript or "교직원" in transcript or "한누리관 9층" in transcript or "한누리관" in transcript:
                print("월요일 교직원 식당 메뉴입니다.")
                audio_response = generate_audio("월요일 교직원 식당 메뉴는 " + str(professor_data[0]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)

        if "화요일" in transcript:
            if "라면" in transcript or "라면타임" in transcript or "간식" in transcript or "간식류" in transcript:
                print("화요일 라면타임&간식류 메뉴입니다.")
                audio_response = generate_audio("화요일 라면타임과 간식류 메뉴는 " + str(student_data[1]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                

            if "단품코너" in transcript or "단품" in transcript:
                print("화요일 단품코너 메뉴입니다.")
                audio_response = generate_audio("화요일 단품코너 메뉴는 " + str(student_data[6]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                

            if "오늘의 백반" in transcript or "백반" in transcript:
                print("화요일 오늘의 백반 메뉴입니다.")
                audio_response = generate_audio("화요일 오늘의 백반 메뉴는 " + str(student_data[11]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                

            if "교직원 식당" in transcript or "교직원" in transcript or "한누리관 9층" in transcript or "한누리관" in transcript:
                print("화요일 교직원 식당 메뉴입니다.")
                audio_response = generate_audio("화요일 교직원 식당 메뉴는 " + str(professor_data[1]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
            
        if "수요일" in transcript:
            if "라면" in transcript or "라면타임" in transcript or "간식" in transcript or "간식류" in transcript:
                print("수요일 라면타임&간식류 메뉴입니다.")
                audio_response = generate_audio("수요일 라면타임과 간식류 메뉴는 " + str(student_data[2]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                

            if "단품코너" in transcript or "단품" in transcript:
                print("수요일 단품코너 메뉴입니다.")
                audio_response = generate_audio("수요일 단품코너 메뉴는 " + str(student_data[7]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                

            if "오늘의 백반" in transcript:
                print("수요일 오늘의 백반 메뉴입니다.")
                audio_response = generate_audio("수요일 오늘의 백반 메뉴는 " + str(student_data[12]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                


            if "교직원 식당" in transcript or "교직원" in transcript or "한누리관 9층" in transcript or "한누리관" in transcript:
                print("수요일 교직원 식당 메뉴입니다.")
                audio_response = generate_audio("수요일 교직원 식당 메뉴는 " + str(professor_data[2]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                
        if "목요일" in transcript:
            if "라면" in transcript or "라면타임" in transcript or "간식" in transcript or "간식류" in transcript:
                print("목요일 라면타임&간식류 메뉴입니다.")
                audio_response = generate_audio("목요일 라면타임과 간식류 메뉴는 " + str(student_data[3]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                
        
            if "단품코너" in transcript or "단품" in transcript:
                print("목요일 단품코너 메뉴입니다.")
                audio_response = generate_audio("목요일 단품코너 메뉴는 " + str(student_data[8]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                

            if "오늘의 백반" in transcript or "백반" in transcript:
                print("목요일 오늘의 백반 메뉴입니다.")
                audio_response = generate_audio("목요일 오늘의 백반 메뉴는 " + str(student_data[13]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                

            if "교직원 식당" in transcript or "교직원" in transcript or "한누리관 9층" in transcript or "한누리관" in transcript:
                print("목요일 교직원 식당 메뉴입니다.")
                audio_response = generate_audio("목요일 교직원 식당 메뉴는 " + str(professor_data[3]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)

        if "금요일" in transcript:
            if "라면" in transcript or "라면타임" in transcript or "간식" in transcript or "간식류" in transcript:
                print("금요일 라면타임&간식류 메뉴입니다.")
                audio_response = generate_audio("금요일 라면타임과 간식류 메뉴는 " + str(student_data[4]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                

            if "단품코너" in transcript or "단품" in transcript:
                print("금요일 단품코너 메뉴입니다.")
                audio_response = generate_audio("금요일 단품코너 메뉴는 " + str(student_data[9]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                

            if "오늘의 백반" in transcript or "백반" in transcript:
                print("금요일은 운영하지 않습니다.")
                audio_response = generate_audio("금요일은 운영하지 않습니다. 단품코너를 이용해주세요.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                


            if "교직원 식당" in transcript or "교직원" in transcript or "한누리관 9층" in transcript or "한누리관" in transcript:
                print("금요일 교직원 식당 메뉴입니다.")
                audio_response = generate_audio("금요일 교직원 식당 메뉴는 " + str(professor_data[4]) + "입니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                    

        if "일요일" in transcript or "토요일" in transcript:
            print("일요일은 운영하지 않습니다.")
            audio_response = generate_audio("일요일은 운영하지 않습니다.")
            sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
            play(sound)

        if "탑백 플레이리스트" in transcript or "탑백" in transcript or "인기차트" in transcript or "탑 100" in transcript:
            audio_response = generate_audio("지금 탑백을 재생합니다.")
            sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
            play(sound)
            
                        
            delay = 0.5

            sw_channel = 0
            vrx_channel = 2
            vry_channel = 1

            pygame.init()

            # 음악 파일을 재생할 창 열기
            pygame.mixer.init()

            playlist_path = "playlist"  # 실제 경로로 대체해주세요
            mp3_files = ['PerfectNight.mp3', 'Drama.mp3', 'ToX.mp3', 'Ditto.mp3', 'Seven.mp3', 'ChillKill.mp3', 'TalkSaxy.mp3']

            full_paths = [os.path.join(playlist_path, mp3) for mp3 in mp3_files]

            # 랜덤으로 시작 곡 선택
            random_file = random.choice(full_paths)
            pygame.mixer.music.load(random_file)
            pygame.mixer.music.play()

            spi = spidev.SpiDev()
            spi.open(0, 0)
            spi.max_speed_hz = 100000

            def readadc(adcnum):
                if adcnum > 7 or adcnum < 0:
                    return -1
                r = spi.xfer2([1, (8 + adcnum) << 4, 0])
                data = ((r[1] & 3) << 8) + r[2]
                return data

            # 이전 상태를 저장하는 변수
            prev_sw_val = 0
            current_song_index = 0
            is_music_playing = False
            current_volume = 0.5

            # 초기 곡 재생
            pygame.mixer.music.set_volume(current_volume)

            sw_val = readadc(sw_channel)
            vrx_pos = readadc(vrx_channel)
            vry_pos = readadc(vry_channel)
            
            while True:
                sw_val = readadc(sw_channel)
                vrx_pos = readadc(vrx_channel)
                vry_pos = readadc(vry_channel)

                if sw_val < 100:
                    print("Joystick Button Pressed")

                    if is_music_playing:
                        # If music is playing, pause it
                        pygame.mixer.music.pause()
                        is_music_playing = False
                    else:
                        # If music is paused, resume playing
                        pygame.mixer.music.unpause()
                        is_music_playing = True

                # 조이스틱 좌우 이동에 따라 이전곡과 다음곡 선택
                if vrx_pos < 300:
                    current_song_index -= 1
                    if current_song_index < 0:
                        current_song_index = len(full_paths) - 1
                    pygame.mixer.music.load(full_paths[current_song_index])
                    pygame.mixer.music.play()
                elif vrx_pos > 700:
                    current_song_index += 1
                    if current_song_index >= len(full_paths):
                        current_song_index = 0
                    pygame.mixer.music.load(full_paths[current_song_index])
                    pygame.mixer.music.play()

                # 조이스틱 위아래 이동에 따라 볼륨 극단적으로 조절
                if vry_pos < 500:
                    current_volume = current_volume * 1.5
                    # 볼륨은 0.0에서 1.0 사이의 값으로 설정
                if vry_pos > 800:
                    current_volume = current_volume * 0.5

                # 실제로 볼륨 조절
                pygame.mixer.music.set_volume(current_volume)
                # 현재 상태를 저장
                prev_sw_val = sw_val

                # 나머지 코드 및 동작
                print("X: {}, Y: {}, SW: {}".format(vrx_pos, vry_pos, sw_val))
                time.sleep(delay)

            # pygame 종료
            pygame.quit()

      
            
        bz_pin = 18

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(bz_pin, GPIO.OUT)

        if "타이머" in transcript:
            # Use regular expression to extract numeric part from the text
            match = re.search(r'(\d+)', transcript)
            numeric_part = match.group(1)
            timer_duration = int(numeric_part)
            if match:
                print(f"{numeric_part}초 동안 타이머를 맞추었습니다.")
                audio_response = generate_audio(f"{numeric_part}초 동안 타이머를 맞추었습니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)

            try:
                # Wait for the specified duration obtained from the transcript
                time.sleep(timer_duration)

                # Start the alarm loop
                p = GPIO.PWM(bz_pin, 100)
                Frq = [262, 330, 392, 330, 262, 1]
                speed = 0.5
                sw_channel = 0
                
                spi = spidev.SpiDev()
                spi.open(0, 0)
                spi.max_speed_hz = 100000
                
                i2c = busio.I2C(SCL, SDA)
                x = 0
                padding = -2
                y = padding

                display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

                # OLED 화면 초기화
                display.fill(0)
                display.show()

                font_size = 20

                # Specify a font file and create a font with the desired size
                font = ImageFont.truetype("FreeMono.ttf", font_size)

                width = display.width
                height = display.height
                image = Image.new("1", (width, height))

                draw = ImageDraw.Draw(image)
                

                numeric_part = timer_duration
                try:
                    while numeric_part >= 0:
                        draw.rectangle((0, 0, width, height), outline=0, fill=0)  # Clear the screen
                        draw.text((x, y), "Time: {}s".format(numeric_part), font=font, fill=255)
                        display.image(image)
                        display.show()

                        for fr in Frq:
                            p.ChangeFrequency(fr)
                            
                        time.sleep(0.9)
                        numeric_part -= 1

                except KeyboardInterrupt:
                    pass

            except KeyboardInterrupt:
                pass

            finally:
                p.start(10)
                while 1:
                    for fr in Frq:
                        p.ChangeFrequency(fr)
                        time.sleep(0.5)
                    time.sleep(1)
                display.fill(0)
                display.show()
                GPIO.cleanup()

        if "날씨" in transcript:
            audio_response = generate_audio("현재 날씨를 알려드립니다.")
            sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
            play(sound)
            print("현재 날씨를 보여드립니다.")
                        
            current_datetime = datetime.now()
            base_date = current_datetime.strftime("%Y%m%d")
            base_time = current_datetime.strftime("%H00")

            url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
            params ={'serviceKey' : '6gJTZlpAHG/BsVfQa7V9uirC088uzkuVL6BtWZgJKJQmxYLC3ULsEd0Pkj9bdk77MBBIrAtjjYo4uJ7tzOi/ow==', 'pageNo' : '1', 
                    'numOfRows' : '10', 'dataType' : 'JSON', 'base_date' : "20231209", 'base_time' : "0400", 'nx' : '55', 'ny' : '127' }
            response = requests.get(url, params=params) 


            if (response.status_code >= 200) or (response.status_code < 300): 
                r_dict = json.loads(response.text) 
            
                r_resultcode = r_dict["response"]["header"]["resultCode"]
                r_item = r_dict["response"]["body"]["items"]["item"]

                if r_resultcode == '00':
                    for item in r_item:
                        if (item.get("category") == "T1H"): 
                            result = item
                            obsr_value_str = result.get("obsrValue", "obsrValue not found")  # obsrValue 값을 가져옴
                            obsr_value = float(obsr_value_str)  # 문자열을 실수로 변환
                            print(obsr_value)
                            time.sleep(5)
                            audio_response = generate_audio(f"현재 날씨는 {obsr_value}도입니다.")
                            sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                            play(sound)
                            break

            
            if "종료" in transcript:
                print("대화를 종료합니다.")
                audio_response = generate_audio("대화를 종료합니다. 이용해주셔서 감사합니다.")
                sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
                play(sound)
                break

    # else:
    #     print("무슨 말씀이신지 이해하지 못했습니다.")
    #     audio_response = generate_audio("무슨 말씀이신지 이해하지 못했습니다.")
    #     sound = AudioSegment.from_file(io.BytesIO(audio_response), format="wav")
    #     play(sound)


        # Resume the stream for the next interaction
        stream.start_stream()

    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    main()
