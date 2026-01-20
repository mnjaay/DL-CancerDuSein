import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import io
import os
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
API_BASE_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")
st.set_page_config(
    page_title="🏥 Cancer Detection System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] button {
            font-size: 1.1rem;
            font-weight: bold;
        }
        .positive {
            background-color: #ffcccc;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #ff0000;
        }
        .negative {
            background-color: #ccffcc;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #00cc00;
        }
    </style>
""", unsafe_allow_html=True)

# Initialiser la session
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None

# Header
st.markdown("# 🏥 Cancer Detection AI System")
st.markdown("### Système de détection du cancer du sein par intelligence artificielle")

# Sidebar - Authentification
with st.sidebar:
    st.markdown("## 🔐 Authentification")
    
    if st.session_state.token is None:
        auth_tab1, auth_tab2 = st.tabs(["Login", "Register"])
        
        with auth_tab1:
            st.subheader("Se connecter")
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Mot de passe", type="password", key="login_password")
            
            if st.button("🔓 Connexion", use_container_width=True):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/api/auth/login",
                        json={"email": login_email, "password": login_password},
                        timeout=10
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.token = data.get("access_token")
                        st.session_state.username = login_email
                        st.success("✅ Connecté avec succès!")
                        st.rerun()
                    else:
                        st.error("❌ Email ou mot de passe incorrect")
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")
        
        with auth_tab2:
            st.subheader("Créer un compte")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Mot de passe", type="password", key="reg_password")
            reg_password_confirm = st.text_input("Confirmer mot de passe", type="password", key="reg_password_confirm")
            
            if st.button("📝 S'inscrire", use_container_width=True):
                if reg_password != reg_password_confirm:
                    st.error("❌ Les mots de passe ne correspondent pas")
                else:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/api/auth/register",
                            json={"email": reg_email, "password": reg_password},
                            timeout=10
                        )
                        if response.status_code == 200:
                            st.success("✅ Inscription réussie! Connectez-vous maintenant.")
                        else:
                            st.error(f"❌ Erreur: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")
    
    else:
        st.success(f"✅ Connecté: **{st.session_state.username}**")
        if st.button("🔓 Déconnexion", use_container_width=True):
            st.session_state.token = None
            st.session_state.username = None
            st.rerun()

# Contenu principal - uniquement si connecté
if st.session_state.token is None:
    st.warning("⚠️ Veuillez vous connecter pour accéder au système")
else:
    # Onglets principaux
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Prédiction",
        "📊 Statistiques",
        "📝 Historique",
        "ℹ️ À propos"
    ])
    
    # ============ TAB 1: PRÉDICTION ============
    with tab1:
        st.header("Prédiction Cancer")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📸 Upload Image")
            uploaded_file = st.file_uploader(
                "Choisir une image mammographique",
                type=["jpg", "jpeg", "png"],
                help="Format: JPG, JPEG ou PNG"
            )
            
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Image uploadée", use_container_width=True)
                
                if st.button("🚀 Analyser l'image", key="predict_btn", use_container_width=True):
                    with st.spinner("🔄 Analyse en cours..."):
                        try:
                            # Lire le contenu du fichier en bytes
                            uploaded_file.seek(0)
                            file_bytes = uploaded_file.read()
                            
                            # Envoyer les bytes directement
                            files = {"file": (uploaded_file.name, file_bytes, "image/jpeg")}
                            response = requests.post(
                                f"{API_BASE_URL}/api/workflow/predict-and-save",
                                files=files,
                                timeout=60
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                
                                # Enregistrer dans les logs au lieu d'afficher
                                logger.info(f"API Response: {result}")
                                
                                prediction = result.get("prediction", {}).get("prediction")
                                confidence = result.get("prediction", {}).get("confidence")
                                
                                if prediction is None or confidence is None:
                                    logger.error(f"Invalid API response: {result}")
                                    st.error(f"❌ Erreur: Réponse API invalide")
                                else:
                                    st.session_state.last_prediction = {
                                        "prediction": prediction,
                                        "confidence": confidence,
                                        "filename": uploaded_file.name
                                    }
                                    st.success("✅ Analyse terminée!")
                            else:
                                st.error(f"❌ Erreur: {response.text}")
                        except Exception as e:
                            st.error(f"❌ Erreur: {str(e)}")
        
        with col2:
            st.subheader("📋 Résultat")
            
            if "last_prediction" in st.session_state:
                pred = st.session_state.last_prediction
                prediction = pred["prediction"]
                confidence = pred["confidence"]
                
                # Affichage du résultat
                if prediction == "Positive":
                    st.markdown(f"""
                        <div class="positive">
                            <h3>🚨 POSITIF (Cancer détecté)</h3>
                            <p><b>Confiance:</b> {confidence*100:.1f}%</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="negative">
                            <h3>✅ NÉGATIF (Pas de cancer)</h3>
                            <p><b>Confiance:</b> {confidence*100:.1f}%</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=confidence * 100,
                    title="Confiance (%)",
                    domain={"x": [0, 1], "y": [0, 1]},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "darkblue"},
                        "steps": [
                            {"range": [0, 50], "color": "lightgray"},
                            {"range": [50, 100], "color": "gray"}
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 4},
                            "thickness": 0.75,
                            "value": 90
                        }
                    }
                ))
                fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig, use_container_width=True)
                
                st.info(f"📁 Fichier: **{pred['filename']}**")
            else:
                st.info("⏳ Uploadez une image et cliquez sur 'Analyser' pour voir le résultat")
    
    # ============ TAB 2: STATISTIQUES ============
    with tab2:
        st.header("📊 Statistiques Globales")
        
        try:
            stats_response = requests.get(
                f"{API_BASE_URL}/api/predictions/stats/summary",
                timeout=10
            )
            
            if stats_response.status_code == 200:
                stats = stats_response.json()
                
                # KPIs
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📊 Total Analyses", stats["total"])
                
                with col2:
                    st.metric("🚨 Positif", stats["positive"])
                
                with col3:
                    st.metric("✅ Négatif", stats["negative"])
                
                with col4:
                    st.metric("📈 % Positif", f"{stats['positive_percentage']:.1f}%")
                
                # Pie chart
                col_pie, col_bar = st.columns([1, 1])
                
                with col_pie:
                    fig_pie = go.Figure(data=[go.Pie(
                        labels=["Positif", "Négatif"],
                        values=[stats["positive"], stats["negative"]],
                        hole=0.3,
                        marker=dict(colors=["#ff6b6b", "#51cf66"])
                    )])
                    fig_pie.update_layout(title="Distribution des résultats")
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with col_bar:
                    fig_bar = go.Figure(data=[
                        go.Bar(
                            x=["Positif", "Négatif"],
                            y=[stats["positive"], stats["negative"]],
                            marker=dict(color=["#ff6b6b", "#51cf66"])
                        )
                    ])
                    fig_bar.update_layout(title="Nombre d'analyses par résultat")
                    st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.error("❌ Erreur lors de la récupération des statistiques")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")
    
    # ============ TAB 3: HISTORIQUE ============
    with tab3:
        st.header("📝 Historique des Prédictions")
        
        try:
            predictions_response = requests.get(
                f"{API_BASE_URL}/api/predictions?skip=0&limit=100",
                timeout=10
            )
            
            if predictions_response.status_code == 200:
                predictions = predictions_response.json()
                
                if predictions:
                    # Convertir en DataFrame
                    df = pd.DataFrame(predictions)
                    df["confidence"] = (df["confidence"] * 100).round(1)
                    df = df[["id", "prediction", "confidence", "filename", "created_at"]]
                    df.columns = ["ID", "Résultat", "Confiance (%)", "Fichier", "Date"]
                    
                    # Afficher le tableau
                    st.subheader("📋 Liste des analyses")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Filtrer par résultat
                    st.subheader("🔍 Filtrer")
                    result_filter = st.selectbox(
                        "Résultat",
                        ["Tous", "Positive", "Negative"],
                        key="result_filter"
                    )
                    
                    if result_filter != "Tous":
                        filtered_df = df[df["Résultat"] == result_filter]
                        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
                    
                    # Télécharger CSV
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Télécharger CSV",
                        csv,
                        "predictions.csv",
                        "text/csv"
                    )
                else:
                    st.info("⏳ Aucune prédiction trouvée")
            else:
                st.error("❌ Erreur lors de la récupération de l'historique")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")
    
    # ============ TAB 4: À PROPOS ============
    with tab4:
        st.header("ℹ️ À propos du système")
        
        st.markdown("""
        ## 🏥 Système de Détection du Cancer du Sein
        
        ### 📋 Description
        Ce système utilise l'intelligence artificielle (Deep Learning) pour analyser 
        les images mammographiques et détecter la présence de cancer du sein.
        
        ### 🔬 Technologie
        - **Modèle**: TensorFlow/Keras
        - **Architecture**: Réseau de neurones convolutif (CNN)
        - **Précision**: Entraîné sur des données publiques
        
        ### 🏗️ Architecture Système
        - **API Gateway**: Point d'entrée unique (FastAPI)
        - **Auth Service**: Gestion de l'authentification
        - **Inference Service**: Moteur de prédiction
        - **Data Service**: Stockage des résultats (PostgreSQL)
        - **Frontend**: Interface utilisateur (Streamlit)
        
        ### ⚠️ Avertissements
        - Ce système est à titre informatif uniquement
        - Ne remplace pas un diagnostic médical professionnel
        - Consultez toujours un médecin spécialiste
        
        ### 📊 Données Sauvegardées
        - ID de la prédiction
        - Résultat (Positif/Négatif)
        - Score de confiance
        - Nom du fichier
        - Timestamp
        
        ### 🔐 Sécurité
        - Authentification JWT
        - CORS activé
        - Données chiffrées en base de données
        
        ### 📞 Support
        Pour toute question ou problème, contactez l'équipe de développement.
        """)
        
        # API Status
        st.subheader("🔌 État des Services")
        
        services = {
            "API Gateway": f"{API_BASE_URL}/health",
            "Auth Service": f"{API_BASE_URL.replace('8004', '8000')}/health",
            "Inference Service": f"{API_BASE_URL.replace('8004', '8001')}/health",
            "Data Service": f"{API_BASE_URL.replace('8004', '8003')}/health"
        }
        
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        
        for (name, url), col in zip(services.items(), cols):
            with col:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        st.success(f"✅ {name}")
                    else:
                        st.error(f"❌ {name}")
                except:
                    st.error(f"❌ {name}")
