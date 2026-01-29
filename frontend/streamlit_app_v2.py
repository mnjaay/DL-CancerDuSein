"""
Cancer Detection System - Application Streamlit Premium
Version modernisée avec design system et composants réutilisables
"""

import streamlit as st
import pandas as pd
import os
import logging
from PIL import Image

# Import des composants custom
from config.theme import CUSTOM_CSS
from components.auth import render_auth_sidebar
from components.upload import render_upload_section
from components.prediction import show_prediction_result, show_loading_animation
from components.stats import show_stats_dashboard
from utils.api import predict_and_save, get_predictions, get_stats, delete_prediction

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration de la page
st.set_page_config(
    page_title="🏥 Cancer Detection System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration API
API_BASE_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")
if not API_BASE_URL.startswith("http://") and not API_BASE_URL.startswith("https://"):
    API_BASE_URL = f"http://{API_BASE_URL}"

# Appliquer le CSS custom
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialiser la session
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

# Header principal
st.markdown("""
    <div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem; background: linear-gradient(135deg, #0066CC 0%, #00C896 100%); border-radius: 16px; box-shadow: 0 8px 32px rgba(0,102,204,0.2);">
        <h1 style="margin: 0; color: white; font-size: 2.5rem; font-weight: 700;">
            🏥 Système d'IA de Détection du Cancer
        </h1>
        <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.9); font-size: 1.2rem;">
            Système de détection du cancer du sein par intelligence artificielle
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar - Authentification
is_authenticated = render_auth_sidebar(API_BASE_URL)

# Contenu principal
if not is_authenticated:
    # Page de bienvenue pour utilisateurs non connectés
    st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 4rem 2rem;">
            <div style="font-size: 5rem; margin-bottom: 1rem;">🔬</div>
            <h2 style="color: #1E293B; margin-bottom: 1rem;">Bienvenue sur Cancer Detection System</h2>
            <p style="color: #64748B; font-size: 1.1rem; max-width: 600px; margin: 0 auto 2rem auto; line-height: 1.6;">
                Système intelligent utilisant l'intelligence artificielle pour analyser
                les images mammographiques et détecter le cancer du sein.
            </p>
            <div style="background: #FEF3C7; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #F59E0B; max-width: 700px; margin: 0 auto;">
                <p style="margin: 0; color: #92400E;">
                    ⚠️ <b>Veuillez vous connecter</b> pour accéder au système de détection
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Fonctionnalités
    st.markdown("---")
    st.markdown("### ✨ Fonctionnalités")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="metric-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                <h3 style="color: #0066CC; margin-bottom: 0.5rem;">Analyse IA</h3>
                <p style="color: #64748B; margin: 0;">
                    Détection automatique avec réseaux de neurones convolutifs
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h3 style="color: #00C896; margin-bottom: 0.5rem;">Statistiques</h3>
                <p style="color: #64748B; margin: 0;">
                    Visualisations et métriques détaillées des analyses
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📝</div>
                <h3 style="color: #FF6B6B; margin-bottom: 0.5rem;">Historique</h3>
                <p style="color: #64748B; margin: 0;">
                    Suivi complet de toutes vos analyses passées
                </p>
            </div>
        """, unsafe_allow_html=True)

else:
    # Utilisateur connecté - Application complète
    
    # Onglets principaux
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Analyse",
        "📊 Statistiques",
        "📝 Historique",
        "ℹ️ À propos"
    ])
    
    # ============ TAB 1: ANALYSE ============
    with tab1:
        st.markdown("## 🔍 Analyse d'Image Mammographique")
        
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            # Section upload
            uploaded_file, image = render_upload_section()
            
            if uploaded_file and image:
                if st.button("🚀 Lancer l'Analyse", use_container_width=True, type="primary"):
                    # Analyse avec animation de chargement
                    with st.spinner(""):
                        show_loading_animation("Analyse de l'image en cours...")
                        
                        # Appel API
                        uploaded_file.seek(0)
                        file_bytes = uploaded_file.read()
                        
                        success, result = predict_and_save(
                            API_BASE_URL,
                            file_bytes,
                            uploaded_file.name
                        )
                        
                        if success:
                            # Extraire les données
                            prediction_data = result.get("prediction", {})
                            prediction = prediction_data.get("prediction")
                            confidence = prediction_data.get("confidence")
                            
                            if prediction and confidence is not None:
                                # Sauvegarder dans la session
                                st.session_state.last_prediction = {
                                    "prediction": prediction,
                                    "confidence": confidence,
                                    "filename": uploaded_file.name
                                }
                                st.success("✅ Analyse terminée avec succès!")
                                st.rerun()
                            else:
                                st.error("❌ Erreur: Réponse API invalide")
                        else:
                            st.error(f"❌ {result}")
        
        with col2:
            # Section résultats
            st.markdown("### 📋 Résultat de l'Analyse")
            
            if st.session_state.last_prediction:
                pred = st.session_state.last_prediction
                show_prediction_result(
                    pred["prediction"],
                    pred["confidence"],
                    pred["filename"]
                )
            else:
                st.markdown("""
                    <div class="glass-card" style="text-align: center; padding: 3rem 2rem;">
                        <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;">⏳</div>
                        <p style="color: #64748B; font-size: 1.1rem;">
                            Uploadez une image et cliquez sur "Lancer l'Analyse" pour voir les résultats
                        </p>
                    </div>
                """, unsafe_allow_html=True)
    
    # ============ TAB 2: STATISTIQUES ============
    with tab2:
        st.markdown("## 📊 Statistiques Globales")
        
        success, stats = get_stats(API_BASE_URL)
        
        if success:
            show_stats_dashboard(stats)
        else:
            st.error(f"❌ Impossible de charger les statistiques: {stats}")
    
    # ============ TAB 3: HISTORIQUE ============
    with tab3:
        st.markdown("## 📝 Historique des Analyses")
        
        success, predictions = get_predictions(API_BASE_URL, skip=0, limit=100)
        
        if success and predictions:
            # Convertir en DataFrame
            df = pd.DataFrame(predictions)
            df["confidence"] = (df["confidence"] * 100).round(1)
            df = df[["id", "prediction", "confidence", "filename", "created_at"]]
            df.columns = ["ID", "Résultat", "Confiance (%)", "Fichier", "Date"]
            
            # Filtres
            col_filter1, col_filter2 = st.columns(2)
            
            with col_filter1:
                result_filter = st.selectbox(
                    "Filtrer par résultat",
                    ["Tous", "Positive", "Negative"],
                    key="result_filter"
                )
            
            with col_filter2:
                sort_by = st.selectbox(
                    "Trier par",
                    ["Date (récent)", "Date (ancien)", "Confiance (haute)", "Confiance (basse)"],
                    key="sort_filter"
                )
            
            # Appliquer les filtres
            filtered_df = df.copy()
            
            if result_filter != "Tous":
                filtered_df = filtered_df[filtered_df["Résultat"] == result_filter]
            
            # Appliquer le tri
            if sort_by == "Date (récent)":
                filtered_df = filtered_df.sort_values("Date", ascending=False)
            elif sort_by == "Date (ancien)":
                filtered_df = filtered_df.sort_values("Date", ascending=True)
            elif sort_by == "Confiance (haute)":
                filtered_df = filtered_df.sort_values("Confiance (%)", ascending=False)
            elif sort_by == "Confiance (basse)":
                filtered_df = filtered_df.sort_values("Confiance (%)", ascending=True)
            
            # Afficher le tableau
            st.markdown(f"### 📋 {len(filtered_df)} analyse(s) trouvée(s)")
            
            # Styler le dataframe
            def style_prediction(val):
                if val == "Positive":
                    return 'background-color: #FEE2E2; color: #991B1B; font-weight: bold'
                elif val == "Negative":
                    return 'background-color: #D1FAE5; color: #065F46; font-weight: bold'
                return ''
            
            styled_df = filtered_df.style.applymap(
                style_prediction,
                subset=['Résultat']
            )
            
            st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            # Actions
            col_action1, col_action2 = st.columns(2)
            
            with col_action1:
                # Export CSV
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Télécharger CSV",
                    csv,
                    "predictions.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            with col_action2:
                # Rafraîchir
                if st.button("🔄 Actualiser", use_container_width=True):
                    st.rerun()
        
        elif success and not predictions:
            st.info("📭 Aucune analyse trouvée. Commencez par analyser une image!")
        else:
            st.error(f"❌ Impossible de charger l'historique: {predictions}")
    
    # ============ TAB 4: À PROPOS ============
    with tab4:
        st.markdown("## ℹ️ À propos du Système")
        
        st.markdown("""
            <div class="glass-card">
                <h3 style="color: #0066CC; margin-top: 0;">🏥 Système de Détection du Cancer du Sein</h3>
                
                <h4 style="color: #1E293B; margin-top: 2rem;">📋 Description</h4>
                <p style="color: #64748B; line-height: 1.8;">
                    Ce système utilise l'intelligence artificielle (Deep Learning) pour analyser
                    les images mammographiques et détecter la présence de cancer du sein. Le modèle
                    a été entraîné sur des données publiques et utilise un réseau de neurones convolutif (CNN).
                </p>
                
                <h4 style="color: #1E293B; margin-top: 2rem;">🔬 Technologie</h4>
                <ul style="color: #64748B; line-height: 1.8;">
                    <li><b>Modèle:</b> TensorFlow/Keras CNN</li>
                    <li><b>Architecture:</b> Réseau de neurones convolutif (DenseNet121)</li>
                    <li><b>Entrée:</b> Images 128x128 RGB</li>
                    <li><b>Sortie:</b> Classification binaire (Positif/Négatif)</li>
                </ul>
                
                <h4 style="color: #1E293B; margin-top: 2rem;">🏗️ Architecture Système</h4>
                <ul style="color: #64748B; line-height: 1.8;">
                    <li><b>API Gateway:</b> Point d'entrée unique (FastAPI)</li>
                    <li><b>Auth Service:</b> Gestion de l'authentification (JWT)</li>
                    <li><b>Inference Service:</b> Moteur de prédiction CNN</li>
                    <li><b>Data Service:</b> Stockage des résultats (PostgreSQL)</li>
                    <li><b>Frontend:</b> Interface utilisateur (Streamlit)</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Avertissement médical
        st.markdown("""
            <div style="background: #FEF2F2; border-left: 4px solid #DC2626; padding: 1.5rem; border-radius: 12px;">
                <h3 style="margin-top: 0; color: #991B1B; display: flex; align-items: center;">
                    <span style="font-size: 1.5rem; margin-right: 0.5rem;">⚠️</span>
                    Avertissement Médical Important
                </h3>
                <p style="color: #7F1D1D; margin: 0; line-height: 1.8;">
                    <b>Ce système est à titre informatif uniquement.</b> Il ne remplace en aucun cas
                    un diagnostic médical professionnel. Consultez toujours un médecin spécialiste
                    pour toute question relative à votre santé. Les résultats fournis par ce système
                    doivent être validés par un professionnel de la santé qualifié.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Version et contact
        col_v1, col_v2 = st.columns(2)
        
        with col_v1:
            st.markdown("""
                <div class="metric-card">
                    <h4 style="color: #0066CC; margin-top: 0;">📦 Version</h4>
                    <p style="color: #64748B; margin: 0;">
                        <b>Application:</b> v2.0 (Premium)<br>
                        <b>Dernière mise à jour:</b> Janvier 2026
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_v2:
            st.markdown("""
                <div class="metric-card">
                    <h4 style="color: #00C896; margin-top: 0;">📞 Contact</h4>
                    <p style="color: #64748B; margin: 0;">
                        <b>Support:</b> contact@cancer-detection.sn<br>
                        <b>GitHub:</b> github.com/organisation/DL-CancerDuSein
                    </p>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #64748B;">
       
        <p style="margin: 0.5rem 0 0 0; font-size: 0.875rem;">
            © 2026 Cancer Detection System. Tous droits réservés.
        </p>
    </div>
""", unsafe_allow_html=True)
