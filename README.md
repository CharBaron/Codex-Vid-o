# Codex Vidéo — Le Polymath

Six vidéos verticales : histoire, psychologie, philosophie, corps humain, économie et mathématiques. Voix synthétique Achird, gravures et animations pilotées par des profils de temps.

## Série 01

| Domaine | Sujet | Durée |
|---|---|---:|
| Histoire | Les onze jours disparus du calendrier | 59 s |
| Psychologie | Le mensonge à un dollar | 60 s |
| Philosophie | Le bateau de Thésée | 69 s |
| Corps humain | La tache aveugle | 60 s |
| Économie | Le prix zéro | 62 s |
| Mathématiques | Les trois portes de Monty Hall | 60 s |

Le code et les médias de calcul sont dans [series/](series/). Les références sont dans [series/sources/REFERENCES.md](series/sources/REFERENCES.md).

## Rendus vérifiés

- [Test six secondes réussi](https://github.com/CharBaron/Codex-Vid-o/actions/runs/41037434104) : 15,59 s de rendu et contrôles sur GitHub, contre 50,13 s localement lors de l'essai compact. Comparaison ponctuelle, pas un benchmark contrôlé.
- [Six rendus de série réussis](https://github.com/CharBaron/Codex-Vid-o/actions/runs/41047090214).
- [Correction ciblée psychologie réussie](https://github.com/CharBaron/Codex-Vid-o/actions/runs/41048694550) : apparition du billet de 20 dollars alignée au passage « D'autres ».

GitHub calcule les images et une prévisualisation avec la voix. Le mix final avec musique et effets est assemblé localement ; les six MP4 terminés sont livrés dans le chat et le dossier de travail. Les fichiers de musique tiers et la clé Google ne sont pas dans ce dépôt. Aucun appel à une API de génération n'est nécessaire pour recalculer les images à partir des voix fournies.

## Reproduction

Avec Python 3.12 et FFmpeg installés :

```sh
python -m pip install -r series/requirements.txt
python series/make_video.py histoire
```

Les sorties vont dans `series/out/histoire/`. Les programmes préservent les sorties existantes. Les workflows permettent également un lancement manuel depuis Actions.

## Périmètre des contrôles

1080 × 1920, 30 images/s ; nombre d'images et décodage intégral vérifiés ; fichiers récupérés avec contrôle SHA-256. La vidéo sur la tache aveugle contient un maintien volontaire des repères pour l'expérience, déclaré dans son profil. La croix reste effectivement dessinée.

Les planches et les contrôles automatiques ne remplacent pas une écoute intégrale ou un test sur téléphone. Le nombre de coupes ne prouve pas une amélioration de la rétention : celle-ci sera à mesurer après publication.

Les polices et la variante adaptée sont accompagnées de leurs [licences](series/fonts/licenses/). Les visuels sont des illustrations, pas des documents historiques ou anatomiques d'archives. Aucune publication sur les réseaux sociaux n'est effectuée par ces workflows.
