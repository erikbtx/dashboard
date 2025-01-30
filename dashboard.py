import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração do Streamlit
st.set_page_config(page_title="Dashboard de Satisfação", layout="wide")

# Criar navegação entre páginas
menu = st.sidebar.radio("Navegação", ["Visão Geral", "Detalhamento"])

# Dados dos operadores e clientes
operadores_clientes = [
    ("Cintia", "Apas"), ("Cintia", "CMOC (Copebrás)"), ("Cintia", "KIMBERLY CLARK"),
    ("Cintia", "MSC"), ("Cintia", "Tetra Pak"), ("Cintia", "Weleda"), ("Cintia", "Zara"),
    ("Cintia", "ZARA INTERMITENTE 06-20"), ("Erick Massuco", "ZARA INTERMITENTE 21-05"),
    ("Erick Massuco", "ZUP"), ("Cintia", "Maersk"), ("Danielle", "SBT"), ("Danielle", "Serasa"),
    ("Danielle", "Mecalor"), ("Erick Massuco", "Mitsubishi"), ("Erick Massuco", "Panalpina (Air&Sea e Solutions)"),
    ("Erick Massuco", "Sompo"), ("Erick Massuco", "ZIM"), ("Erick Massuco", "Amway"), ("G.Paiva", "Banco Fibra"),
    ("G.Paiva", "Danone"), ("G.Paiva", "Edf"), ("Kauã", "Electrolux"), ("G.Paiva", "Ericsson EDB & EGS"),
    ("G.Paiva", "GlobalPack - [9 Unid]"), ("G.Paiva", "kohler"), ("Kauã", "Owens"), ("G.Paiva", "RecordTV"),
    ("G.Paiva", "RoadCard"), ("G.Paiva", "Sencinet"), ("Kauã", "Sephora"), ("G.Paiva", "Sifra"),
    ("G.Paiva", "Vopak"), ("G.Paiva", "João Fortes"), ("Kauã", "Carbon (Unicom)"), ("João", "Dafiti"),
    ("João", "Pamcary"), ("João", "SumUp"), ("João", "Torrent"), ("João", "Tuvsud"), ("João", "Visão Prev"),
    ("João", "Capemisa"), ("Kauã", "Canon (Toshiba)"), ("Luan", "Celistics"), ("Luan", "Cengage"),
    ("Kauã", "Cirion (Level 3)"), ("Luan", "FMU"), ("Luan", "Lopes"), ("Kauã", "AIG"),
    ("Luan", "Dr. Oetker"), ("Luan", "Linhas Uni"), ("Kauã", "Thermo Fisher"), ("Luan", "Zambon"),
    ("Kauã", "99 Tecnologia"), ("Ruan", "Alper"), ("Ruan", "Ascenty"), ("Ruan", "Cateno"),
    ("Ruan", "DuPont"), ("Ruan", "Informa Markets"), ("Ruan", "JC Hitachi"), ("Ruan", "Promedon"),
    ("Ruan", "Recovery"), ("Ruan", "Jockey Club"), ("Lucas Barros", "ClienteX")
]

# Criar DataFrame
df_operador_cliente = pd.DataFrame(operadores_clientes, columns=["Operador", "Cliente"])

# Gerar dados de avaliações e satisfação média dinamicamente
operadores_unicos = df_operador_cliente["Operador"].unique()
df_respostas = pd.DataFrame({
    "Operador": operadores_unicos,
    "Satisfação Média": [round(0.75 + (i % 3) * 0.1, 2) for i in range(len(operadores_unicos))],
    "Avaliações": [5 for _ in range(len(operadores_unicos))]
})

# Calcular métricas gerais
media_geral_satisfacao = df_respostas["Satisfação Média"].mean()
total_avaliacoes_realizadas = df_respostas["Avaliações"].sum()
percentual_uso_bpo = (df_operador_cliente["Cliente"].nunique() / len(df_operador_cliente)) * 100

# Criar DataFrame de feedbacks
df_feedback = df_operador_cliente.copy()
df_feedback["Feedback"] = df_feedback["Cliente"].apply(lambda x: "Ótimo atendimento" if "A" in x else "Pode melhorar")
df_feedback["Tipo Feedback"] = df_feedback["Feedback"].apply(lambda x: "Positivo" if "Ótimo" in x else "Negativo")

if menu == "Visão Geral":
    st.title("📊 Visão Geral da Equipe")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Clientes", df_operador_cliente["Cliente"].nunique())
    col2.metric("Total de Operadores", df_operador_cliente["Operador"].nunique())
    col3.metric("Média Geral de Satisfação", f"{media_geral_satisfacao:.3f}")
    col4.metric("Total de Avaliações", total_avaliacoes_realizadas)
    
    # Gráfico de Satisfação por Operador
    st.subheader("📌 Satisfação Média por Operador")
    fig = px.bar(df_respostas, x="Operador", y="Satisfação Média", color_discrete_sequence=["#1f77b4"], title="Satisfação Média por Operador")
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de Feedbacks Positivos e Negativos
    st.subheader("📌 Feedbacks Positivos e Negativos por Operador")
    feedback_contagem = df_feedback.groupby(["Operador", "Tipo Feedback"]).size().reset_index(name="Quantidade")
    fig_feedback = px.bar(feedback_contagem, x="Operador", y="Quantidade", color="Tipo Feedback", barmode="group", title="Feedbacks por Operador")
    st.plotly_chart(fig_feedback, use_container_width=True)
    
elif menu == "Detalhamento":
    st.title("📌 Detalhamento por Operador")
    operador_selecionado = st.selectbox("Selecione o Operador", df_operador_cliente["Operador"].unique())
    clientes_filtrados = df_operador_cliente[df_operador_cliente["Operador"] == operador_selecionado]["Cliente"].unique()
    cliente_selecionado = st.selectbox("Selecione o Cliente", clientes_filtrados)
    
    st.subheader(f"🎯 {operador_selecionado}")
    col1, col2 = st.columns([2, 3])
    satisfacao_media = df_respostas.set_index("Operador").get(operador_selecionado, {}).get("Satisfação Média", "N/A")
    avaliacoes = df_respostas.set_index("Operador").get(operador_selecionado, {}).get("Avaliações", "N/A")
    col1.metric("Satisfação Média", satisfacao_media)
    col1.metric("Total de Avaliações", avaliacoes)
    col1.metric("Total de Clientes Atendidos", len(clientes_filtrados))
    
    feedbacks = df_feedback[(df_feedback["Operador"] == operador_selecionado) & (df_feedback["Cliente"] == cliente_selecionado)]["Feedback"].tolist()
    col2.write("**Resumo dos Feedbacks:**")
    for feedback in feedbacks:
        col2.write(f"- {feedback}")

        import os
import pandas as pd
import streamlit as st

from io import BytesIO

def salvar_csv():
    caminho_pasta = "export_powerbi"
    os.makedirs(caminho_pasta, exist_ok=True)  # Criar a pasta se não existir

    # Criar arquivos CSV na memória para download
    arquivos = {
        "📥 Baixar Dados de Satisfação": df_respostas,
        "📥 Baixar Feedbacks": df_feedback,
        "📥 Baixar Operadores e Clientes": df_operador_cliente,
    }

    st.success("📊 Dados exportados com sucesso! Baixe os arquivos abaixo.")

    for nome, df in arquivos.items():
        output = BytesIO()
        df.to_csv(output, index=False, encoding="utf-8")
        output.seek(0)
        
        st.download_button(
            label=nome,
            data=output,
            file_name=f"{nome.split(' ')[1].lower()}.csv",
            mime="text/csv"
        )

# Criar botão para exportação
if st.button("📤 Exportar Dados para o Power BI"):
    salvar_csv()
