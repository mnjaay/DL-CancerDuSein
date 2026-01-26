"""
Composant pour l'authentification
"""

import streamlit as st
import requests

def render_auth_sidebar(api_base_url):
    """
    Rendu de la sidebar d'authentification
    
    Args:
        api_base_url: URL de base de l'API
        
    Returns:
        bool: True si l'utilisateur est connecté
    """
    
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 1rem 0; margin-bottom: 1.5rem;">
                <h2 style="margin: 0; color: #0066CC;">🔐 Authentification</h2>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.token is None:
            # Tabs pour Login et Register
            auth_tab1, auth_tab2 = st.tabs(["🔓 Connexion", "📝 Inscription"])
            
            with auth_tab1:
                show_login_form(api_base_url)
            
            with auth_tab2:
                show_register_form(api_base_url)
            
            return False
        
        else:
            # Utilisateur connecté
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #10B981; margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 2rem; margin-right: 0.5rem;">👤</span>
                        <div>
                            <div style="font-weight: 600; color: #065F46; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 1px;">
                                Connecté
                            </div>
                            <div style="font-weight: 700; color: #064E3B; font-size: 1.1rem; margin-top: 0.25rem;">
                                {st.session_state.username}
                            </div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚪 Déconnexion", use_container_width=True, type="primary"):
                st.session_state.token = None
                st.session_state.username = None
                st.rerun()
            
            return True


def show_login_form(api_base_url):
    """Formulaire de connexion"""
    
    st.markdown("### Se connecter")
    
    login_email = st.text_input(
        "Email",
        key="login_email",
        placeholder="votre@email.com"
    )
    
    login_password = st.text_input(
        "Mot de passe",
        type="password",
        key="login_password",
        placeholder="••••••••"
    )
    
    if st.button("🔓 Connexion", use_container_width=True, type="primary"):
        if not login_email or not login_password:
            st.error("❌ Veuillez remplir tous les champs")
            return
        
        try:
            with st.spinner("Connexion en cours..."):
                response = requests.post(
                    f"{api_base_url}/api/auth/login",
                    json={"email": login_email, "password": login_password},
                    timeout=10
                )
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.token = data.get("access_token")
                st.session_state.username = login_email
                st.success("✅ Connecté avec succès!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Email ou mot de passe incorrect")
        
        except requests.exceptions.Timeout:
            st.error("⏱️ Délai d'attente dépassé. Veuillez réessayer.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Impossible de se connecter au serveur. Vérifiez que l'API est démarrée.")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")


def show_register_form(api_base_url):
    """Formulaire d'inscription"""
    
    st.markdown("### Créer un compte")
    
    reg_email = st.text_input(
        "Email",
        key="reg_email",
        placeholder="votre@email.com"
    )
    
    reg_password = st.text_input(
        "Mot de passe",
        type="password",
        key="reg_password",
        placeholder="••••••••",
        help="Minimum 8 caractères"
    )
    
    reg_password_confirm = st.text_input(
        "Confirmer le mot de passe",
        type="password",
        key="reg_password_confirm",
        placeholder="••••••••"
    )
    
    if st.button("📝 S'inscrire", use_container_width=True, type="primary"):
        # Validation
        if not reg_email or not reg_password or not reg_password_confirm:
            st.error("❌ Veuillez remplir tous les champs")
            return
        
        if reg_password != reg_password_confirm:
            st.error("❌ Les mots de passe ne correspondent pas")
            return
        
        if len(reg_password) < 8:
            st.warning("⚠️ Le mot de passe doit contenir au moins 8 caractères")
            return
        
        if "@" not in reg_email or "." not in reg_email:
            st.error("❌ Email invalide")
            return
        
        try:
            with st.spinner("Inscription en cours..."):
                response = requests.post(
                    f"{api_base_url}/api/auth/register",
                    json={"email": reg_email, "password": reg_password},
                    timeout=10
                )
            
            if response.status_code == 200:
                st.success("✅ Inscription réussie! Connectez-vous maintenant.")
                st.balloons()
            else:
                error_detail = response.json().get("detail", response.text)
                st.error(f"❌ Erreur: {error_detail}")
        
        except requests.exceptions.Timeout:
            st.error("⏱️ Délai d'attente dépassé. Veuillez réessayer.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Impossible de se connecter au serveur. Vérifiez que l'API est démarrée.")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")
