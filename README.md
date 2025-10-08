# Vid-Sub: AI Subtitle Generator

This project is a web-based application that automatically generates and embeds subtitles into videos. Users can upload a video file or provide a video URL, and the application will transcribe the audio, translate it to a specified language, and burn the subtitles into the video.

## Project Overview

The application provides a simple web interface to upload a video or submit a video URL. The backend then processes the video in the following steps:

1.  **Video Download/Upload**: The video is either uploaded by the user or downloaded from a given URL.
2.  **Audio Extraction**: The audio track is extracted from the video.
3.  **Speech-to-Text**: The audio is transcribed into text with timestamps using a speech recognition model.
4.  **Translation**: The transcribed text is translated into the desired target language.
5.  **Subtitle Generation**: An SRT (SubRip Subtitle) file is created from the translated text and timestamps.
6.  **Video Encoding**: The subtitles are embedded into the original video using `ffmpeg`.
7.  **Download**: The user can download the final subtitled video.

## Features

-   File upload and URL-based video processing.
-   Automatic speech recognition.
-   Translation to multiple languages.
-   Subtitle generation in SRT format.
-   Subtitles are hard-coded into the video.
-   Real-time processing status updates.

## Tech Stack

-   **Backend**: Python, Flask
-   **Frontend**: HTML, CSS, JavaScript
-   **Speech-to-Text**: Groq API (Whisper Large)
-   **Translation**: Groq API (OpenAI GPT-OSS)
-   **Video Processing**: ffmpeg, moviepy
-   **Audio Processing**: pydub

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Vid-Sub.git
    cd Vid-Sub
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The dependencies are listed in `pyproject.toml`, you may need to generate a `requirements.txt` file or install them directly.*

4.  **Install ffmpeg:**
    Make sure you have `ffmpeg` installed on your system and that it is accessible from the command line. You can download it from [ffmpeg.org](https://ffmpeg.org/download.html).

## Configuration

1.  **API Keys**: This project requires API keys for the speech-to-text and translation services. You need to set the following environment variables:
    -   `GROQ_API_KEY`: Your API key for the Groq API.

    You can set them in your environment or create a `.env` file in the project root and add the following lines:
    ```
    GROQ_API_KEY="your_groq_api_key"
    ```

2.  **Session Secret**: For production environments, it is recommended to set a secret key for the Flask session.
    ```
    SESSION_SECRET="your_strong_secret_key"
    ```

## Usage

1.  **Start the Flask application:**
    ```bash
    python app.py
    ```

2.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:8080`.

3.  **Upload a video or provide a URL:**
    -   Select the source and target languages.
    -   Choose a video file to upload or paste a video URL.
    -   Click "Generate Subtitles".

4.  **Monitor the progress:**
    The application will show the real-time status of the video processing.

5.  **Download the video:**
    Once the processing is complete, a download link for the subtitled video will be provided.

## API Keys

The current implementation has hardcoded API keys in `gpt_translator.py` and `video_processor.py`. It is strongly recommended to replace these with environment variables for security reasons, as described in the **Configuration** section.
