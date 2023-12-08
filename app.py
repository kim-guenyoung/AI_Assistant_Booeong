# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import spidev
import time
import os
import pygame
import random

app = Flask(__name__)
socketio = SocketIO(app)

delay = 0.5

sw_channel = 0
vrx_channel = 2
vry_channel = 1

pygame.init()
pygame.mixer.init()

playlist_path = "playlist"
mp3_files = ['PerfectNight.mp3', 'Drama.mp3', 'ToX.mp3', 'Ditto.mp3', 'Seven.mp3', 'ChillKill.mp3', 'TalkSaxy.mp3']
full_paths = [os.path.join(playlist_path, mp3) for mp3 in mp3_files]

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

prev_sw_val = 0
current_song_index = 0
is_music_playing = False
current_volume = 0.5

pygame.mixer.music.set_volume(current_volume)

def joystick_control():
    global current_song_index, is_music_playing, current_volume, prev_sw_val

    while True:
        sw_val = readadc(sw_channel)
        vrx_pos = readadc(vrx_channel)
        vry_pos = readadc(vry_channel)

        if sw_val < 100:
            print("Joystick Button Pressed")

            if is_music_playing:
                pygame.mixer.music.pause()
                is_music_playing = False
            else:
                pygame.mixer.music.unpause()
                is_music_playing = True

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

        if vry_pos < 500:
            current_volume = min(current_volume * 1.5, 1.0)
        if vry_pos > 800:
            current_volume = max(current_volume * 0.5, 0.0)

        pygame.mixer.music.set_volume(current_volume)
        prev_sw_val = sw_val

        socketio.emit('update', {'vrx_pos': vrx_pos, 'vry_pos': vry_pos, 'sw_val': sw_val})
        time.sleep(delay)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('update', {'vrx_pos': 0, 'vry_pos': 0, 'sw_val': 0})

if __name__ == '__main__':
    socketio.start_background_task(joystick_control)
    socketio.run(app, debug=True)
