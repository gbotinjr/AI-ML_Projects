import pickle
import os

def test_model_file_exists():
    assert os.path.exists("model.pkl"), "Model artifact was not generated!"

def test_model_loads_and_predicts():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    assert hasattr(model, "predict"), "Loaded object is not a valid sklearn model"
    # Test prediction on dummy data
    dummy_data = [[0.0] * 10]
    pred = model.predict(dummy_data)
    assert len(pred) == 1, "Model prediction output shape is incorrect"
