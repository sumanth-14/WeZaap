from openai import OpenAI
import os

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def transcribe_audio(audio_path):
    """
    Transcribe an audio file directly using OpenAI's Whisper API.
    Supports MP3, WAV, and other formats natively.
    """
    # Open the audio file in binary mode
    with open(audio_path, 'rb') as f:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="text"
        )
    return transcription.strip()

# Example usage (optional, for testing)
if __name__ == "__main__":
    audio_file = "tmp_audio/q1_answer.webm"  # Adjust path based on your temp audio file
    try:
        transcription = transcribe_audio(audio_file)
        print("Transcription:", transcription)
    except FileNotFoundError:
        print(f"Error: The file '{audio_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")