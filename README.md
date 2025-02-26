# 🎓 Automatisation de l'émargement v2.2

Ce projet vise à automatiser l'émargement des étudiants de l'Université Bretagne Sud, en particulier ceux de l'ENSIBS. En utilisant Selenium dans un conteneur Docker, il enregistre automatiquement leur présence en cours, évitant ainsi toute retenue sur leur salaire. Son fonctionnement : chaque jour de la semaine, il récupère les cours de l'étudiant via l'API de PlanningSup et, au début de chaque cours, il émarge automatiquement entre 15 et 25 minutes après le début du cours.

> [!CAUTION]
> Ce dépôt Github est à utiliser avec prudence. Si vous le mettez en place, assurez-vous d'être présent à chaque cours de votre emploi du temps.

## 📌 Installation

1. Clonez le dépôt Github

```bash
git clone https://github.com/MTlyx/Emarge.git && cd Emarge
```

2. Modifiez les variables d'environnement du fichier `docker-compose.yml`

Les variables à modifier sont les suivantes :
- `FORMATION` : formation de l'étudiant (cyberdefense, cyberdata ou cyberlog)
- `ANNEE` : Année d'étude (3, 4 ou 5)
- `TP` : Numéro du groupe de TP (1 à 6)
- `Us` : Votre identifiant UBS
- `Pa` : Votre mot de passe UBS
- `blacklist` : Liste de mots-clés pour exclure certains cours de l'émargement automatique

Exemple de configuration d'un cyberdefense en 3eme année dans le TP 1
```yaml
- FORMATION=cyberdefense
- ANNEE=3
- TP=1
- Us=E123456
- Pa=MonSuperMotDePasse
- blacklist=Entrainement Le Robert, Activités HACK2G2, Activités GCC
```

> [!NOTE]
> La `blacklist` est une liste de mots-clés permettant d'exclure certains cours de l'émargement automatique. Lors de l'exécution, tout cours dont le nom contient un des mots-clés de la `blacklist` ne sera pas émargé. Il est recommandé de laisser la blacklist comme dans l'exemple ci-dessus.

3. Lancez le conteneur Docker

```bash
sudo docker compose up -d
```

## 📊 Vérification des logs

Vous pouvez vérifier vos logs de deux manières :

1. Directement depuis Docker :

```bash
sudo docker compose logs -f
```

2. En consultant le fichier de log :

```bash
cat app/emargement.log
```

Les logs vous permettront de voir :
- Les horaires prévus d'émargement
- Les succès/échecs des émargements
- Les éventuelles erreurs