import streamlit as st
import pandas as pd

# ---------- Configuração da página e estilo responsivo ----------
st.set_page_config(
    page_title='Recomendação de Jogos',
    layout='wide',
    initial_sidebar_state='expanded'
)

# CSS customizado para responsividade e melhoria visual
st.markdown(
    """
    <style>
    /* Container principal com padding e fonte ajustada */
    .main .block-container {
        padding: 1rem;
        font-size: 1rem;
    }
    /* Cabeçalhos maiores em dispositivos menores */
    @media (max-width: 768px) {
        .main .block-container h1 {
            font-size: 1.8rem;
        }
        .main .block-container h2 {
            font-size: 1.4rem;
        }
        .stTable table {
            font-size: 0.9rem;
        }
    }
    /* Ajuste de margens para tabelas em modo wide */
    .stTable {
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Carrega dados das planilhas com encoding apropriado
@st.cache_data
def load_data():
    df_sistemas = pd.read_csv('csvs/sistemas.csv', sep=';', encoding='latin-1')
    df_generos = pd.read_csv('csvs/generos.csv', sep=';', encoding='latin-1')
    df_recomend = pd.read_csv('csvs/recomendação.csv', sep=';', encoding='latin-1')
    # Renomeia colunas principais
    df_sistemas.rename(columns={df_sistemas.columns[0]: 'Sistema'}, inplace=True)
    df_generos.rename(columns={df_generos.columns[0]: 'Genero'}, inplace=True)
    df_recomend.rename(columns={df_recomend.columns[0]: 'Genero'}, inplace=True)
    return df_sistemas, df_generos, df_recomend

# Carrega dataframes
df_sistemas, df_generos, df_recomend = load_data()

# ---------- Sidebar para seleção de filtros ----------
st.sidebar.header('Filtros de Seleção')

sistema = st.sidebar.selectbox('Sistema', df_sistemas['Sistema'].unique())
row_sis = df_sistemas[df_sistemas['Sistema'] == sistema].iloc[0]
aud_cols = ['Infantil', 'Todos', 'Adulto']
aud_opcoes = [c for c in aud_cols if row_sis[c] in ['++', '+++']]
aud = st.sidebar.selectbox('Público', aud_opcoes)

tipos = ['Acao','Aventura','RPG','Simulacao','Estrategia','Casual']
tipo_opcoes = [t for t in tipos if row_sis[t] in ['++','+++']]
tipo = st.sidebar.selectbox('Tipo de Jogo', tipo_opcoes)

gen_opcoes = df_generos[
    (df_generos[tipo].isin(['++','+++'])) & (df_generos[aud].isin(['++','+++']))
]['Genero'].tolist()
if not gen_opcoes:
    st.sidebar.error('Sem temas disponíveis.')
    st.stop()
tema = st.sidebar.selectbox('Tema Detalhado', gen_opcoes)

# ---------- Botão de ação ----------
botao = st.sidebar.button('Mostrar Configurações')

# ---------- Conteúdo principal ----------
st.title('Configurações de Stage')

if botao:
    rec = df_recomend[df_recomend['Genero'] == tipo]
    if rec.empty:
        st.warning('Não há recomendações para esta combinação.')
    else:
        rec = rec.iloc[0]
        # Layout em colunas responsivas
        c1, c2, c3 = st.columns((1,1,1))
        # Stage 1
        with c1:
            st.header('Stage 1')
            df_s1 = pd.DataFrame({
                'Configuração': ['Engine','Jogabilidade','História/Missões'],
                'Valor': [rec['Engine'], rec['Jogabilidade'], rec['História/Missões']]
            })
            st.dataframe(df_s1)
        # Stage 2
        with c2:
            st.header('Stage 2')
            df_s2 = pd.DataFrame({
                'Configuração': ['Diálogo','Design_de_Níveis','IA'],
                'Valor': [rec['Diálogo'], rec['Design_de_Níveis'], rec['IA']]
            })
            st.dataframe(df_s2)
        # Stage 3
        with c3:
            st.header('Stage 3')
            df_s3 = pd.DataFrame({
                'Configuração': ['Design_do_Mundo','Gráfico','Som'],
                'Valor': [rec['Design_do_Mundo'], rec['Gráfico'], rec['Som']]
            })
            st.dataframe(df_s3)

        # Sinergias extras abaixo das tabelas
        st.markdown('---')
        st.subheader('Sinergias do Tema Detalhado')
        gen_row = df_generos[df_generos['Genero'] == tema].iloc[0]
        st.write({f'Público ({aud})': gen_row[aud], f'Tipo ({tipo})': gen_row[tipo]})
        st.subheader('Visão Geral do Sistema')
        st.write(row_sis[aud_cols + tipos])
else:
    st.info('Use o painel lateral para selecionar filtros e clique em Mostrar Configurações')
