import os
import requests
from pydub import AudioSegment
import speech_recognition as sr
import sys
import subprocess
from openai import OpenAI
import time

# Initialize OpenAI Client
client = OpenAI(api_key='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')

# API Keys
weather_api_key = '3a219c41f4034fcab1a114219240208'
news_api_key = '015af73c404b43b2b4119c94553f928d'

# File Paths
audio_file_path = os.path.expanduser('~/Desktop/sample.mp3')  
wav_file_path = 'new_test_audio.wav'   

# Install missing packages
def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    except subprocess.CalledProcessError:
        print(f"Failed to install {package_name}")

def ensure_dependencies():
    packages = ['pydub', 'SpeechRecognition', 'requests', 'openai', 'ffmpeg-python']
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} is not installed. Installing...")
            install_package(package)
            try:
                __import__(package)
            except ImportError:
                print(f"Failed to install {package}")

ensure_dependencies()

# Convert MP3 to WAV
def convert_audio_to_wav(mp3_path, wav_path):
    try:
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format='wav')
    except Exception as e:
        print(f"Error converting audio: {e}")

# Convert Audio to Text
def audio_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    retry_count = 3
    while retry_count > 0:
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio_data = recognizer.record(source)
                return recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            retry_count -= 1
            time.sleep(5)  # Wait before retrying
        except Exception as e:
            return f"An error occurred: {e}"
    return "Failed to recognize audio after several attempts."

# Get OpenAI Completion Response
def get_openai_response(prompt):
    try:
        response = client.completions.create(
            model='curie',
            prompt=prompt
        )
        return response.choices[0].text
    except Exception as e:
        return f"Error with OpenAI API: {e}"

# Get Weather Information
def get_weather():
    try:
        response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q=London')
        return response.json().get('current', {}).get('temp_c', 'No weather data available')
    except Exception as e:
        return f"Error fetching weather data: {e}"

# Get News Headlines
def get_news():
    try:
        response = requests.get(f'https://newsapi.org/v2/top-headlines?apiKey={news_api_key}&country=us')
        articles = response.json().get('articles', [])
        return [article['title'] for article in articles[:5]]  
    except Exception as e:
        return f"Error fetching news data: {e}"

# Main Function
def main(audio_file_path):
    try:
        # Convert and process audio
        convert_audio_to_wav(audio_file_path, wav_file_path)
        
        # Convert audio to text
        user_message = audio_to_text(wav_file_path)
        print(f"User Message: {user_message}")

        if user_message.startswith("Sorry"):
            print(user_message)
            return
        
        # Get response from OpenAI
        response = get_openai_response(user_message)
        print(f"OpenAI Response: {response}")

        # Get weather and news information
        weather_info = get_weather()
        print(f"Current Weather: {weather_info}°C")
        
        news_headlines = get_news()
        print("Top News Headlines:")
        for headline in news_headlines:
            print(f"- {headline}")

    except Exception as e:
        print(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main(audio_file_path)
