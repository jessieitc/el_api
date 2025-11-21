#packages: pip install elevenlabs
#pip install python-dotenv

import os
from typing import IO
import io
from fastapi.responses import StreamingResponse
#from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY

#ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
elevenlabs = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

def elevenlabs_tts(text: str):
    # Perform the text-to-speech conversion
    try:
        response = elevenlabs.text_to_speech.stream(
            voice_id="pNInz6obpgDQGcFmaJgB", # Adam pre-made voice
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_multilingual_v2",
        # Optional voice settings that allow you to customize the output
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
                speed=1.0,
        ),
    )

    # Collect all audio chunks into a single byte array
        audio_bytes = io.BytesIO()
        for chunk in response:
            audio_bytes.write(chunk)

        return audio_bytes.getvalue()
    # Return the stream
    #return StreamingResponse(response, media_type="audio/mp3")
    except Exception as e:
        # print the real ElevenLabs error
        print("🔥 ElevenLabs TTS ERROR:", e)
        raise

def elevenlabs_stt():
    audio_file_path = "kwame1.m4a"

    # Open the file in binary read mode and read its content
    with open(audio_file_path, "rb") as audio_file:
        audio_data_bytes = audio_file.read()

    # Wrap the bytes in BytesIO
    audio_data = io.BytesIO(audio_data_bytes)

    transcription = elevenlabs.speech_to_text.convert(
        file=audio_data,
        model_id="scribe_v1", # Model to use, for now only "scribe_v1" is supported
        tag_audio_events=True, # Tag audio events like laughter, applause, etc.
        language_code="eng", # Language of the audio file. If set to None, the model will detect the language automatically.
        diarize=True, # Whether to annotate who is speaking
    )
    return transcription.text