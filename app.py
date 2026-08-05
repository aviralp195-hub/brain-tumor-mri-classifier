"""
Brain Tumor MRI Detection — Flask backend
-------------------------------------------------
Loads the trained model (model.h5, exported from the notebook) and exposes:
  GET  /            -> the web page (upload UI)
  POST /predict      -> runs the model on an uploaded MRI image, returns JSON

Preprocessing here matches the notebook EXACTLY:
  - resize to IMAGE_SIZE x IMAGE_SIZE (128x128)
  - divide pixel values by 255.0
  - add a batch dimension before model.predict()
"""

import os
import io

import numpy as np
from flask import Flask, request, jsonify, render_template
from PIL import Image
from tensorflow.keras.models import load_model

# ---------------------------------------------------------------------------
# Config — edit these if your training setup differs
# ---------------------------------------------------------------------------
IMAGE_SIZE = 128
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.h5")

# IMPORTANT: this order MUST match the order used during training
# (i.e. the order os.listdir(train_dir) returned when you ran encode_label()).
# The notebook used: ['pituitary', 'glioma', 'notumor', 'meningioma']
# If your predictions look "shifted" (e.g. tumor images say No Tumor and
# vice-versa), this list is very likely out of order — check your Training
# folder's actual listing order and fix it here.
CLASS_LABELS = ["pituitary", "glioma", "notumor", "meningioma"]

MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "webp"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE_MB * 1024 * 1024

# ---------------------------------------------------------------------------
# Load model once at startup
# ---------------------------------------------------------------------------
model = None
model_load_error = None
try:
    model = load_model(MODEL_PATH)
except Exception as exc:  # noqa: BLE001
    model_load_error = str(exc)
    print(f"[WARN] Could not load model at {MODEL_PATH}: {model_load_error}")
    print("       Drop your trained model.h5 next to app.py and restart the server.")


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(file_bytes: bytes) -> np.ndarray:
    """Mirrors the notebook's load_img + img_to_array + /255.0 pipeline."""
    img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
    arr = np.array(img).astype("float32") / 255.0
    arr = np.expand_dims(arr, axis=0)  # batch dimension
    return arr


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "ok" if model is not None else "model_not_loaded",
            "error": model_load_error,
        }
    )


@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return (
            jsonify(
                {
                    "error": "Model not loaded on server. Place your trained "
                    "model.h5 file in the project folder and restart the app."
                }
            ),
            503,
        )

    if "file" not in request.files:
        return jsonify({"error": "No file was sent."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return (
            jsonify(
                {"error": "Unsupported file type. Please upload a PNG/JPG image."}
            ),
            400,
        )

    try:
        file_bytes = file.read()
        img_array = preprocess_image(file_bytes)

        predictions = model.predict(img_array, verbose=0)[0]
        predicted_index = int(np.argmax(predictions))
        predicted_label = CLASS_LABELS[predicted_index]
        confidence = float(predictions[predicted_index])

        has_tumor = predicted_label != "notumor"

        all_probs = [
            {"label": CLASS_LABELS[i], "confidence": float(predictions[i])}
            for i in range(len(CLASS_LABELS))
        ]
        all_probs.sort(key=lambda x: x["confidence"], reverse=True)

        return jsonify(
            {
                "prediction": predicted_label,
                "has_tumor": has_tumor,
                "confidence": confidence,
                "display_result": (
                    f"Tumor detected: {predicted_label}"
                    if has_tumor
                    else "No tumor detected"
                ),
                "all_probabilities": all_probs,
            }
        )

    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": f"Could not process image: {exc}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
