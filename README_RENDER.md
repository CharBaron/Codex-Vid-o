# Test de rendu GitHub — Le Polymath

Ce dossier est la racine du futur dépôt de test. Il contient uniquement le moteur nécessaire, quelques visuels, les polices et six secondes de la narration déjà générée. La clé Google, les environnements locaux et les anciens projets ne sont pas inclus.

## Déroulement
Le workflow .github/workflows/render-test.yml se lance manuellement depuis Actions. Il utilise un runner Linux standard, installe les dépendances, calcule 180 images en 1080 × 1920 à 30 i/s, ajoute l'extrait de voix puis vérifie les dimensions, la durée et le décodage intégral. Le MP4 et le résultat JSON sont récupérables comme fichiers de résultat pendant trois jours.

## État
La validation locale est enregistrée dans qa/local-test.log et qa/result.json lorsqu'elle est terminée. Un succès local ne constitue pas un succès GitHub : le dépôt, l'accès et un run distant terminé sont nécessaires. Aucun résultat distant n'est encore revendiqué.

## Ce que le test ne prouve pas
Il ne mesure pas la rétention des spectateurs, ne remplace pas une écoute et une revue visuelle et ne garantit pas que GitHub sera plus rapide que ce Mac. Le temps distant sera comparé au temps local avant de choisir la méthode pour la série.

## Usage GitHub
Créer un dépôt vide et envoyer son URL dans le chat. Une fois l'accès GitHub confirmé, ce dossier pourra être publié et le test déclenché. Aucun déclenchement automatique à chaque modification. Durée maximale du job : 15 minutes ; une seule exécution à la fois.

GitHub facture les runners standards privés selon le quota du compte. Les runners standards publics sont gratuits selon la documentation consultée le 30 octobre 2026 ; la visibilité du dépôt reste le choix de Charles.
https://docs.github.com/en/billing/concepts/product-billing/github-actions
