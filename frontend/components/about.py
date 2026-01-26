"""
Composant pour la section À Propos
"""

import streamlit as st

def render_about_section():
    """
    Affiche les informations détaillées sur le projet
    """
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
                <li><b>Architecture:</b> Réseau de neurones convolutif</li>
                <li><b>Input:</b> Images 128x128 RGB</li>
                <li><b>Output:</b> Classification binaire (Positif/Négatif)</li>
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
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <h4 style="color: #0066CC; margin-top: 0;">📦 Version</h4>
                <p style="color: #64748B; margin: 0;">
                    <b>Application:</b> v2.0 (Premium)<br>
                    <b>Dernière mise à jour:</b> Janvier 2024
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <h4 style="color: #00C896; margin-top: 0;">📞 Contact</h4>
                <p style="color: #64748B; margin: 0;">
                    <b>Support:</b> support@example.com<br>
                    <b>GitHub:</b> mnjaay/DL-CancerDuSein
                </p>
            </div>
        """, unsafe_allow_html=True)
