
# Dashboard Principal - Sistema Integrado Agro
import streamlit as st

st.title("Sistema Integrado de Gestão Agrícola")
st.write("Dashboard consolidando Fases 1-3, 5-6")

# Botões para acionar cada fase
if st.button("Fase 1 - API Meteorológica"):
    from phase1 import main as phase1_main
    phase1_main.run()

if st.button("Fase 2 - Banco de Dados"):
    from phase2 import main as phase2_main
    phase2_main.run()
    
# ... outros botões para as demais fases
