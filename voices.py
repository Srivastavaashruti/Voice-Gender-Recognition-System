import os
import speech_recognition as sr
import soundfile as sf
import datetime

# Create folders if not exist
os.makedirs("voice_data/male", exist_ok=True)
os.makedirs("voice_data/female", exist_ok=True)

# Initialize recognizer
r = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Speak something... (Google will recognize your words)")
    audio = r.listen(source)
    print("✅ Recording complete!")

# Save temp file first
filename = f"temp_{datetime.datetime.now().strftime('%H%M%S')}.wav"
with open(filename, "wb") as f:
    f.write(audio.get_wav_data())
print(f"💾 Saved temporary file: {filename}")

# Recognize speech using Google
try:
    text = r.recognize_google(audio, language="en-IN")
    print("🗣️ You said:", text)

    # 🔹 Decide folder based on keyword or voice info
    if "male" in text.lower():
        new_path = os.path.join("audio_samples/male", f"male_{datetime.datetime.now().strftime('%H%M%S')}.wav")
    elif "female" in text.lower():
        new_path = os.path.join("audio_samples/female", f"female_{datetime.datetime.now().strftime('%H%M%S')}.wav")
    else:
        new_path = os.path.join("audio_samples", f"unknown_{datetime.datetime.now().strftime('%H%M%S')}.wav")

    # Rename (move) file to correct folder
    os.replace(filename, new_path)
    print(f"✅ File saved to: {new_path}")

except sr.UnknownValueError:
    print("❌ Could not understand the audio")
except sr.RequestError as e:
    print(f"⚠️ Could not request results from Google Speech API: {e}")
