# 📰 Fake News Detection

A Machine Learning web application that analyzes news content and predicts whether it is **REAL** or **FAKE** using Natural Language Processing and Machine Learning.

This project was originally developed in **2021 as a BTech final-year team project at Aditya Engineering College**.

The original academic project has now been revisited and prepared as a deployable web application while preserving its original Machine Learning approach.

---

## 🚀 Live Demo

**Live Application:** https://fake-news-detection-4l8r.onrender.comgit 

The live version focuses on the core Fake News Detection functionality and allows users to analyze news content directly through a web interface.

---

## 📌 Project Overview

Fake news and misinformation have become major challenges with the growth of online news platforms and social media.

The objective of this project is to develop a Machine Learning model capable of identifying patterns in news content and classifying it as:

- ✅ REAL
- ⚠️ FAKE

Fake News Detection is treated as a **text classification problem**.

The core Machine Learning approach used in this project is:

```text
TF-IDF Vectorization
        ↓
Multinomial Naive Bayes
        ↓
REAL / FAKE Prediction
```

---

## 🧠 How It Works

### 1. News Input

The user provides news content to the application.

For the most reliable prediction, article text can be pasted directly into the application.

The application can also attempt to retrieve text from publicly accessible news article URLs.

### 2. Text Vectorization

The news content is transformed into numerical features using:

**TF-IDF — Term Frequency-Inverse Document Frequency**

TF-IDF represents the importance of words within the training dataset.

### 3. Classification

The transformed text is passed to a:

**Multinomial Naive Bayes Classifier**

Naive Bayes is commonly used for text classification because of its efficiency when working with word-frequency-based features.

### 4. Prediction

The application returns one of two classifications:

```text
REAL
```

or

```text
FAKE
```

---

## 🏗️ Current Application Architecture

```text
User
  │
  ▼
Web Browser
  │
  ▼
HTML / CSS Frontend
  │
  ▼
Flask Application
  │
  ▼
News Article Text
  │
  ▼
TF-IDF Vectorization
  │
  ▼
Multinomial Naive Bayes
  │
  ▼
REAL / FAKE Prediction
```

---

## 🛠️ Technology Stack

### Machine Learning

- Python
- Scikit-learn
- Pandas
- NumPy
- TF-IDF Vectorization
- Multinomial Naive Bayes

### Backend

- Flask
- Python

### Frontend

- HTML
- CSS

### Deployment

- GitHub
- Render

---

## 📂 Repository Structure

```text
Fake-News-Detection/
│
├── docs/
│   └── Original BTech project documentation
│
├── fakenewsproject/
│   ├── html/
│   │   └── main.html
│   │
│   ├── app.py
│   ├── ml.py
│   ├── model.pickle
│   ├── model_metadata.json
│   ├── news.csv
│   └── requirements.txt
│
├── nodelogin.zip
│
├── .gitignore
├── .python-version
├── render.yaml
└── README.md
```

---

## 🤖 Machine Learning Model

The project uses a Machine Learning pipeline consisting of:

```text
News Dataset
      ↓
Training / Testing Split
      ↓
TF-IDF Vectorizer
      ↓
Multinomial Naive Bayes
      ↓
Trained Classification Model
```

The original academic project reported **above 80% accuracy** using the Naive Bayes classifier.

The deployable model has been regenerated from the original dataset using the same core TF-IDF + Multinomial Naive Bayes approach so that it can run with current Python and Scikit-learn dependencies.

---

## 💻 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/harimarni/Fake-News-Detection.git
```

### 2. Enter the project

```bash
cd Fake-News-Detection/fakenewsproject
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Install dependencies

On Windows:

```bash
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 5. Start Flask

```bash
.\.venv\Scripts\python.exe app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

---

## 🌐 News URL Support

The application can attempt to retrieve article text from publicly accessible news URLs.

Some websites may prevent automated article extraction because of:

- Paywalls
- Subscription requirements
- Bot protection
- Access restrictions

If a website blocks URL extraction, the article text can be pasted directly into the application.

---

## 🔐 Original Authentication System

The original BTech project was designed as a larger system that also included:

- User registration
- Login and logout
- Password reset
- User database
- Authentication
- Dashboard
- URL validation
- Fake News Prediction

The original architecture was approximately:

```text
User
  │
  ▼
Registration / Login
  │
  ▼
Authentication
  │
  ▼
Dashboard
  │
  ▼
News Input
  │
  ▼
Flask Prediction Service
  │
  ▼
Machine Learning Model
  │
  ▼
REAL / FAKE
```

For the current public deployment, authentication is not required.

This makes the Machine Learning demonstration directly accessible without requiring visitors to register or configure a database.

The original authentication implementation has been preserved separately as:

```text
nodelogin.zip
```

Sensitive configuration files, credentials and installed dependencies are not included in the archived source.

---

## 🎓 Academic Project

This project was originally developed as a **BTech final-year team project** at:

### Aditya Engineering College

Department of Information Technology

### Project Team

- Ch. Sri Bala Vidyadhari
- P. Hari Priya
- **M. Hari Krishna**
- B. Sireesha

### Project Guide

**Mr. S. V. V. D. Jagadeesh**  
Assistant Professor  
Department of Information Technology  
Aditya Engineering College

The original project documentation and presentation are preserved in this repository for reference.

---

## 🚧 Version 2 — Coming Soon

A modernized **Version 2** of this project is planned.

The goal of Version 2 will be to improve the original Machine Learning system while keeping this implementation available as the historical baseline.

Planned improvements include:

- Newer and more diverse news datasets
- Updated text preprocessing
- Model retraining
- Comparison of multiple classification algorithms
- Accuracy evaluation
- Precision
- Recall
- F1-score
- Confusion matrix analysis
- Improved generalization to newer news content
- Updated Machine Learning pipeline
- Production-oriented deployment improvements

The objective will be to compare the original academic implementation with a more modern Fake News Detection system.

---

## ⚠️ Disclaimer

This application is an **educational Machine Learning project**.

A prediction of **REAL** or **FAKE** represents the output of a statistical classification model and should not be interpreted as definitive fact-checking.

The model was trained on the project's original dataset, and language, topics and news patterns can change over time.

Important information should always be verified using reliable news sources and professional fact-checking methods.

---

## 👨‍💻 Developer

**M. Hari Krishna**

GitHub: https://github.com/harimarni

---

## ⭐ Project Status

**Current:** Original Fake News Detection application ready for deployment.

**Next:** Version 2 with updated data, model evaluation and improved Machine Learning techniques.