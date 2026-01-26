"""
Composants pour l'upload d'images
"""

import streamlit as st
from PIL import Image
import io

def render_upload_section():
    """
    Zone d'upload moderne avec preview d'image
    
    Returns:
        tuple: (uploaded_file, image) ou (None, None)
    """
    
    st.markdown("""
        <div style="margin: 2rem 0;">
            <h3 style="color: #1E293B; margin-bottom: 1rem;">📤 Upload d'Image</h3>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choisir une image mammographique",
        type=["jpg", "jpeg", "png"],
        help="Formats acceptés: JPG, JPEG, PNG (max 10MB)"
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        
        # Image preview
        st.image(image, caption=f"Image: {uploaded_file.name}", use_container_width=True)
        
        # Validation de l'image (invisible ou sous forme de success simple)
        file_size_mb = uploaded_file.size / (1024 * 1024)
        warnings = []
        
        if file_size_mb > 10:
            warnings.append("⚠️ Image très volumineuse (> 10MB)")
        
        if image.size[0] < 100 or image.size[1] < 100:
            warnings.append("⚠️ Résolution très basse")
        
        if image.mode not in ['RGB', 'L']:
            warnings.append("⚠️ Format de couleur inhabituel")
        
        if warnings:
            st.warning("\n\n".join(warnings))
        else:
            st.success("✅ Image prête pour analyse")
        
        return uploaded_file, image
    
    else:
        # Zone d'upload vide - afficher les instructions
        st.markdown("""
            <div class="upload-zone">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📤</div>
                <h3 style="color: #1E293B; margin: 0.5rem 0;">Glissez une image ici</h3>
                <p style="color: #64748B; margin-bottom: 1rem;">ou cliquez pour sélectionner un fichier</p>
                <span style="display: inline-block; background: #E0E7FF; color: #3730A3; padding: 0.5rem 1rem; border-radius: 8px; font-size: 0.875rem; font-weight: 500;">
                    JPG, JPEG, PNG • Max 10MB
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        return None, None


def create_image_comparison(image1, image2, label1="Image 1", label2="Image 2"):
    """
    Afficher deux images côte à côte pour comparaison
    
    Args:
        image1: Premier image PIL
        image2: Deuxième image PIL
        label1: Label de la première image
        label2: Label de la deuxième image
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{label1}**")
        st.image(image1, use_container_width=True)
    
    with col2:
        st.markdown(f"**{label2}**")
        st.image(image2, use_container_width=True)
