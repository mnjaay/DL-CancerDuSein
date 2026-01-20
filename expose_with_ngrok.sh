#!/bin/bash

# Script pour exposer les services via ngrok
# Assurez-vous que ngrok est installé et authentifié

echo "🚀 Exposition des services via ngrok..."
echo ""

# Vérifier que les services sont en cours d'exécution
echo "📋 Vérification des services Docker..."
docker-compose ps

echo ""
echo "🌐 Exposition des services:"
echo ""

# Fonction pour exposer un service
expose_service() {
    local port=$1
    local name=$2
    local logfile="ngrok_${name}.log"
    echo "📡 Exposition de $name sur le port $port..."
    ngrok http "$port" --log stdout > "$logfile" 2>&1 &
}

# Exposer les services
expose_service 8501 "Frontend"
expose_service 8004 "API Gateway"

echo ""
echo "✅ Services exposés!"
echo ""
echo "⏳ Attente de 5 secondes pour que ngrok initialise..."
sleep 5

echo ""
echo "🔗 URLs publiques:"
echo "===================="

# Afficher les URLs
if [ -f "ngrok_Frontend.log" ]; then
    echo "📱 Frontend Streamlit:"
    grep "url=" "ngrok_Frontend.log" | tail -1
fi

if [ -f "ngrok_API Gateway.log" ]; then
    echo "🔌 API Gateway:"
    grep "url=" "ngrok_API Gateway.log" | tail -1
fi

echo ""
echo "✨ Les services sont maintenant accessibles publiquement!"
echo ""
echo "💡 Pour arrêter ngrok, utilisez: pkill -f ngrok"
echo "   Ou appuyez sur Ctrl+C pour arrêter le script"

# Garder le script actif
wait
