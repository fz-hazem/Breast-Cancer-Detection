import os
import pickle
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

print("Entraînement d'un modèle équilibré...")

# 1. Chargement complet des données
data = load_breast_cancer()
X = data.data
y = data.target

# 2. Séparation train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Ajustement et sauvegarde du Scaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# 4. Entraînement du modèle
model = LogisticRegression(max_iter=5000, C=0.1)
model.fit(X_train_scaled, y_train)

score = model.score(scaler.transform(X_test), y_test)
print(f"Précision du modèle : {score * 100:.2f}%")

# 5. Sauvegarde physique dans le dossier 'models'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(BASE_DIR, 'models')
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

with open(os.path.join(models_dir, 'model.pkl'), 'wb') as f:
    pickle.dump(model, f)

with open(os.path.join(models_dir, 'scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print("✓ Modèle et Scaler synchronisés et optimisés dans 'models/' !")