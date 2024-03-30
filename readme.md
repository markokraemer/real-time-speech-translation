## Installation and Setup

To get started with this real-time speech translation project, follow these steps:

1. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Export your OpenAI and Groq API keys as environment variables. Replace `<Your-OpenAI-API-Key>` and `<Your-Groq-API-Key>` with your actual API keys.
   ```
   export OPENAI_API_KEY=<Your-OpenAI-API-Key>
   export GROQ_API_KEY=<Your-Groq-API-Key>
   ```

3. Run the main script to start the real-time speech translation:
   ```
   python3 main.py
   ```

4. When prompted, hit ENTER to start recording your speech. Speak clearly into your microphone. When finished, hit ENTER again to stop the recording. The script will then process your speech, translate it, and read out the translation.

## How It Works

This script facilitates real-time speech translation from any language to English. Here's a brief overview of its functionality:

- **Recording User Input**: Upon execution, the script prompts the user to start recording their speech by hitting ENTER. It captures the audio input using the microphone.

- **Transcribing Audio to Text**: The recorded audio is then transcribed to text using OpenAI's Whisper model, which can recognize and transcribe speech from various languages.

- **Translating Text**: The transcribed text is sent to a language model (specified by the `model_name` variable) which translates the text into English. This model operates under strict guidelines to ensure that only the translation is outputted, without any additional content.

- **Text-to-Speech**: Finally, the translated text is converted back into speech using OpenAI's text-to-speech model. This audio is then played back to the user, providing them with the translation of their original speech.

This process allows for a seamless conversation in any language, with real-time translations provided in English.
