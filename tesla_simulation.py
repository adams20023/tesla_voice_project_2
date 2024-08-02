import os
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key="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")

def process_command(command):
    try:
        # Create a chat completion using the new client methods
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": command}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    while True:
        command = input("Speak your command:\nCommand: ")
        if command.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        processed_command = process_command(command)
        print(f"Processed Command: {processed_command}")

if __name__ == "__main__":
    main()

