import os
import threading
import speech_recognition as sr
import requests
from gtts import gTTS
from playsound import playsound

# Weather API details
WEATHER_API_KEY = '135df778cb684e289dc110848243107'
NEWS_API_KEY = '015af73c404b43b2b4119c94553f928d'
CITY = 'Peterborough'

def get_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={CITY}&aqi=no"
    response = requests.get(url).json()
    condition = response['current']['condition']['text']
    temperature = response['current']['temp_c']
    return f"The weather in {CITY} is {condition} with a temperature of {temperature}°C."

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?q={CITY}&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response.get('articles', [])
    if articles:
        title = articles[0]['title']
        source = articles[0]['source']['name']
        return f"Here's the latest news: {title} - {source}"
    else:
        return "No news available."

def play_audio(filename):
    playsound(filename)
    os.remove(filename)

def speak_response(response):
    tts = gTTS(text=response, lang='en')
    filename = "response.mp3"
    tts.save(filename)
    
    # Use a thread to play the audio file
    audio_thread = threading.Thread(target=play_audio, args=(filename,))
    audio_thread.start()

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Recognized command: {command}")
            return command
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def process_command(command):
    if 'weather' in command:
        response = get_weather()
    elif 'news' in command:
        response = get_news()
    else:
        response = "I didn't understand the command."
    return response

def main():
    while True:
        command = listen_for_command()
        if command:
            response = process_command(command)
            print(f"Processed Command: {response}")
            speak_response(response)

if __name__ == "__main__":
    main()

