#!/bin/bash

# Script simple pour exposer le service via ngrok
# Usage: ./ngrok_expose.sh [frontend|api|both]

SERVICE=${1:-frontend}

echo "🚀 Exposition via ngrok"
echo "======================="
echo ""

# Vérifier si ngrok est installé
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok n'est pas installé"
    echo "Installez-le avec: brew install ngrok"
    exit 1
fi

# Vérifier l'authentification
if [ ! -f ~/.ngrok2/ngrok.yml ]; then
    echo "❌ ngrok n'est pas authentifié"
    echo ""
    echo "Pour configurer ngrok:"
    echo "1. Allez sur: https://dashboard.ngrok.com/signup"
    echo "2. Récupérez votre token: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "3. Configurez le token: ngrok config add-authtoken YOUR_TOKEN"
    exit 1
fi

echo "✅ ngrok authentifié"
echo ""

case $SERVICE in
    frontend)
        echo "📱 Exposition du Frontend Streamlit (port 8501)..."
        echo ""
        ngrok http 8501
        ;;
    api)
        echo "🔌 Exposition de l'API Gateway (port 8004)..."
        echo ""
        ngrok http 8004
        ;;
    both)
        echo "📱 Exposition du Frontend Streamlit (port 8501)..."
        ngrok http 8501 &
        FRONTEND_PID=$!
        
        sleep 2
        
        echo "🔌 Exposition de l'API Gateway (port 8004)..."
        ngrok http 8004 &
        API_PID=$!
        
        echo ""
        echo "✅ Les deux services sont exposés!"
        echo "📡 Accédez à http://localhost:4040 pour voir les tunnels"
        
        wait $FRONTEND_PID $API_PID
        ;;
    *)
        echo "❌ Usage: $0 [frontend|api|both]"
        exit 1
        ;;
esac
