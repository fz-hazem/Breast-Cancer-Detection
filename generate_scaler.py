import os
import pickle
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler

print("Chargement des données pour l'entraînement du scaler...")
# On charge le dataset standard correspondant à votre modèle
data = load_breast_cancer()
X = data.data  # Contient les 30 caractéristiques

# Entraînement du Scaler
scaler = StandardScaler()
scaler.fit(X)

# Définition de l'emplacement de sauvegarde (dans le dossier 'models')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(BASE_DIR, 'models')

# Si le dossier 'models' n'existe pas, on le crée
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

scaler_path = os.path.join(models_dir, 'scaler.pkl')

# Sauvegarde du fichier scaler.pkl
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)

print(f"✓ Fichier généré avec succès dans : {scaler_path}")