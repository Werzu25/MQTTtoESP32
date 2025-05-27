import numpy as np
import sounddevice as sd
from tensorflow.lite.python import interpreter as tflite
import time

SAMPLE_RATE = 44100
CHUNK_DURATION = 1  # seconds
MODEL_PATH = "models/soundclassifier_with_metadata.tflite"
LABELS_PATH = "models/labels.txt"
THRESHOLD = 0.6

def record_audio(duration, sample_rate):
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    return np.squeeze(audio)

def preprocess_raw_audio(audio, input_shape):
    target_length = input_shape[1]
    if len(audio) > target_length:
        audio = audio[:target_length]
    elif len(audio) < target_length:
        audio = np.pad(audio, (0, target_length - len(audio)))
    return np.expand_dims(audio, axis=0).astype(np.float32)

def load_labels(path):
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]

def predict(interpreter, input_data):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    return interpreter.get_tensor(output_details[0]['index'])[0]

if __name__ == "__main__":
    interpreter = tflite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    input_shape = input_details[0]['shape']
    labels = load_labels(LABELS_PATH)

    print("Start speaking. Press Ctrl+C to stop.")
    try:
        while True:
            audio = record_audio(CHUNK_DURATION, SAMPLE_RATE)
            audio_input = preprocess_raw_audio(audio, input_shape)
            prediction = predict(interpreter, audio_input)
            max_prob = np.max(prediction)
            max_idx = np.argmax(prediction)
            if max_prob > THRESHOLD:
                print(f"Detected: {labels[max_idx]} ({max_prob:.2%})")
            time.sleep(0.1)  # Small delay to avoid overlap
    except KeyboardInterrupt:
        print("Stopped.")