# 🌐 Guide d'exposition du service via ngrok

## 📋 Vue d'ensemble

Ce projet inclut une configuration complète pour exposer l'application de détection du cancer du sein via **ngrok**, permettant d'accéder au service de n'importe où sur Internet.

## 🚀 Configuration rapide

### 1. Installer ngrok
```bash
brew install ngrok
```

### 2. Créer un compte ngrok
- Visitez [https://dashboard.ngrok.com/signup](https://dashboard.ngrok.com/signup)
- Confirmez votre email

### 3. Configurer le token d'authentification
```bash
# Récupérez votre token sur:
# https://dashboard.ngrok.com/get-started/your-authtoken

ngrok config add-authtoken YOUR_TOKEN_HERE
```

### 4. Utiliser le script d'exposition

#### Exposer le Frontend uniquement
```bash
./ngrok_expose.sh frontend
```

#### Exposer l'API Gateway uniquement
```bash
./ngrok_expose.sh api
```

#### Exposer les deux services
```bash
./ngrok_expose.sh both
```

## 📡 Manuel: Exposition directe

### Frontend Streamlit
```bash
ngrok http 8501
```

### API Gateway
```bash
ngrok http 8004
```

### Avec authentification HTTP
```bash
ngrok http 8501 --basic-auth="user:password"
```

### Avec domaine personnalisé (plan Pro)
```bash
ngrok http 8501 --domain=cancer-ai.ngrok.io
```

## 📊 Monitoring

Consultez l'interface de monitoring ngrok:
```
http://localhost:4040
```

## 🔒 Sécurité

### URLs publiques vs. localhost

| Type | URL | Accès |
|------|-----|-------|
| Local | `http://localhost:8501` | Seulement depuis votre machine |
| ngrok | `https://xxxxx.ngrok.io` | Accessible publiquement |

### Recommandations de sécurité

1. **Authentification HTTP** (gratuit)
```bash
ngrok http 8501 --basic-auth="user:password"
```

2. **Domaine ngrok gratuit** (change à chaque redémarrage)
```bash
ngrok http 8501
```

3. **Domaine personnalisé** (plan Pro)
```bash
ngrok http 8501 --domain=custom.ngrok.io
```

## 🐳 Option Docker: ngrok intégré

### Utiliser docker-compose avec ngrok
```bash
export NGROK_AUTHTOKEN=your_token
docker-compose -f docker-compose.ngrok.yml up
```

Les services seront alors accessibles via les URLs ngrok fournies.

## 💻 Workflows courants

### 1. Démonstration du système
```bash
# Terminal 1: Lancer les services
docker-compose up

# Terminal 2: Exposer le frontend
./ngrok_expose.sh frontend

# Partagez l'URL ngrok avec votre audience
```

### 2. Tests depuis un téléphone
```bash
# Lancer ngrok
./ngrok_expose.sh frontend

# Sur votre téléphone, accédez à l'URL ngrok
# Exemple: https://abc123-def456.ngrok.io
```

### 3. Intégration avec des webhooks
```bash
# Exposer l'API
./ngrok_expose.sh api

# Utiliser l'URL ngrok comme webhook destination
# Exemple: https://abc123-def456.ngrok.io/api/predictions
```

## 📈 Performance et limite

### Plan gratuit ngrok
- Limite: 1 URL/session
- Sessiond'une heure (peut être réinitialisée)
- URL aléatoires
- Limite de bande passante

### Plan Pro ngrok
- URLs personnalisées
- Sessions illimitées
- Domaines personnalisés
- Meilleure bande passante

## 🧪 Test d'exposition

Vérifier que tout fonctionne:

```bash
# Dans un autre terminal, testez l'URL
curl -I https://your-ngrok-url.ngrok.io

# Pour l'API
curl -I https://your-ngrok-url.ngrok.io/api/health
```

## ⚠️ Troubleshooting

### "authentication failed"
```bash
# Configurer le token
ngrok config add-authtoken YOUR_TOKEN
```

### "ERR_NGROK_121 address already in use"
```bash
# Changer le port
ngrok http 8501 -bind-tls=true
```

### Connexion lente
```bash
# Utiliser une région plus proche
ngrok http 8501 --region eu   # Europe
ngrok http 8501 --region ap   # Asie
ngrok http 8501 --region au   # Australie
```

### URL ngrok ne fonctionne pas
```bash
# Vérifier que les services Docker sont actifs
docker-compose ps

# Relancer les services
docker-compose restart
```

## 📚 Ressources

- [Documentation ngrok officielle](https://ngrok.com/docs)
- [Dashboard ngrok](https://dashboard.ngrok.com)
- [API ngrok](https://ngrok.com/docs/api)

## 🔗 Architecture après exposition

```
Internet
   ↓
ngrok.io (tunnel public)
   ↓
localhost:8501 (Frontend)
   ↓
localhost:8004 (API Gateway)
   ↓
Services internes (inference, auth, data, postgres)
```

---

**Note**: Les URLs ngrok gratuites changent à chaque session. Conservez votre token ngrok en sécurité!
