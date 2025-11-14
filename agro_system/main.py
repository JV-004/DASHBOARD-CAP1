
# Dashboard Principal - Sistema Integrado Agro
# main.py - Dashboard Principal Streamlit
import streamlit as st
import sys
import os

# Adiciona as pastas das fases ao path para importação
sys.path.append('phase1')
sys.path.append('phase4')
# Futuramente: sys.path.append('phase2'), etc.

# Importações das fases
try:
    from phase1 import adicionar_dados, listar_dados, calcular_manejo, executar_analise
    FASE1_PRONTA = True
except ImportError as e:
    st.error(f"Erro ao importar Fase 1: {e}")
    FASE1_PRONTA = False
   
# Importação da Fase 4 (sensores)
from phase4.sensores import ler_sensores_simulado   # <<--- ADICIONADO AQUI

# Configuração da página
st.set_page_config(
    page_title="Sistema Integrado Agro",
    page_icon="🌱",
    layout="wide"
)

# Título principal
st.title("🌱 Sistema Integrado de Gestão Agrícola")
st.markdown("Dashboard consolidando todas as fases do projeto")

# Sidebar para navegação entre fases
st.sidebar.title("Navegação")
fase_selecionada = st.sidebar.radio(
    "Selecione a Fase:",
    ["Fase 1 - Dados e Cálculos", "Fase 2 - Banco de Dados", "Fase 3 - IoT", 
    "Fase 5 - Cloud", "Fase 6 - Visão Computacional"]
)

# ==================== FASE 1 ====================
if fase_selecionada == "Fase 1 - Dados e Cálculos":
    st.header("📊 Fase 1 - Dados de Plantio e Cálculos")
    
    if not FASE1_PRONTA:
        st.error("Fase 1 não está disponível. Verifique a importação.")
    else:
        # Abas para organizar as funcionalidades da Fase 1
        tab1, tab2, tab3, tab4 = st.tabs(["Adicionar Dados", "Listar Dados", "Cálculo de Manejo", "Análise R"])

        with tab1:
            st.subheader("Adicionar Novo Plantio")
            
            cultura = st.selectbox("Cultura", ["Café", "Milho"], key="cultura_add")
            insumo = st.text_input("Insumo", placeholder="Ex: fosfato, ureia...", key="insumo_add")
            
            if cultura == "Café":
                col1, col2 = st.columns(2)
                with col1:
                    largura = st.number_input("Largura (m)", min_value=0.0, value=10.0, format="%.2f", key="largura_cafe")
                with col2:
                    comprimento = st.number_input("Comprimento (m)", min_value=0.0, value=20.0, format="%.2f", key="comprimento_cafe")
                raio = None
            else:  # Milho
                raio = st.number_input("Raio (m)", min_value=0.0, value=10.0, format="%.2f", key="raio_milho")
                largura = None
                comprimento = None

            if st.button("Adicionar Dados", key="btn_add"):
                if cultura and insumo and (largura is not None or raio is not None):
                    resultado, mensagem = adicionar_dados(
                        cultura, 
                        insumo, 
                        largura=largura, 
                        comprimento=comprimento, 
                        raio=raio
                    )
                    if resultado:
                        st.success(mensagem)
                        st.json(resultado)
                    else:
                        st.error(mensagem)
                else:
                    st.warning("Preencha todos os campos!")

        with tab2:
            st.subheader("Dados Cadastrados")
            dados = listar_dados()
            if dados:
                # Formata os dados para exibição
                dados_formatados = []
                for i, dado in enumerate(dados):
                    dados_formatados.append({
                        "ID": i,
                        "Cultura": dado["cultura"],
                        "Área (m²)": f"{dado['area']:.2f}",
                        "Insumo": dado["insumo"]
                    })
                st.table(dados_formatados)
            else:
                st.info("Nenhum dado cadastrado ainda.")

        with tab3:
            st.subheader("Cálculo de Manejo de Insumos")
            dados = listar_dados()
            if dados:
                # Seleciona o plantio para cálculo
                plantio_options = [f"{i} - {d['cultura']} (Área: {d['area']}m²)" for i, d in enumerate(dados)]
                selected_plantio = st.selectbox("Selecione o plantio:", plantio_options, key="select_plantio")
                indice = int(selected_plantio.split(" - ")[0])
                
                if st.button("Calcular Manejo", key="btn_manejo"):
                    resultado = calcular_manejo(indice)
                    if "erro" not in resultado:
                        st.success("**Resultado do Cálculo:**")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Cultura", resultado['cultura'])
                        with col2:
                            st.metric("Área", f"{resultado['area']:.2f} m²")
                        with col3:
                            st.metric("Insumo", resultado['insumo'])
                        
                        st.info(f"**Quantidade Necessária:** {resultado['quantidade_insumos']:.2f} {resultado['unidade']}")
                    else:
                        st.error(resultado["erro"])
            else:
                st.info("Adicione dados primeiro na aba 'Adicionar Dados'.")

        with tab4:
            st.subheader("Análise Estatística e Clima (R)")
            st.info("Esta análise calcula estatísticas dos dados e consulta a API meteorológica")
            
            if st.button("Executar Análise R", key="btn_r"):
                with st.spinner("Executando análise R..."):
                    resultado = executar_analise()
                
                st.subheader("Resultado da Análise:")
                st.text_area("", resultado, height=200, key="resultado_r")

# ==================== FASE 2 ====================
elif fase_selecionada == "Fase 2 - Banco de Dados":
    st.header("🗃️ Fase 2 - Banco de Dados")
    st.info("Funcionalidade em desenvolvimento...")
    # Futuramente: from phase2 import funcoes_fase2

# ==================== FASE 3 ====================
elif fase_selecionada == "Fase 3 - IoT":
    st.header("📡 Fase 3 - IoT e Sensores (Simulação da Fase 4)")

    # Coleta dos dados simulados
    dados = ler_sensores_simulado()

    st.subheader("📡 Leitura Atual dos Sensores")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Umidade (%)", f"{dados['umidade']}%")

    with col2:
        st.metric("pH do Solo", dados["pH"])

  with col3:
    st.metric("Bomba de Irrigação",
              "🌊 Ligada" if dados["bomba"] else "⛔ Desligada")


    st.subheader("💊 Nutrientes")
    col4, col5 = st.columns(2)

    with col4:
        st.metric("Fósforo Detectado?", "Sim" if dados["fosforo"] else "Não")

    with col5:
        st.metric("Potássio Detectado?", "Sim" if dados["potassio"] else "Não")

    st.markdown("### 📈 Detalhes Técnicos")
    st.json(dados)


# ==================== FASE 5 ====================
elif fase_selecionada == "Fase 5 - Cloud":
    st.header("☁️ Fase 5 - Cloud Computing")
    st.info("Funcionalidade em desenvolvimento...")
    # Futuramente: from phase5 import funcoes_fase5

# ==================== FASE 6 ====================
elif fase_selecionada == "Fase 6 - Visão Computacional":
    st.header("👁️ Fase 6 - Visão Computacional")
    st.info("Funcionalidade em desenvolvimento...")
    # Futuramente: from phase6 import funcoes_fase6

# Rodapé
st.markdown("---")
st.markdown("**Sistema Integrado Agro** - Fase 7 | Desenvolvido por [Nome do Time]")

# Status do sistema na sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Status do Sistema")
if FASE1_PRONTA:
    st.sidebar.success("✅ Fase 1 - Pronta")
else:
    st.sidebar.error("❌ Fase 1 - Com problemas")

st.sidebar.info("🟡 Fase 2 - Pendente")
st.sidebar.info("🟡 Fase 3 - Pendente")
st.sidebar.info("🟡 Fase 5 - Pendente")
st.sidebar.info("🟡 Fase 6 - Pendente")
