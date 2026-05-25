# # main.py
# import sys
# import pickle
# from extract_features import extract_features

# def predict_gender(audio_path):
#     with open("model.pkl", "rb") as f:
#         model = pickle.load(f)

#     features = extract_features(audio_path)
#     if features is None:
#         return "Could not extract features"
    
#     prediction = model.predict([features])[0]
#     return "Male" if prediction == 1 else "Female"

# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument("audio_path", help="Path to .wav audio file")
#     args = parser.parse_args()

#     result = predict_gender(args.audio_path)
#     print("Predicted Gender:", result)


# copyt ..........................................
# import os
# import pickle
# import sounddevice as sd
# import soundfile as sf
# from extract_features import extract_features

# def record_voice(filename="realtime_voice.wav", duration=4, fs=44100):
#     """🎤 Record live voice for a few seconds and save inside audio_samples folder"""
#     folder = "audio_samples"
#     os.makedirs(folder, exist_ok=True)  # create folder if not exists
#     filepath = os.path.join(folder, filename)

#     print("🎙️ Speak now... Recording in progress!")
#     recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
#     sd.wait()
#     sf.write(filepath, recording, fs)
#     print(f"✅ Voice recorded and saved as {filepath}")
#     return filepath

# def predict_gender(audio_path):
#     """🔍 Predict gender using trained model"""
#     with open("model.pkl", "rb") as f:
#         model = pickle.load(f)

#     features = extract_features(audio_path)
#     if features is None:
#         return "Could not extract features"

#     prediction = model.predict([features])[0]
#     return "Male" if prediction == 1 else "Female"

# if __name__ == "__main__":
#     print("🎤 Real-Time Gender Prediction System 🎧")
#     print("----------------------------------------")
#     duration = int(input("⏱️ Enter recording duration in seconds (e.g., 4): "))

#     # Step 1: Record and save inside audio_samples/
#     recorded_file = record_voice(duration=duration)

#     # Step 2: Predict gender
#     result = predict_gender(recorded_file)
#     print(f"\n🧠 Predicted Gender: {result}")
import os
import pickle
import sounddevice as sd
import soundfile as sf
from extract_features import extract_features

# 🎤 Record live voice
def record_voice(filename="temp_voice.wav", duration=4, fs=44100):
    os.makedirs("audio_samples", exist_ok=True)
    filepath = os.path.join("audio_samples", filename)
    print("🎙️ Speak now... Recording in progress!")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    sf.write(filepath, recording, fs)
    print(f" Voice recorded and saved temporarily at {filepath}")
    return filepath

#  Predict gender using model.pkl
def predict_gender(audio_path):
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    features = extract_features(audio_path)
    if features is None:
        return None
    prediction = model.predict([features])[0]
    return "male" if prediction == 1 else "female"


#  Save voice into correct folder based on prediction
def save_voice_by_gender(audio_path, gender):
    folder = os.path.join("dataset", gender)
    os.makedirs(folder, exist_ok=True)
    existing_files = len(os.listdir(folder))
    new_filename = f"{gender}_{existing_files + 1}.wav"
    new_filepath = os.path.join(folder, new_filename)
    os.replace(audio_path, new_filepath)
    print(f"Saved as {new_filepath}")

if __name__ == "__main__":
    print(" Real-Time Gender Detection and Auto-Save System ")
    print("----------------------------------------------------")

    while True:
        duration = int(input("\n Enter recording duration (e.g., 4 sec): "))
        recorded_file = record_voice(duration=duration)

        gender = predict_gender(recorded_file)
        if gender:
            print(f" Predicted Gender: {gender.upper()}")
            save_voice_by_gender(recorded_file, gender)
        else:
            print("Could not extract features or predict gender.")

        again = input("Do you want to record again? (y/n): ").strip().lower()
        if again != 'y':
            break

    print("\n Session ended. All voices saved in dataset folders.")
