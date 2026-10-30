# Le Polymath — série 01
Six vidéos : histoire, psychologie, philosophie, corps humain, économie et mathématiques.

Le moteur compose les gravures et les textes à 1080 × 1920, 30 images/s. Les profils contiennent l'horloge commune, les sous-titres et les plans. Les composants sont dans scenes.py ; render.py gère la composition, les transitions et l'habillage. Les voix Achird sont générées en amont et livrées comme médias : aucun secret ni appel d'API n'est nécessaire sur GitHub.

Le workflow effectue le calcul des images et produit une prévisualisation avec la voix, un rapport et une planche de contrôle. La musique et les effets sont assemblés localement après récupération. Les fichiers de musique tiers et la clé Google restent hors du dépôt.

Lancer localement, depuis ce dossier :
```sh
python -m pip install -r requirements.txt
python make_video.py histoire
```
FFmpeg est requis. Les sorties vont dans out/histoire/. Le programme refuse de remplacer une sortie existante.

## Contrôles
Dimensions, cadence, nombre d'images et décodage intégral sont vérifiés pour chaque export. Les groupes de sous-titres ont été contrôlés en largeur. La vidéo sur la tache aveugle conserve les deux repères fixes pendant l'expérience : ce maintien volontaire est déclaré dans le profil et distingué d'un gel accidentel. La croix ne disparaît pas artificiellement dans le code.

Les planches ne remplacent pas un visionnage intégral sur téléphone ni une écoute critique humaine. La rétention réelle des spectateurs n'est pas déduite du nombre de coupes. Les fichiers de sources exposent les conditions et les limites des sujets.

Les visuels sont des illustrations générées et des schémas, pas des documents historiques ou anatomiques d'archives. La voix est synthétique. Aucun contenu n'est publié sur les réseaux sociaux par ce workflow.
