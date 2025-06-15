import streamlit as st
import pandas as pd

# Carrega dados das planilhas com encoding apropriado
@st.cache_data
def load_data():
    df_sistemas = pd.read_csv('csvs/sistemas.csv', sep=';', encoding='latin-1')
    df_generos = pd.read_csv('csvs/generos.csv', sep=';', encoding='latin-1')
    df_recomend = pd.read_csv('csvs/recomendação.csv', sep=';', encoding='latin-1')
    # Renomeia colunas principais
    df_sistemas.rename(columns={df_sistemas.columns[0]: 'Sistema'}, inplace=True)
    df_generos.rename(columns={df_generos.columns[0]: 'Gênero'}, inplace=True)
    df_recomend.rename(columns={df_recomend.columns[0]: 'Gênero'}, inplace=True)
    return df_sistemas, df_generos, df_recomend

# Carrega dataframes
df_sistemas, df_generos, df_recomend = load_data()

st.title('App de Recomendação de Desenvolvimento de Jogos')
st.markdown('Selecione Sistema, Público, Tipo e Tema para obter configurações de Stage.')

# 1. Seleção de Sistema
sistema = st.selectbox('Sistema', df_sistemas['Sistema'].unique())
row_sis = df_sistemas[df_sistemas['Sistema'] == sistema].iloc[0]

# 2. Seleção de Público (I, T, A)
aud_cols = ['I', 'T', 'A']
aud_opcoes = [c for c in aud_cols if row_sis.get(c) in ['++', '+++']]
aud = st.selectbox('Público', aud_opcoes)

# 3. Seleção de Tipo de Jogo (broad genres)
tipos = ['Ação','Aventura','RPG','Simulação','Estratégia','Casual']
tipo_opcoes = [t for t in tipos if row_sis.get(t) in ['++','+++']]
tipo = st.selectbox('Tipo de Jogo', tipo_opcoes)

# 4. Seleção de Tema Detalhado
gen_opcoes = df_generos[
    df_generos[tipo].isin(['++','+++']) & df_generos[aud].isin(['++','+++'])
]['Gênero'].tolist()
if not gen_opcoes:
    st.error('Nenhum tema disponível para este Tipo e Público.')
    st.stop()
tema = st.selectbox('Tema Detalhado', gen_opcoes)

# 5. Botão para exibir configurações de Stage
if st.button('Mostrar Configurações de Stage'):
    # Usa o Tema Detalhado para buscar a linha correta
    rec_row = df_recomend[df_recomend['Gênero'] == tipo]
    if rec_row.empty:
        st.warning('Não há recomendações de Stage para este Tema.')
    else:
        rec = rec_row.iloc[0]
        st.subheader('Configurações de Stage')
        # Definição manual dos grupos de colunas por stage
        stage1_cols = df_recomend.columns[1:4]
        stage2_cols = df_recomend.columns[4:7]
        stage3_cols = df_recomend.columns[7:10]
         # Dados de Stage 1
        st.markdown('**Stage 1**')
        df_s1 = pd.DataFrame({
            'Configuração': stage1_cols,
            'Valor': [rec[col] for col in stage1_cols]
        })
        st.dataframe(df_s1)
        # Dados de Stage 2
        st.markdown('**Stage 2**')
        df_s2 = pd.DataFrame({
            'Configuração': stage2_cols,
            'Valor': [rec[col] for col in stage2_cols]
        })
        st.dataframe(df_s2)
        # Dados de Stage 3
        st.markdown('**Stage 3**')
        df_s3 = pd.DataFrame({
            'Configuração': stage3_cols,
            'Valor': [rec[col] for col in stage3_cols]
        })
        st.dataframe(df_s3)

# 6. Sinergias do Tema Detalhado Sinergias do Tema Detalhado
gen_row = df_generos[df_generos['Gênero'] == tema].iloc[0]
st.subheader('Sinergias do Tema Detalhado')
st.markdown(f"**Público ({aud})**: {gen_row[aud]}")
st.markdown(f"**Tipo ({tipo})**: {gen_row[tipo]}")

# 7. Visão Geral de Sinergias do Sistema
st.subheader('Visão Geral de Sinergias do Sistema')
st.write(row_sis[aud_cols + tipos])
