# 🎓 Automatisation de l'émargement v2.1

Ce projet a pour but d'automatiser l'émargement des élèves de l'Université Bretagne Sud, en particulier ceux de l'ENSIBS, à l'aide de Selenium dans un conteneur docker. Chaque jours de la semaine, deux horaires aléatoires sont choisis pour émarger le matin et le soir.

> [!CAUTION]
> Ce dépôt Github est à utiliser avec prudence. Si vous le mettez en place, assurez-vous d'être présent à chaque cours. 

## 📌 Installation

1. Clonez le dépôt github

```shell
git clone https://github.com/MTlyx/Emarge.git && cd Emarge
```

2. Modifiez les variables d'environnement du fichier `docker-compose.yml`

Pour les 3ᵉ années, seul l'utilisateur et le mot de passe doivent être modifiés. Pour les autres, il faudra également changer les identifiants du cours `CourseID` et de l'émargement `AttendanceID`.

```shell
- CourseID=10731
- AttendanceID=433339
- Us=USER
- Pa=PASS
```

3. Lancez le conteneur docker

```shell
sudo docker-compose up -d
```
