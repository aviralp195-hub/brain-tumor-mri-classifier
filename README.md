
# Brain Tumor MRI Classifier

A deep learning web application that classifies brain MRI scans into four
categories — **glioma**, **meningioma**, **pituitary tumor**, or **no tumor**
— using a fine-tuned **VGG16** convolutional neural network, served through
a Flask backend with a custom web interface.

## Overview

- **Model**: Transfer learning on VGG16, fine-tuned for 4-class MRI classification
- **Input size**: 128×128 RGB images
- **Backend**: Flask (Python) serving predictions via a `/predict` API endpoint
- **Frontend**: HTML/CSS/JavaScript — drag-and-drop image upload with a live
  confidence breakdown for each class
- **Training/experimentation**: see [`brain_tumour_detection_using_deep_learning.ipynb`](./brain_tumour_detection_using_deep_learning.ipynb)
  for data preprocessing, model architecture, training, and evaluation

## Project Structure

```
brain-tumor-mri-classifier/
├── app.py                          # Flask backend (loads model, serves predictions)
├── brain_tumour_detection_using_deep_learning.ipynb   # model training & evaluation
├── requirements.txt                 # Python dependencies
├── templates/
│   └── index.html                   # Web UI
└── static/
    ├── css/style.css                # Styling
    └── js/script.js                 # Client-side logic (upload, API calls)
```

## Model File

`model.h5` is not included in this repository due to its size (~120 MB).
Download it here and place it in the project root, alongside `app.py`:

**[Download model.h5](PASTE_YOUR_GOOGLE_DRIVE_LINK_HERE)**

## Setup & Usage

1. Clone this repository and download `model.h5` into the project root
   (see above).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open `http://localhost:5000` in your browser, upload an MRI scan, and
   click **Analyze scan** to see the predicted class and confidence scores.

## Important Note on Class Labels

The prediction labels in `app.py` must match the class order used during
training (`os.listdir(train_dir)` in the notebook). If predictions appear
inverted or incorrect, verify this order against your training data folder
structure and update `CLASS_LABELS` in `app.py` accordingly.

## Disclaimer

This project is intended for educational and research purposes only. It is
**not a certified medical device** and should not be used for actual
clinical diagnosis. Always consult a licensed radiologist or physician.

## Tech Stack

`Python` · `TensorFlow / Keras` · `Flask` · `HTML/CSS/JavaScript` · `VGG16`
