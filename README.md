# 🎓 Automatisation de l'émargement v2.1

Ce projet a pour but d'automatiser l'émargement des étudiants de l'Université Bretagne Sud, en particulier ceux de l'ENSIBS. Il utilise Selenium dans un conteneur Docker pour simuler la présence aux cours. Chaque jour de la semaine (du lundi au vendredi), un horaire aléatoire est choisi entre 5 et 15 minutes après le début du cours pour émarger.

> [!CAUTION]
> Ce dépôt Github est à utiliser avec prudence. Si vous le mettez en place, assurez-vous d'être présent à chaque cours de votre emploie du temps.

## 📌 Installation

1. Clonez le dépôt Github

```bash
git clone https://github.com/MTlyx/Emarge.git && cd Emarge
```

2. Modifiez les variables d'environnement du fichier `docker-compose.yml`

Les variables à modifier sont les suivantes :
- `ANNEE` : Année d'étude (3, 4 ou 5)
- `SEMESTRE` : Numéro du semestre (5 à 8)
- `TP` : Numéro du groupe de TP (1 à 6)
- `Us` : Votre identifiant UBS
- `Pa` : Votre mot de passe UBS

Exemple de configuration d'un 3eme année dans le TP 1
```yaml
- ANNEE=3
- SEMESTRE=6
- TP=1
- Us=E123456
- Pa=MonSuperMotDePasse
```

3. Lancez le conteneur Docker

```bash
sudo docker-compose up -d
```

## 📊 Vérification des logs

Vous pouvez vérifier les logs de deux manières :

1. Directement depuis Docker :
```bash
docker-compose logs -f
```

2. En consultant le fichier de log :
```bash
cat app/emargement.log
```

Les logs vous permettront de voir :
- Les horaires prévus d'émargement
- Les succès/échecs des émargements
- Les éventuelles erreurs de connexion
