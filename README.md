# 🌦️ Fuzzy Logic Weather Outlook Predictor

A simple Flask web app that predicts the weather outlook (Bad, Moderate, Good) using **fuzzy logic** principles. Input the current weather conditions — get an intelligent, human-like forecast.

---

## 🔍 What Is This?

This project demonstrates how fuzzy logic can be applied to real-world decision-making — in this case, predicting how the weather *feels* based on:

- 🌧️ Precipitation  
- 🌡️ Temperature  
- 🌬️ Wind Speed  
- 💧 Humidity  

---

## ✨ Features

- 🔁 **Fuzzy Inference System** built with `scikit-fuzzy`
- 🧠 **Human-style reasoning** with `if-then` fuzzy rules
- 💬 **Clear, categorical output**: Bad • Moderate • Good
- 🌐 **Web interface** for easy input and interaction

---

## ⚙️ How It Works

1. **Fuzzification**: Inputs (precipitation, temperature, wind speed, humidity) are converted into fuzzy values using predefined fuzzy sets.

2. **Rule Evaluation**: A set of fuzzy `IF-THEN` rules determine how these inputs influence the weather outlook.

   Examples:
   - `IF Precipitation IS heavy OR Wind Speed IS strong THEN Weather Outlook IS bad`
   - `IF Temperature IS mild AND Humidity IS medium THEN Weather Outlook IS moderate`
   - `IF Precipitation IS none AND Humidity IS low THEN Weather Outlook IS good`

3. **Defuzzification**: The fuzzy output is turned into a crisp value, then mapped to:
   - 🟥 **Bad**
   - 🟨 **Moderate**
   - 🟩 **Good**

---

## 🚀 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Create Virtual Environment (optional but recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install Flask numpy scikit-fuzzy
   ```

---

## ▶️ Run the App

Once setup is complete, run the app with:

```bash
python app.py
```

Visit `http://localhost:5000` in your browser to use the predictor.

---

## 🧠 Powered By

- [Flask](https://flask.palletsprojects.com/)
- [scikit-fuzzy](https://github.com/scikit-fuzzy/scikit-fuzzy)
- [NumPy](https://numpy.org/)

---

## 📌 Final Notes

This project is meant to demonstrate how fuzzy logic can bring a human-like decision system to life — not just in theory, but in action.

Give it a try and feel the fuzz! 🌫️
