import openai
import requests
from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
import os

# API Keys
weather_api_key = "3a219c41f4034fcab1a114219240208"
news_api_key = "015af73c404b43b2b4119c94553f928d"
openai.api_key = "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"

def get_weather(location="Peterborough"):
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={location}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()

        # Debugging: Print raw response data
        print(f"Weather API response: {data}")

        if 'current' in data:
            condition = data['current']['condition']['text']
            temp_c = data['current']['temp_c']
            return f"The weather in {location} is {condition} with a temperature of {temp_c}°C."
        else:
            return "Unable to retrieve weather information."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()

        # Debugging: Print raw response data
        print(f"News API response: {data}")

        if 'articles' in data and len(data['articles']) > 0:
            top_article = data['articles'][0]
            return f"Top news: {top_article['title']} - {top_article['description']}"
        else:
            return "No news available."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def speak_response(response):
    tts = gTTS(text=response, lang='en')
    tts.save("response.mp3")
    playsound("response.mp3")
    os.remove("response.mp3")

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Recognized command: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Sorry, there was an error with the speech recognition service.")
            return None

def main():
    while True:
        command = listen_for_command()
        if command:
            print(f"Processing command: {command}")  # Debug statement
            if "weather" in command:
                location = command.split("weather in")[-1].strip()
                if not location:
                    location = "Peterborough"  # Default location
                response = get_weather(location)
            elif "news" in command:
                response = get_news()
            elif "exit" in command:
                response = "Goodbye!"
                speak_response(response)
                break
            else:
                response = "Sorry, I didn't understand that command."

            print(f"Response to speak: {response}")  # Debug statement
            speak_response(response)

if __name__ == "__main__":
    main()
