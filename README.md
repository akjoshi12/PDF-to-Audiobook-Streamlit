# PDF to Audiobook Converter (Streamlit Edition)

This project is a web-based application built with Streamlit that converts PDF files into audiobooks. Users can upload a PDF, choose from a variety of voices, and generate an MP3 audio file of the document's content.

## Features

- **PDF to Audio Conversion:** Extracts text from uploaded PDF files and converts it into speech.
- **Voice Selection:** Allows users to choose from a wide range of voices for the audiobook generation, powered by Microsoft Edge's online text-to-speech service.
- **Simple Interface:** A clean and simple user interface built with Streamlit.
- **Audio Playback and Download:** Once the audiobook is generated, it can be played directly in the browser or downloaded as an MP3 file.

## Technologies Used

- **Streamlit:** A fast and easy way to create data apps.
- **edge-tts:** A Python library that uses Microsoft Edge's online text-to-speech service to convert text to speech.
- **pydub:** A Python library to work with audio files.
- **pdfplumber:** A library to extract text from PDF files.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/pdf_to_audiobook_fastapi.git
    cd pdf_to_audiobook_fastapi
    ```

2.  **Install dependencies:**
    Install the required Python packages using pip.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    From the project's root directory, run the Streamlit app.
    ```bash
    streamlit run app.py
    ```
    The application will be running at the URL provided by Streamlit in your terminal.

## Usage

1.  **Open the web interface:**
    Open the URL provided by Streamlit in your web browser.

2.  **Upload a PDF:**
    Click the "Upload your PDF" button and select a PDF file from your computer.

3.  **Select a Voice:**
    Choose a voice from the dropdown menu.

4.  **Convert:**
    Click the "Convert to Audiobook" button to start the conversion process. The progress bar will show the status of the conversion.

5.  **Playback and Download:**
    Once the conversion is complete, an audio player will appear. You can play the audiobook directly or download it to your device using the "Download Audiobook (MP3)" button.