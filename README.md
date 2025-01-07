# 🎓 Automatisation de l'émargement sur Moodle pour l'Université Bretagne Sud

Ce projet automatise l'émargement des élèves de l'Université Bretagne Sud en utilisant Selenium. 

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/MTlyx/Emargement_UBS.git && cd Emargement_UBS
```

2. Installez les dépendances Python :
```bash
pip install -r requirements.txt
```

3. Modifiez le fichier `.env` pour y stocker vos identifiants et paramètres :
```bash
MoodleUs=USER
MoodlePa=PASSWORD
```

## Lancement 
Une fois configuré, lancez le script avec :
```bash
python3 Emarge.py
```

## Configuration du fichier .env

### **MoodleUs** : 
Définissez votre identifiant pour moodle

### **MoodlePa** : 
Définissez votre mot de passe pour moodle

### **MoodleSh** :  
Définissez si vous souhaitez que le navigateur s'exécute en mode invisible :  
- `True`
- `False`

### **MoodleSt** :  
Définissez le statut à utiliser pour l'émergement :  
- `Présent`
- `Absent`
- `Excusé`
- `Absent`

### **MoodleCourseUrl** : 
Définissez l'Url du cours sur moodle

### **MoodleAttendanceUrl** : 
Définissez l'Url de l'attendance sur moodle

## ⏰ Automatisation avec Crontab

Automatisation de l'émergement tous les jours de la semaine (du lundi au vendredi) le matin et le soir 

1. ⚠️ Configuration ⚠️

Selenium doit être configuré pour s'exécuter sans ouvrir de fenêtre de navigateur
```bash
MoodleSh=True
```

2. Ouvrir l'éditeur de crontab
```bash
crontab -e
```

3. Ajouter les lignes suivantes
```bash
2 8 * * 1-5 python3 /path/to/Emargement_UBS/Emarge.py
47 14 * * 1-5 python3 /path/to/Emargement_UBS/Emarge.py
```

Les logs sont automatiquement sauvegarder dans le fichier emargement.log