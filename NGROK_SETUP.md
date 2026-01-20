# 🌐 Exposition du Service via ngrok

## Configuration initiale

### 1. Créer un compte ngrok
- Allez sur [https://dashboard.ngrok.com/signup](https://dashboard.ngrok.com/signup)
- Créez un compte gratuit
- Confirmez votre email

### 2. Récupérer et installer votre authtoken
- Accédez à [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
- Copiez votre token d'authentification
- Exécutez la commande:
```bash
ngrok config add-authtoken YOUR_TOKEN_HERE
```

## Exposition du service

### Option 1: Frontend Streamlit uniquement
```bash
ngrok http 8501
```

### Option 2: API Gateway uniquement
```bash
ngrok http 8004
```

### Option 3: Utiliser le script avec plusieurs tunnels
```bash
# Dans un terminal, exposer le frontend:
ngrok http 8501 --domain=your-custom-domain.ngrok.io

# Dans un autre terminal, exposer l'API Gateway:
ngrok http 8004
```

## Exemple de sortie ngrok

Après avoir lancé `ngrok http 8501`, vous verrez:

```
Session Status                online
Account                       votrecompte@email.com
Version                       3.x.x
Region                        us (United States)
Forwarding                    https://xxxxx-xxxxx-xxxxx.ngrok.io -> http://localhost:8501
```

## Accéder au service

- **Frontend Streamlit**: `https://xxxxx-xxxxx-xxxxx.ngrok.io`
- **API Gateway**: Exposé sur un autre port

## Configuration avancée

### Authentification du tunnel ngrok
Pour sécuriser votre tunnel avec un mot de passe:

```bash
ngrok http 8501 --basic-auth="username:password"
```

### Domaine personnalisé (plan Pro)
```bash
ngrok http 8501 --domain=votre-domaine.ngrok.io
```

### Limiter les connexions par IP
```bash
ngrok http 8501 --allow-hosts="192.168.1.100"
```

## Troubleshooting

### Erreur: "authentication failed"
Solution: Vous devez configurer votre authtoken
```bash
ngrok config add-authtoken YOUR_TOKEN
```

### Port déjà utilisé
Vérifiez que les services Docker sont en cours d'exécution:
```bash
docker-compose ps
```

### Slow performance
Utilisez une région ngrok plus proche:
```bash
ngrok http 8501 --region eu  # pour l'Europe
ngrok http 8501 --region ap  # pour l'Asie
```

## API ngrok (optionnel)

Voir les tunnels en cours:
```bash
# Via l'interface ngrok (disponible sur http://localhost:4040)
```

## Arrêter ngrok
```bash
# Dans le terminal:
Ctrl + C

# Ou via une autre session:
pkill -f ngrok
```

## Cas d'usage

1. **Démonstration du système**: Partagez l'URL ngrok avec d'autres
2. **Tests externes**: Accédez au service depuis votre téléphone
3. **Webhooks**: Recevez des webhooks de services externes
4. **Déploiement temporaire**: Sans avoir besoin d'un serveur public

---

**Note**: Les URLs ngrok gratuites changent à chaque redémarrage. Pour une URL stable, utilisez un plan Pro ngrok.
