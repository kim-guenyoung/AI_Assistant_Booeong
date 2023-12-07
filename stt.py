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
import random


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
            
                        
            delay = 1  # 루프 간격을 더 짧게 설정

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
            current_volume = 0.5  # 초기 볼륨 설정 (0.0에서 1.0 사이)

            # 초기 곡 재생
            pygame.mixer.music.set_volume(current_volume)

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
                    current_volume = min(1.0, current_volume * 1.5)
                    # 볼륨은 0.0에서 1.0 사이의 값으로 설정
                if vry_pos > 800:
                    current_volume = max(0.0, current_volume * 0.5)

                # 실제로 볼륨 조절
                pygame.mixer.music.set_volume(current_volume)
                # 현재 상태를 저장
                prev_sw_val = sw_val

                # 나머지 코드 및 동작
                print("X: {}, Y: {}, SW: {}".format(vrx_pos, vry_pos, sw_val))
                time.sleep(delay)

            # pygame 종료
            pygame.quit()


                

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
