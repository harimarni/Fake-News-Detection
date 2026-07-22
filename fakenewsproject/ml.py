"""Train and evaluate the Fake News Detection model.

This preserves the original project architecture: TF-IDF text features followed by
Multinomial Naive Bayes. The script evaluates on a deterministic 80/20 holdout,
then retrains on the complete bundled dataset and writes model.pickle.
"""
from pathlib import Path
import json
import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "news.csv"
MODEL_PATH = BASE_DIR / "model.pickle"
METADATA_PATH = BASE_DIR / "model_metadata.json"


def build_model() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(stop_words="english")),
        ("nb", MultinomialNB(alpha=0.01)),
    ])


def main() -> None:
    news = pd.read_csv(DATA_PATH).dropna(subset=["text", "label"]).copy()
    news["text"] = news["text"].astype(str)
    news["label"] = news["label"].astype(str).str.upper()

    X = news["text"]
    y = news["label"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    evaluation_model = build_model()
    evaluation_model.fit(X_train, y_train)
    predictions = evaluation_model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, predictions, average="weighted", zero_division=0
    )

    print(classification_report(y_test, predictions))
    print(f"Holdout accuracy: {accuracy:.2%}")

    final_model = build_model()
    final_model.fit(X, y)
    with MODEL_PATH.open("wb") as handle:
        pickle.dump(final_model, handle, protocol=pickle.HIGHEST_PROTOCOL)

    metadata = {
        "dataset_rows": int(len(news)),
        "real_rows": int((y == "REAL").sum()),
        "fake_rows": int((y == "FAKE").sum()),
        "evaluation_split": "80/20 stratified holdout, random_state=42",
        "holdout_accuracy": round(float(accuracy), 4),
        "weighted_precision": round(float(precision), 4),
        "weighted_recall": round(float(recall), 4),
        "weighted_f1": round(float(f1), 4),
        "algorithm": "TF-IDF + Multinomial Naive Bayes",
        "naive_bayes_alpha": 0.01,
        "note": "Metrics are evaluation results from a fixed holdout split; final deployment model is retrained on the full bundled dataset.",
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Saved model to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
