"""
Composants pour afficher les résultats de prédiction
"""

import streamlit as st
import plotly.graph_objects as go

def show_prediction_result(prediction, confidence, filename):
    """
    Afficher les résultats de prédiction avec design premium
    
    Args:
        prediction: "Positive" ou "Negative"
        confidence: Score de confiance (0-1)
        filename: Nom du fichier analysé
    """
    
    is_positive = prediction == "Positive"
    
    # Animated result card
    result_class = "result-positive" if is_positive else "result-negative"
    icon = "🚨" if is_positive else "✅"
    title = "POSITIF" if is_positive else "NÉGATIF"
    subtitle = "Cancer détecté" if is_positive else "Pas de cancer détecté"
    card_color = "#DC2626" if is_positive else "#059669"
    
    st.markdown(f"""
        <div class="{result_class}">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                <div style="flex: 1; min-width: 200px;">
                    <h2 style="margin: 0; display: flex; align-items: center; font-size: 2rem;">
                        <span style="font-size: 2.5rem; margin-right: 0.5rem;">{icon}</span>
                        <span>{title}</span>
                    </h2>
                    <p style="margin: 0.75rem 0 0 0; font-size: 1.2rem; color: #334155;">
                        {subtitle}
                    </p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 3rem; font-weight: 700; color: {card_color};">
                        {confidence*100:.1f}%
                    </div>
                    <div style="font-size: 0.875rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                        Confiance
                    </div>
                </div>
            </div>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 2px solid rgba(0,0,0,0.1);">
                <p style="margin: 0; color: #64748B; font-size: 0.9rem;">
                    📁 Fichier: <b>{filename}</b>
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Gauge chart
    st.markdown("### 📊 Score de Confiance Détaillé")
    fig = create_premium_gauge(confidence, is_positive)
    st.plotly_chart(fig, use_container_width=True, key=f"gauge_{filename}")
    
    # Recommendations
    show_recommendations(is_positive, confidence)


def create_premium_gauge(confidence, is_positive=False):
    """
    Créer un gauge chart premium et moderne
    
    Args:
        confidence: Score de confiance (0-1)
        is_positive: True si résultat positif
        
    Returns:
        Plotly figure
    """
    
    # Couleurs selon le résultat
    bar_color = "#DC2626" if is_positive else "#10B981"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': "Score de Confiance du Modèle",
            'font': {
                'size': 24,
                'family': 'Inter',
                'color': '#1E293B',
                'weight': 600
            }
        },
        number={
            'suffix': "%",
            'font': {
                'size': 56,
                'family': 'Inter',
                'weight': 700,
                'color': bar_color
            }
        },
        gauge={
            'axis': {
                'range': [None, 100],
                'tickwidth': 2,
                'tickcolor': "#CBD5E1",
                'tickfont': {'family': 'Inter', 'size': 14}
            },
            'bar': {
                'color': bar_color,
                'thickness': 0.75,
                'line': {'color': '#FFFFFF', 'width': 2}
            },
            'bgcolor': "#F8FAFC",
            'borderwidth': 3,
            'bordercolor': "#E2E8F0",
            'steps': [
                {'range': [0, 50], 'color': '#FEE2E2'},
                {'range': [50, 75], 'color': '#FEF3C7'},
                {'range': [75, 100], 'color': '#D1FAE5'}
            ],
            'threshold': {
                'line': {'color': "#DC2626", 'width': 5},
                'thickness': 0.85,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=80, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter'}
    )
    
    return fig


def show_recommendations(is_positive, confidence):
    """
    Afficher les recommandations médicales
    
    Args:
        is_positive: True si résultat positif
        confidence: Score de confiance (0-1)
    """
    
    if is_positive:
        st.markdown("""
            <div class="recommendation-box recommendation-positive">
                <h3 style="margin-top: 0; color: #991B1B; display: flex; align-items: center;">
                    <span style="font-size: 1.5rem; margin-right: 0.5rem;">⚠️</span>
                    Recommandations Importantes
                </h3>
                <ul style="color: #7F1D1D; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                    <li><b>Consultez immédiatement</b> un oncologue ou médecin spécialisé</li>
                    <li>Apportez cette analyse à votre rendez-vous médical</li>
                    <li>Des examens complémentaires (biopsie, IRM) seront probablement nécessaires</li>
                    <li>Un diagnostic précoce améliore significativement les chances de guérison</li>
                    <li>Ne paniquez pas : ce résultat nécessite confirmation par un professionnel</li>
                </ul>
                <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(255,255,255,0.5); border-radius: 8px;">
                    <p style="margin: 0; color: #7F1D1D; font-size: 0.9rem;">
                        ⚕️ <b>Note importante:</b> Ce système est un outil d'aide à la décision. 
                        Seul un médecin qualifié peut établir un diagnostic définitif.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="recommendation-box recommendation-negative">
                <h3 style="margin-top: 0; color: #065F46; display: flex; align-items: center;">
                    <span style="font-size: 1.5rem; margin-right: 0.5rem;">✅</span>
                    Recommandations de Suivi
                </h3>
                <ul style="color: #064E3B; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                    <li>Continuez vos <b>dépistages réguliers</b> selon les recommandations médicales</li>
                    <li>Maintenez un <b>mode de vie sain</b> (alimentation équilibrée, activité physique)</li>
                    <li>Consultez votre médecin pour <b>confirmation</b> et suivi personnalisé</li>
                    <li>Surveillance recommandée tous les <b>6 à 12 mois</b></li>
                    <li>Signalez tout changement ou symptôme inhabituel à votre médecin</li>
                </ul>
                <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(255,255,255,0.5); border-radius: 8px;">
                    <p style="margin: 0; color: #064E3B; font-size: 0.9rem;">
                        💚 <b>Bon résultat:</b> Cette analyse est rassurante, mais une consultation 
                        médicale reste recommandée pour validation et suivi approprié.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Confidence interpretation
    st.markdown("---")
    st.markdown("### 📈 Interprétation du Score de Confiance")
    
    if confidence >= 0.9:
        conf_level = "Très élevée"
        conf_color = "#059669"
        conf_desc = "Le modèle est très confiant dans cette prédiction."
    elif confidence >= 0.75:
        conf_level = "Élevée"
        conf_color = "#0EA5E9"
        conf_desc = "Le modèle a un bon niveau de confiance."
    elif confidence >= 0.6:
        conf_level = "Modérée"
        conf_color = "#F59E0B"
        conf_desc = "Le modèle a une confiance modérée. Une vérification supplémentaire est recommandée."
    else:
        conf_level = "Faible"
        conf_color = "#EF4444"
        conf_desc = "Le modèle est peu confiant. Des examens complémentaires sont fortement recommandés."
    
    st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid {conf_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 2rem; font-weight: 700; color: {conf_color};">
                    {confidence*100:.1f}%
                </div>
                <div>
                    <div style="font-weight: 600; color: #1E293B; font-size: 1.1rem;">
                        Confiance {conf_level}
                    </div>
                    <div style="color: #64748B; margin-top: 0.25rem;">
                        {conf_desc}
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def show_loading_animation(message="Analyse en cours..."):
    """
    Afficher une animation de chargement
    
    Args:
        message: Message à afficher pendant le chargement
    """
    
    st.markdown(f"""
        <div style="text-align: center; padding: 3rem 0;">
            <div class="spinner"></div>
            <p style="margin-top: 1.5rem; color: #64748B; font-size: 1.1rem; font-weight: 500;">
                {message}
            </p>
            <div style="margin-top: 1rem;">
                <div style="width: 200px; height: 4px; background: #E2E8F0; border-radius: 4px; margin: 0 auto; overflow: hidden;">
                    <div style="width: 100%; height: 100%; background: linear-gradient(90deg, #0066CC 0%, #00C896 100%); animation: progress 2s ease-in-out infinite;"></div>
                </div>
            </div>
        </div>
        
        <style>
            @keyframes progress {{
                0% {{ transform: translateX(-100%); }}
                100% {{ transform: translateX(100%); }}
            }}
        </style>
    """, unsafe_allow_html=True)
