import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard Depressão Estudantil", layout="wide")

# ---- DOCUMENTAÇÃO (mostrada na barra lateral) ----
st.sidebar.title("ℹ️ Sobre o Dashboard")
st.sidebar.info("""
**Objetivo:**  
Este dashboard visa explorar padrões relacionados à depressão entre estudantes, considerando fatores como gênero, sono, CGPA, estresse financeiro e pensamentos suicidas.

**Navegação:**  
Use o menu lateral *"Selecione a Página"* para alternar entre seções com diferentes visualizações.

**Filtros:**  
Você pode filtrar os dados por gênero. Isso afeta todos os gráficos mostrados nas páginas, permitindo comparações mais direcionadas.
""")

# ---- Carregar e preparar os dados ----
df = pd.read_csv("dataset_depressao_estudantes.csv")
df["depression_label"] = df["depression"].replace({0: "Não", 1: "Sim"})

# ---- Navegação e Filtros ----
pagina = st.sidebar.selectbox("Selecione a Página", [
    "Página 1: Depressão e Sono",
    "Página 2: CGPA e Estresse Financeiro",
    "Página 3: Pressão no Trabalho e Suicídio",
    "Página 4: Interativos",
    "Tabela de Dados"
])

st.sidebar.header("🎯 Filtros")
generos = st.sidebar.multiselect("Gênero", df["gender"].unique(), default=df["gender"].unique())
df = df[df["gender"].isin(generos)]

# ---- Página 1 ----
if pagina == "Página 1: Depressão e Sono":
    st.title("📊 Depressão por Gênero e Hábitos de Sono")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Depressão por Gênero")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x="gender", hue="depression_label", ax=ax)
        ax.set_xlabel("Gênero")
        ax.set_ylabel("Contagem")
        ax.legend(title="Depressão")
        st.pyplot(fig)

    with col2:
        st.subheader("Duração do Sono por Satisfação nos Estudos")
        fig, ax = plt.subplots()
        sns.boxplot(data=df, x="study_satisfaction", y="sleep_duration", ax=ax)
        ax.set_xlabel("Satisfação com os Estudos")
        ax.set_ylabel("Duração do Sono")
        st.pyplot(fig)

# ---- Página 2 ----
elif pagina == "Página 2: CGPA e Estresse Financeiro":
    st.title("📊 CGPA e Estresse Financeiro")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("CGPA vs Pressão Acadêmica")
        fig = px.scatter(
            df,
            x="academic_pressure",
            y="cgpa",
            color="depression_label",
            hover_data=["gender", "academic_pressure", "cgpa"],
            labels={"academic_pressure": "Pressão Acadêmica", "cgpa": "CGPA", "depression_label": "Depressão"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Estresse Financeiro por Depressão")
        fig, ax = plt.subplots()
        sns.violinplot(data=df, x="depression", y="financial_stress", ax=ax)
        ax.set_xlabel("Depressão")
        ax.set_ylabel("Estresse Financeiro")
        st.pyplot(fig)

# ---- Página 3 ----
elif pagina == "Página 3: Pressão no Trabalho e Suicídio":
    st.title("📊 Pressão no Trabalho e Pensamentos Suicidas")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pressão no Trabalho vs Depressão")
        fig, ax = plt.subplots()
        sns.boxplot(data=df, x="depression_label", y="work_pressure", ax=ax)
        ax.set_xlabel("Depressão")
        ax.set_ylabel("Pressão no Trabalho")
        st.pyplot(fig)

    with col2:
        st.subheader("Pensamentos Suicidas por Gênero")
        filtrar_depressao = st.checkbox("Mostrar apenas estudantes com depressão", key="suicidio")
        df_plot = df[df["depression"] == 1] if filtrar_depressao else df
        fig, ax = plt.subplots()
        sns.countplot(data=df_plot, x="gender", hue="suicidal_thoughts", ax=ax)
        ax.set_xlabel("Gênero")
        ax.set_ylabel("Contagem")
        ax.legend(title="Pensamentos Suicidas")
        st.pyplot(fig)

# ---- Página 4 ----
elif pagina == "Página 4: Interativos":
    st.title("📈 Gráficos Interativos com Plotly")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("CGPA vs Pressão Acadêmica (Interativo)")
        fig = px.scatter(
            df,
            x="academic_pressure",
            y="cgpa",
            color="depression_label",
            hover_data=["gender", "academic_pressure", "cgpa"],
            labels={"academic_pressure": "Pressão Acadêmica", "cgpa": "CGPA", "depression_label": "Depressão"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Distribuição da Pressão no Trabalho (Interativo)")
        fig = px.violin(
            df,
            x="depression_label",
            y="work_pressure",
            color="depression_label",
            box=True,
            points="all",
            hover_data=["gender", "work_pressure"],
            labels={"depression_label": "Depressão", "work_pressure": "Pressão no Trabalho"},
        )
        st.plotly_chart(fig, use_container_width=True)

# ---- Tabela ----
elif pagina == "Tabela de Dados":
    st.title("📋 Tabela de Dados Completos")
    st.dataframe(df)
