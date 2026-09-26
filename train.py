# train.py - Simple training script
import pickle
import argparse
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

def main(output_path):
    X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    with open(output_path, "wb") as f:
        pickle.dump(model, f)
    print(f"Model trained and saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="model.pkl", help="Output path")
    args = parser.parse_args()
    main(args.output)
