from llm import make_llm_api_call
import json
from pathlib import Path
from openai import OpenAI
import subprocess
import playsound  # Import playsound for directly playing audio
import sounddevice as sd
from scipy.io.wavfile import write
import wavio
import threading
import queue
import numpy as np

# Make sure to initialise your OpenAI & Groq API Key 

def record_user_audio(filename="user_input.wav", fs=44100):
    def callback(indata, frames, time, status):
        q.put(indata.copy())

    q = queue.Queue()

    input("Hit ENTER to start recording...")
    print("Recording...")
    with sd.InputStream(samplerate=fs, channels=1, dtype='int16', callback=callback):
        q = queue.Queue()
        frames = []
        input("Hit ENTER again to stop recording...")
        while True:
            try:
                frame = q.get_nowait()
            except queue.Empty:
                break
            frames.append(frame)
        recording = np.concatenate(frames, axis=0)
    wavio.write(filename, recording, fs, sampwidth=2)
    print("Recording finished.")

def transcribe_user_audio(filename="user_input.wav"):
    client = OpenAI()
    with open(filename, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcription.text

def converse_with_model():
    client = OpenAI()
    conversation_history = [{"role": "system", "content": "You are a translator who accepts inputs in any language and translates them into English.\n\nRULES:\n- You only output the English translation, nothing else. Just the exact sentence in English.\n\nExamples\n- If the user message, INPUT is \"Hallo, wie geht es dir?\" then your OUTPUT is \"Hey how are you doing?\"\"\n- DO NOT UNDER ANY CIRCUMSTANCE WRITE MORE THAN THE TRANSLATION, DO NOT INCLUDE ANY NOTES OR OTHER UNRELATED CONTENT. ONLY OUTPUT THE JSON.\n\nOutput your answer in the following JSON Format:\n{\n\"content-translated-into-english\": \" <Translation here> \"\n}"}]
    model_name = "groq/mixtral-8x7b-32768"
    
    print("You can start the conversation in any language and you will get the translation. Type 'exit' to end the conversation.")
    
    while True:
        print("Say something ('exit' to end): ")
        record_user_audio()
        user_input = transcribe_user_audio()
        print("You:", user_input)
        
        if user_input.lower() == 'exit':
            print("Exiting conversation.")
            break
        
        conversation_history.append({"role": "user", "content": user_input})
        
        try:
            response = make_llm_api_call(conversation_history, model_name, json_mode=True)
            response_content = response.choices[0].message['content']
            response_json = json.loads(response_content)
            assistant_message = response_json["content-translated-into-english"]

            print("Assistant:", assistant_message)
            conversation_history.append({"role": "assistant", "content": assistant_message})

            # Text-to-speech & play the responses
            speech_file_path = Path(__file__).parent / "speech.mp3"
            tts_response = client.audio.speech.create(
              model="tts-1",
              voice="alloy",
              input=assistant_message
            )
            tts_response.stream_to_file(speech_file_path)
            # Directly play the audio file using playsound
            playsound.playsound(str(speech_file_path))

        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    converse_with_model()


