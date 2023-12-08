import spidev
import time
import os
import pygame
import random

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