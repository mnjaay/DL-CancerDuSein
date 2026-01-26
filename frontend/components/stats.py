"""
Composants pour afficher les statistiques
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

def show_stats_dashboard(stats):
    """
    Afficher le dashboard de statistiques
    
    Args:
        stats: Dict contenant total, positive, negative, positive_percentage
    """
    
    # KPIs en haut
    st.markdown("### 📊 Vue d'ensemble")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        show_metric_card(
            "Total Analyses",
            stats["total"],
            "📊",
            "#0066CC"
        )
    
    with col2:
        show_metric_card(
            "Positif",
            stats["positive"],
            "🚨",
            "#EF4444"
        )
    
    with col3:
        show_metric_card(
            "Négatif",
            stats["negative"],
            "✅",
            "#10B981"
        )
    
    with col4:
        show_metric_card(
            "% Positif",
            f"{stats['positive_percentage']:.1f}%",
            "📈",
            "#F59E0B"
        )
    
    # Graphiques
    st.markdown("---")
    st.markdown("### 📈 Visualisations")
    
    col_pie, col_bar = st.columns(2)
    
    with col_pie:
        fig_pie = create_pie_chart(stats)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_bar:
        fig_bar = create_bar_chart(stats)
        st.plotly_chart(fig_bar, use_container_width=True)


def show_metric_card(label, value, icon, color):
    """
    Afficher une carte métrique
    
    Args:
        label: Label de la métrique
        value: Valeur à afficher
        icon: Emoji icon
        color: Couleur de la carte
    """
    
    st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-size: 2rem;">{icon}</span>
                <span style="font-size: 0.875rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                    {label}
                </span>
            </div>
            <div style="font-size: 2.5rem; font-weight: 700; color: {color}; text-align: center; margin: 1rem 0;">
                {value}
            </div>
        </div>
    """, unsafe_allow_html=True)


def create_pie_chart(stats):
    """
    Créer un pie chart moderne
    
    Args:
        stats: Dict avec positive et negative
        
    Returns:
        Plotly figure
    """
    
    fig = go.Figure(data=[go.Pie(
        labels=["Positif", "Négatif"],
        values=[stats["positive"], stats["negative"]],
        hole=0.4,
        marker=dict(
            colors=["#FF6B6B", "#51CF66"],
            line=dict(color='#FFFFFF', width=3)
        ),
        textinfo='label+percent',
        textfont=dict(size=14, family='Inter', color='white'),
        hovertemplate='<b>%{label}</b><br>%{value} analyses<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': "Distribution des Résultats",
            'font': {'size': 20, 'family': 'Inter', 'color': '#1E293B', 'weight': 600},
            'x': 0.5,
            'xanchor': 'center'
        },
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter'},
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        )
    )
    
    # Add annotation in center
    fig.add_annotation(
        text=f"<b>{stats['total']}</b><br>Total",
        x=0.5, y=0.5,
        font=dict(size=18, family='Inter', color='#1E293B'),
        showarrow=False
    )
    
    return fig


def create_bar_chart(stats):
    """
    Créer un bar chart moderne
    
    Args:
        stats: Dict avec positive et negative
        
    Returns:
        Plotly figure
    """
    
    fig = go.Figure(data=[
        go.Bar(
            x=["Positif", "Négatif"],
            y=[stats["positive"], stats["negative"]],
            marker=dict(
                color=["#FF6B6B", "#51CF66"],
                line=dict(color='#FFFFFF', width=2)
            ),
            text=[stats["positive"], stats["negative"]],
            textposition='outside',
            textfont=dict(size=16, family='Inter', weight=700),
            hovertemplate='<b>%{x}</b><br>%{y} analyses<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': "Nombre d'Analyses par Résultat",
            'font': {'size': 20, 'family': 'Inter', 'color': '#1E293B', 'weight': 600},
            'x': 0.5,
            'xanchor': 'center'
        },
        height=400,
        margin=dict(l=20, r=20, t=60, b=60),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter'},
        xaxis=dict(
            title="",
            tickfont=dict(size=14, family='Inter'),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(
                text="Nombre d'analyses",
                font=dict(size=14, family='Inter', color='#64748B')
            ),
            tickfont=dict(size=12, family='Inter'),
            gridcolor='#E2E8F0',
            showgrid=True
        ),
        bargap=0.3
    )
    
    return fig


def create_trend_chart(data):
    """
    Créer un graphique de tendance temporelle
    
    Args:
        data: DataFrame avec colonnes 'date' et 'count'
        
    Returns:
        Plotly figure
    """
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['count'],
        mode='lines+markers',
        name='Analyses',
        line=dict(color='#0066CC', width=3),
        marker=dict(size=8, color='#0066CC', line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor='rgba(0, 102, 204, 0.1)',
        hovertemplate='<b>%{x}</b><br>%{y} analyses<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "Évolution des Analyses dans le Temps",
            'font': {'size': 20, 'family': 'Inter', 'color': '#1E293B', 'weight': 600},
            'x': 0.5,
            'xanchor': 'center'
        },
        height=400,
        margin=dict(l=20, r=20, t=60, b=60),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter'},
        xaxis=dict(
            title=dict(
                text="Date",
                font=dict(size=14, family='Inter', color='#64748B')
            ),
            tickfont=dict(size=12, family='Inter'),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(
                text="Nombre d'analyses",
                font=dict(size=14, family='Inter', color='#64748B')
            ),
            tickfont=dict(size=12, family='Inter'),
            gridcolor='#E2E8F0',
            showgrid=True
        )
    )
    
    return fig
