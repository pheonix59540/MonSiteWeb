#!/bin/bash

echo "🚀 Démarrage de la mise à jour Git..."

# Étape 1 : Ajouter tous les changements
git add .

# Étape 2 : Créer un commit
echo "📝 Entrer un message de mise à jour (ex: Correction galerie, ajout figurines...) :"
read message
git commit -m "$message"

# Étape 3 : Pousser vers la branche principale
git push -u origin main

echo "✅ Mise à jour terminée et envoyée sur GitHub !"
