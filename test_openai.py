import speech_recognition as sr
from openai import OpenAI

# Your actual API key
api_key = "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"

# Initialize OpenAI client with your API key
client = OpenAI(api_key=api_key)

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating response: {e}"

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            return command
        except sr.UnknownValueError:
            return "Sorry, I did not understand the audio."
        except sr.RequestError as e:
            return f"Sorry, there was an error with the request: {e}"

def main():
    while True:
        command = listen_for_command()
        print("Recognized command:", command)
        response = generate_response(command)
        print("Processed Command:", response)

if __name__ == "__main__":
    main()

