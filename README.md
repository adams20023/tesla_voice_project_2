# Tesla Voice Project

This project is designed to process audio files, transcribe speech to text, and use the OpenAI API to generate responses. Additionally, it fetches weather information and news headlines.

## Features

- Convert MP3 files to WAV format
- Transcribe audio to text using Google Speech Recognition
- Generate responses using OpenAI API
- Fetch current weather information
- Fetch top news headlines

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/adams20023/tesla_voice_project_2.git
    cd tesla_voice_project_2
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Ensure `ffmpeg` is installed on your system. If not, install it:

    - On macOS using Homebrew:

        ```bash
        brew install ffmpeg
        ```

    - On Ubuntu:

        ```bash
        sudo apt update
        sudo apt install ffmpeg
        ```

    - On Windows, download and install from [FFmpeg](https://ffmpeg.org/download.html).

## Usage

1. Add your API keys in the `ai_system.py` file:

    ```python
    weather_api_key = 'your_weather_api_key'
    news_api_key = 'your_news_api_key'
    openai.api_key = 'your_openai_api_key'
    ```

2. Run the main script:

    ```bash
    python ai_system.py
    ```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request.

## License

This project is licensed under the MIT License.
