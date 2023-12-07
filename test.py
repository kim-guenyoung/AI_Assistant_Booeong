from gtts import gTTS
import json

# Read the JSON file
file_name = "/home/pi/lunch/menu_faculty.json"
with open(file_name, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Convert the JSON data to a string (you can modify this based on your JSON structure)
json_text = json.dumps(json_data, ensure_ascii=False)

# Use gTTS to convert the text to speech
tts = gTTS(text=json_text, lang="ko")

# Save the speech as an audio file
tts.save("json_audio.mp3")
