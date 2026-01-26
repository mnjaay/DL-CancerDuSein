"""
Fonctions utilitaires pour les appels API
"""

import requests
import streamlit as st
from typing import Optional, Dict, Any

def make_api_call(
    url: str,
    method: str = "GET",
    json_data: Optional[Dict] = None,
    files: Optional[Dict] = None,
    params: Optional[Dict] = None,
    timeout: int = 60
) -> tuple[bool, Any]:
    """
    Faire un appel API avec gestion d'erreur
    
    Args:
        url: URL de l'endpoint
        method: Méthode HTTP (GET, POST, PUT, DELETE)
        json_data: Données JSON pour POST/PUT
        files: Fichiers pour upload
        params: Paramètres de requête
        timeout: Timeout en secondes
        
    Returns:
        tuple: (success: bool, data: dict ou error_message: str)
    """
    
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=timeout)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files, timeout=timeout)
            else:
                response = requests.post(url, json=json_data, timeout=timeout)
        elif method == "PUT":
            response = requests.put(url, json=json_data, timeout=timeout)
        elif method == "DELETE":
            response = requests.delete(url, timeout=timeout)
        else:
            return False, f"Méthode HTTP non supportée: {method}"
        
        if response.status_code in [200, 201]:
            return True, response.json()
        else:
            error_detail = response.json().get("detail", response.text)
            return False, f"Erreur {response.status_code}: {error_detail}"
    
    except requests.exceptions.Timeout:
        return False, "Délai d'attente dépassé. Le serveur met trop de temps à répondre."
    
    except requests.exceptions.ConnectionError:
        return False, "Impossible de se connecter au serveur. Vérifiez que l'API est démarrée."
    
    except Exception as e:
        return False, f"Erreur inattendue: {str(e)}"


def predict_and_save(api_base_url: str, file_bytes: bytes, filename: str) -> tuple[bool, Any]:
    """
    Envoyer une image pour prédiction et sauvegarde
    
    Args:
        api_base_url: URL de base de l'API
        file_bytes: Bytes du fichier image
        filename: Nom du fichier
        
    Returns:
        tuple: (success, result_data ou error_message)
    """
    
    files = {"file": (filename, file_bytes, "image/jpeg")}
    url = f"{api_base_url}/api/workflow/predict-and-save"
    
    return make_api_call(url, method="POST", files=files)


def get_predictions(api_base_url: str, skip: int = 0, limit: int = 100) -> tuple[bool, Any]:
    """
    Récupérer l'historique des prédictions
    
    Args:
        api_base_url: URL de base de l'API
        skip: Nombre d'éléments à sauter
        limit: Nombre maximum de résultats
        
    Returns:
        tuple: (success, predictions ou error_message)
    """
    
    url = f"{api_base_url}/api/predictions"
    params = {"skip": skip, "limit": limit}
    
    return make_api_call(url, params=params)


def get_stats(api_base_url: str) -> tuple[bool, Any]:
    """
    Récupérer les statistiques globales
    
    Args:
        api_base_url: URL de base de l'API
        
    Returns:
        tuple: (success, stats ou error_message)
    """
    
    url = f"{api_base_url}/api/predictions/stats/summary"
    
    return make_api_call(url)


def delete_prediction(api_base_url: str, prediction_id: int) -> tuple[bool, Any]:
    """
    Supprimer une prédiction
    
    Args:
        api_base_url: URL de base de l'API
        prediction_id: ID de la prédiction à supprimer
        
    Returns:
        tuple: (success, response ou error_message)
    """
    
    url = f"{api_base_url}/api/predictions/{prediction_id}"
    
    return make_api_call(url, method="DELETE")
