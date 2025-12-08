# Save this as download_real_model.py and run it
import urllib.request
import os

os.makedirs('models', exist_ok=True)

print("Downloading trained model...")
# This is a working model trained on PlantVillage dataset
url = "https://github.com/MarkoArsenovic/DeepLearning_PlantDiseases/raw/master/Models/model.h5"

try:
    urllib.request.urlretrieve(url, 'models/plant_disease_model.h5')
    print("✓ Model downloaded successfully!")
except:
    print("Download failed. Try manual download from:")
    print("https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset")