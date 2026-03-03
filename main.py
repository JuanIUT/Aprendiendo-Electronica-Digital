import streamlit as st
import random
import time

st.set_page_config(page_title="Aprendiendo Electrónica Digital ⚡", page_icon="⚡")

# --- BANCO GRANDE DE PREGUNTAS (puedes agregar más aquí) ---
banco_preguntas = [

    {"p": "¿Cuántos bits tiene un nibble?", 
     "o": ["2 bits", "4 bits", "8 bits", "16 bits"], 
     "c": "4 bits"},

    {"p": "¿Cuántos bits tiene un byte?", 
     "o": ["4", "8", "16", "32"], 
     "c": "8"},

    {"p": "¿Cuál es la salida de una compuerta AND si ambas entradas son 1?", 
     "o": ["0", "1", "Depende del voltaje", "Indefinido"], 
     "c": "1"},

    {"p": "¿Qué compuerta invierte su entrada?", 
     "o": ["AND", "OR", "NOT", "XOR"], 
     "c": "NOT"},

    {"p": "¿Qué número decimal representa el binario 1101?", 
     "o": ["11", "12", "13", "14"], 
     "c": "13"},

    {"p": "¿Cuántos valores puede representar 4 bits?", 
     "o": ["8", "12", "16", "32"], 
     "c": "16"},

    {"p": "¿Qué compuerta es la negación de AND?", 
     "o": ["NOR", "NAND", "XOR", "NOT"], 
     "c": "NAND"},

    {"p": "¿Qué compuerta es la negación de OR?", 
     "o": ["NAND", "NOR", "XOR", "NOT"], 
     "c": "NOR"},

    {"p": "¿Cuál es el resultado de 1 AND 0?", 
     "o": ["0", "1", "Indefinido", "Depende"], 
     "c": "0"},

    {"p": "¿Cuál es el resultado de NOT 1?", 
     "o": ["0", "1", "Indefinido", "2"], 
     "c": "0"},

    # Puedes agregar 20 más aquí 👇
]

# --- FUNCIÓN PARA INICIAR EXAMEN NUEVO ---
def iniciar_examen():
    st.session_state.pool_preguntas = random.sample(banco_preguntas, 5)  # Toma 5 aleatorias
    st.session_state.indice = 0
    st.session_state.puntos = 0
    st.session_state.juego_terminado = False

# Inicialización
if 'pool_preguntas' not in st.session_state:
    iniciar_examen()

# --- INTERFAZ ---
st.title("⚡ Aprendiendo Electrónica Digital")
st.divider()

total_preguntas = len(st.session_state.pool_preguntas)

progreso = st.session_state.indice / total_preguntas
st.progress(progreso)

if not st.session_state.juego_terminado:

    pregunta_actual = st.session_state.pool_preguntas[st.session_state.indice]

    st.subheader(f"Pregunta {st.session_state.indice + 1} de {total_preguntas}")
    st.write(f"### {pregunta_actual['p']}")

    seleccion = st.radio("Selecciona una respuesta:", pregunta_actual['o'])

    if st.button("Confirmar respuesta"):
        if seleccion == pregunta_actual['c']:
            st.success("✅ Correcto")
            st.session_state.puntos += 1
        else:
            st.error(f"❌ Incorrecto. Respuesta correcta: {pregunta_actual['c']}")

        time.sleep(1)

        if st.session_state.indice < total_preguntas - 1:
            st.session_state.indice += 1
            st.rerun()
        else:
            st.session_state.juego_terminado = True
            st.rerun()

else:
    st.header("🏁 Fin del examen")
    st.metric("Puntuación Final", f"{st.session_state.puntos} / {total_preguntas}")

    if st.button("Reintentar examen"):
        iniciar_examen()  # 🔥 Aquí está la magia
        st.rerun()