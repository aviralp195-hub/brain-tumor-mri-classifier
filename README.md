# Cortex Scan — Brain Tumor MRI Website

Aapke notebook ke model ko ek working website mein integrate karne ke liye poora
Flask + HTML/CSS/JS project ready hai. Bas 3 kaam karne hain.

## Step 1 — model.h5 nikaalo Colab se

Aapke notebook mein ye cell already hai (Cell 21):

```python
model.save('model.h5')
```

1. Poora notebook Colab mein run karo (training complete hone tak).
2. Uske baad Colab ke left sidebar mein **Files** icon pe click karo → `model.h5`
   dikhega → uspar right-click karke **Download** karo.
   (Agar wahan nahi dikh raha, ye line chalao: `from google.colab import files; files.download('model.h5')`)

## Step 2 — model.h5 project folder mein daalo

Downloaded `model.h5` file ko is folder ke andar copy karo, `app.py` ke bilkul
saath (same level pe):

```
brain-tumor-website/
├── app.py
├── model.h5   ← yahan
├── requirements.txt
├── templates/index.html
└── static/...
```

## Step 3 — install aur run karo

Terminal mein project folder ke andar:

```bash
pip install -r requirements.txt
python app.py
```

Fir browser mein kholo: **http://localhost:5000**

Image upload karo → "Analyze scan" dabao → result (tumor type + confidence
%) turant screen pe aa jayega.

## ⚠️ Ek important cheez check karna

`app.py` ke top pe ye line hai:

```python
CLASS_LABELS = ["pituitary", "glioma", "notumor", "meningioma"]
```

Ye order EXACTLY wahi hona chahiye jo training ke time `os.listdir(train_dir)`
ne diya tha (notebook Cell 8 ke `encode_label` function mein use hua hai).
Agar website result ulta/galat de raha lage (e.g. tumor wali image "No Tumor"
bata rahi ho), toh sabse pehle yahi order check karo — apne Google Drive
"Training" folder ko dekho ki uske andar 4 sub-folders kis order mein list
hote hain, aur waisa hi order yahan set karo.

## Agar model.h5 bahut bada hai ya deploy karna hai

- Localhost pe test karne ke baad, deploy ke liye Render.com, Railway.app,
  ya PythonAnywhere jaise free/cheap options use kar sakte ho — sabpe Flask
  apps directly deploy ho jaate hain.
- Agar deploy karte waqt "model too large" jaisi dikkat aaye, batana — hum
  model ko lighter format (TFLite) mein convert karke size kam kar sakte hain.
