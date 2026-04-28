import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

# Configuration de la page
st.set_page_config(
    page_title="Santé Plus - Collecte de Données",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .section-header {
        color: #1f77b4;
        font-size: 20px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialisation de la session
if 'data_list' not in st.session_state:
    st.session_state.data_list = []
if 'file_path' not in st.session_state:
    st.session_state.file_path = 'patient_data.json'

# En-tête principal
st.markdown("<h1 class='main-header'>🏥 SANTÉ PLUS - Application de Collecte de Données Médicales</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Une plateforme sécurisée pour la collecte et l'analyse des données de santé</p>", unsafe_allow_html=True)

# Barre latérale - Navigation
st.sidebar.markdown("## 📋 Navigation")
page = st.sidebar.radio("Sélectionnez une page:", 
    ["📝 Collecte des Données", "📊 Analyse Descriptive", "✏️ Modifier une Entrée"])

# ==================== PAGE 1: COLLECTE DES DONNÉES ====================
if page == "📝 Collecte des Données":
    st.markdown("<h2 class='section-header'>Formulaire de Collecte de Données Médicales</h2>", unsafe_allow_html=True)
    
    with st.form("patient_form", clear_on_submit=True):
        # Section 1: Informations Personnelles
        st.markdown("### 👤 Informations Personnelles")
        col1, col2 = st.columns(2)
        
        with col1:
            nom_complet = st.text_input("Nom complet du patient", placeholder="Ex: Jean Dupont")
            age = st.number_input("Âge (années)", min_value=0, max_value=150, value=30)
        
        with col2:
            sexe = st.selectbox("Sexe", ["Masculin", "Féminin", "Autre"])
            date_naissance = st.date_input("Date de naissance", value=None)
        
        # Section 2: Constantes Vitales
        st.markdown("### 💓 Constantes Vitales")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tension_systolique = st.number_input("Tension artérielle (Systolique) - mmHg", min_value=0, max_value=300, value=120)
        
        with col2:
            tension_diastolique = st.number_input("Tension artérielle (Diastolique) - mmHg", min_value=0, max_value=200, value=80)
        
        with col3:
            frequence_cardiaque = st.number_input("Fréquence cardiaque - bpm", min_value=0, max_value=250, value=72)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            temperature = st.number_input("Température - °C", min_value=35.0, max_value=42.0, value=37.0, step=0.1)
        
        with col2:
            poids = st.number_input("Poids - kg", min_value=0.0, max_value=300.0, value=70.0, step=0.1)
        
        with col3:
            taille = st.number_input("Taille - cm", min_value=0, max_value=250, value=170)
        
        # Calcul de l'IMC
        if taille > 0:
            imc = poids / ((taille / 100) ** 2)
            st.info(f"**IMC calculé: {imc:.2f}**")
        
        # Section 3: Antécédents Médicaux
        st.markdown("### 📋 Antécédents Médicaux")
        col1, col2 = st.columns(2)
        
        with col1:
            antecedents = st.multiselect(
                "Antécédents médicaux",
                ["Diabète", "Hypertension", "Asthme", "Allergie", "Maladie cardiaque", "Autre"]
            )
        
        with col2:
            medicaments = st.text_area("Médicaments actuels (un par ligne)", height=100)
        
        # Section 4: Symptômes et Plaintes
        st.markdown("### 🤒 Symptômes et Plaintes")
        symptomes = st.text_area("Décrivez les symptômes ou plaintes actuels", height=100)
        
        # Section 5: Habitudes de Vie
        st.markdown("### 🌿 Habitudes de Vie")
        col1, col2 = st.columns(2)
        
        with col1:
            tabagisme = st.selectbox("Statut tabagique", ["Non-fumeur", "Fumeur actuel", "Ancien fumeur"])
            alcool = st.selectbox("Consommation d'alcool", ["Aucune", "Modérée", "Fréquente"])
        
        with col2:
            activite_physique = st.selectbox("Activité physique", ["Sédentaire", "Légère", "Modérée", "Intense"])
            sommeil = st.number_input("Heures de sommeil par nuit", min_value=0, max_value=24, value=7)
        
        # Section 6: Observations Médicales
        st.markdown("### 📝 Observations Médicales")
        observations = st.text_area("Observations supplémentaires du médecin", height=100)
        
        # Date de consultation
        date_consultation = st.date_input("Date de consultation")
        
        # Bouton de soumission
        submitted = st.form_submit_button("✅ Enregistrer les Données", use_container_width=True)
        
        if submitted:
            if not nom_complet:
                st.error("❌ Veuillez entrer le nom du patient")
            else:
                # Créer un dictionnaire avec les données
                patient_data = {
                    "id": datetime.now().strftime("%Y%m%d%H%M%S"),
                    "date_enregistrement": datetime.now().isoformat(),
                    "nom_complet": nom_complet,
                    "age": age,
                    "sexe": sexe,
                    "date_naissance": str(date_naissance) if date_naissance else "",
                    "tension_systolique": tension_systolique,
                    "tension_diastolique": tension_diastolique,
                    "frequence_cardiaque": frequence_cardiaque,
                    "temperature": temperature,
                    "poids": poids,
                    "taille": taille,
                    "imc": round(poids / ((taille / 100) ** 2), 2) if taille > 0 else 0,
                    "antecedents": antecedents,
                    "medicaments": medicaments,
                    "symptomes": symptomes,
                    "tabagisme": tabagisme,
                    "alcool": alcool,
                    "activite_physique": activite_physique,
                    "sommeil": sommeil,
                    "observations": observations,
                    "date_consultation": str(date_consultation)
                }
                
                # Charger les données existantes
                if os.path.exists(st.session_state.file_path):
                    with open(st.session_state.file_path, 'r', encoding='utf-8') as f:
                        st.session_state.data_list = json.load(f)
                
                # Ajouter les nouvelles données
                st.session_state.data_list.append(patient_data)
                
                # Sauvegarder les données
                with open(st.session_state.file_path, 'w', encoding='utf-8') as f:
                    json.dump(st.session_state.data_list, f, ensure_ascii=False, indent=2)
                
                st.markdown("<div class='success-message'>✅ Données enregistrées avec succès!</div>", unsafe_allow_html=True)
                st.success(f"Patient: {nom_complet} | ID: {patient_data['id']}")

# ==================== PAGE 2: ANALYSE DESCRIPTIVE ====================
elif page == "📊 Analyse Descriptive":
    st.markdown("<h2 class='section-header'>Analyse Descriptive des Données</h2>", unsafe_allow_html=True)
    
    # Charger les données
    if os.path.exists(st.session_state.file_path):
        with open(st.session_state.file_path, 'r', encoding='utf-8') as f:
            data_list = json.load(f)
    else:
        data_list = []
    
    if len(data_list) == 0:
        st.warning("⚠️ Aucune donnée enregistrée pour le moment.")
    else:
        # Convertir en DataFrame
        df = pd.DataFrame(data_list)
        
        # Statistiques générales
        st.markdown("### 📈 Statistiques Générales")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Nombre de patients", len(df))
        with col2:
            st.metric("Âge moyen", f"{df['age'].mean():.1f} ans")
        with col3:
            st.metric("Poids moyen", f"{df['poids'].mean():.1f} kg")
        with col4:
            st.metric("IMC moyen", f"{df['imc'].mean():.2f}")
        
        # Statistiques détaillées
        st.markdown("### 📊 Statistiques Détaillées")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Constantes Vitales")
            stats_vitales = {
                "Tension Systolique (mmHg)": df['tension_systolique'].describe(),
                "Tension Diastolique (mmHg)": df['tension_diastolique'].describe(),
                "Fréquence Cardiaque (bpm)": df['frequence_cardiaque'].describe(),
                "Température (°C)": df['temperature'].describe()
            }
            for stat_name, stat_values in stats_vitales.items():
                st.write(f"**{stat_name}**")
                st.write(f"Moyenne: {stat_values['mean']:.2f} | Min: {stat_values['min']:.2f} | Max: {stat_values['max']:.2f}")
        
        with col2:
            st.subheader("Anthropométrie")
            st.write(f"**Poids (kg)**")
            st.write(f"Moyenne: {df['poids'].mean():.2f} | Min: {df['poids'].min():.2f} | Max: {df['poids'].max():.2f}")
            st.write(f"**Taille (cm)**")
            st.write(f"Moyenne: {df['taille'].mean():.2f} | Min: {df['taille'].min():.2f} | Max: {df['taille'].max():.2f}")
            st.write(f"**IMC**")
            st.write(f"Moyenne: {df['imc'].mean():.2f} | Min: {df['imc'].min():.2f} | Max: {df['imc'].max():.2f}")
        
        # Distribution par sexe
        st.markdown("### 👥 Distribution par Sexe")
        sexe_counts = df['sexe'].value_counts()
        st.bar_chart(sexe_counts)
        
        # Tableau complet des données
        st.markdown("### 📋 Tableau Complet des Données")
        st.dataframe(df, use_container_width=True)
        
        # Télécharger les données
        st.markdown("### 📥 Exporter les Données")
        csv = df.to_csv(index=False, encoding='utf-8')
        st.download_button(
            label="📥 Télécharger en CSV",
            data=csv,
            file_name=f"donnees_sante_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# ==================== PAGE 3: MODIFIER UNE ENTRÉE ====================
elif page == "✏️ Modifier une Entrée":
    st.markdown("<h2 class='section-header'>Modifier une Entrée Existante</h2>", unsafe_allow_html=True)
    
    # Charger les données
    if os.path.exists(st.session_state.file_path):
        with open(st.session_state.file_path, 'r', encoding='utf-8') as f:
            data_list = json.load(f)
    else:
        data_list = []
    
    if len(data_list) == 0:
        st.warning("⚠️ Aucune donnée enregistrée pour le moment.")
    else:
        # Sélectionner un patient
        patient_names = [f"{p['nom_complet']} (ID: {p['id']})" for p in data_list]
        selected_patient = st.selectbox("Sélectionnez un patient à modifier", patient_names)
        
        # Trouver l'index du patient sélectionné
        patient_index = patient_names.index(selected_patient)
        patient = data_list[patient_index]
        
        st.info(f"Modification du dossier de: **{patient['nom_complet']}**")
        
        with st.form("edit_form", clear_on_submit=True):
            # Afficher et permettre la modification des champs
            st.markdown("### Informations Personnelles")
            col1, col2 = st.columns(2)
            
            with col1:
                new_nom = st.text_input("Nom complet", value=patient['nom_complet'])
                new_age = st.number_input("Âge", min_value=0, max_value=150, value=patient['age'])
            
            with col2:
                new_sexe = st.selectbox("Sexe", ["Masculin", "Féminin", "Autre"], 
                                       index=["Masculin", "Féminin", "Autre"].index(patient['sexe']))
            
            st.markdown("### Constantes Vitales")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                new_tension_sys = st.number_input("Tension Systolique", value=patient['tension_systolique'])
            with col2:
                new_tension_dia = st.number_input("Tension Diastolique", value=patient['tension_diastolique'])
            with col3:
                new_fc = st.number_input("Fréquence Cardiaque", value=patient['frequence_cardiaque'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                new_temp = st.number_input("Température", value=patient['temperature'], step=0.1)
            with col2:
                new_poids = st.number_input("Poids", value=patient['poids'], step=0.1)
            with col3:
                new_taille = st.number_input("Taille", value=patient['taille'])
            
            st.markdown("### Autres Informations")
            new_symptomes = st.text_area("Symptômes", value=patient['symptomes'], height=100)
            new_observations = st.text_area("Observations", value=patient['observations'], height=100)
            
            submitted = st.form_submit_button("✅ Mettre à jour", use_container_width=True)
            
            if submitted:
                # Mettre à jour les données
                data_list[patient_index].update({
                    "nom_complet": new_nom,
                    "age": new_age,
                    "sexe": new_sexe,
                    "tension_systolique": new_tension_sys,
                    "tension_diastolique": new_tension_dia,
                    "frequence_cardiaque": new_fc,
                    "temperature": new_temp,
                    "poids": new_poids,
                    "taille": new_taille,
                    "imc": round(new_poids / ((new_taille / 100) ** 2), 2) if new_taille > 0 else 0,
                    "symptomes": new_symptomes,
                    "observations": new_observations
                })
                
                # Sauvegarder
                with open(st.session_state.file_path, 'w', encoding='utf-8') as f:
                    json.dump(data_list, f, ensure_ascii=False, indent=2)
                
                st.markdown("<div class='success-message'>✅ Données mises à jour avec succès!</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("**Version:** 1.0  \n**Dernière mise à jour:** 2026")
