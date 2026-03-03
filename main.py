import streamlit as st
import random
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Aprendiendo Electrónica Digital ⚡", page_icon="⚡", layout="centered")

# --- FONDO AZUL MÁS OSCURO ---
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #010510, #020b2d, #010a1f);
}

/* patrón tecnológico */
.stApp::before {
    content:"";
    position: fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    opacity:0.05;
    background-image:
        radial-gradient(circle at 40px 40px, #00e5ff 2px, transparent 0);
    background-size: 120px 120px;
    pointer-events:none;
}

h1, h2, h3, p {
    color: #e6f7ff;
}

</style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS DE PREGUNTAS (20 preguntas) ---
if 'pool_preguntas' not in st.session_state:
    st.session_state.pool_preguntas = [
        {"p": "¿Cuántos bits tiene un nibble?",
         "o": ["2 bits", "4 bits", "8 bits", "16 bits"],
         "c": "4 bits"},
        {"p": "¿Cuántos bits tiene un byte?",
         "o": ["4", "8", "16", "32"],
         "c": "8"},
        {"p": "¿Cuál es la salida de una compuerta AND si ambas entradas son 1?",
         "o": ["0", "1", "Depende del voltaje", "Indefinido"],
         "c": "1"},
        {"p": "¿Cuál es la salida de una compuerta OR si una entrada es 1?",
         "o": ["0", "1", "Depende de la otra entrada", "Indefinido"],
         "c": "1"},
        {"p": "¿Qué compuerta lógica invierte su entrada?",
         "o": ["AND", "OR", "NOT", "XOR"],
         "c": "NOT"},
        # ... tus otras 15 preguntas permanecen iguales ...
    ]

    random.shuffle(st.session_state.pool_preguntas)

# --- ESTADO DEL JUEGO ---
if "indice" not in st.session_state:
    st.session_state.indice = 0
    st.session_state.puntos = 0
    st.session_state.juego_terminado = False
    st.session_state.start_time = time.time()

# --- INTERFAZ ---
st.title("⚡ Aprendiendo Electrónica Digital")
st.divider()

total_preguntas = len(st.session_state.pool_preguntas)

# Barra de progreso
st.progress(st.session_state.indice / total_preguntas)

# ================= TIMER AUTOMÁTICO (10 → 0) =================

TIEMPO_LIMITE = 10

def tiempo_restante():
    transcurrido = time.time() - st.session_state.start_time
    return max(0, int(TIEMPO_LIMITE - transcurrido))

def avanzar(correcto=False):
    if correcto:
        st.session_state.puntos += 1

    st.session_state.indice += 1
    st.session_state.start_time = time.time()

    if st.session_state.indice >= total_preguntas:
        st.session_state.juego_terminado = True

    st.rerun()

# ================= PANTALLA DEL JUEGO =================

if not st.session_state.juego_terminado:

    pregunta_actual = st.session_state.pool_preguntas[st.session_state.indice]

    # El contador comienza cuando aparece la pregunta
    t_rest = tiempo_restante()

    st.subheader(f"Pregunta {st.session_state.indice + 1} de {total_preguntas}")
    st.write(f"### {pregunta_actual['p']}")

    # Mostrar contador en tiempo real (10 → 0)
    st.markdown(
        f"<h2 style='text-align:center;'>⏳ {t_rest} s</h2>",
        unsafe_allow_html=True
    )

    # Si el tiempo termina automáticamente se marca incorrecto
    if t_rest <= 0:
        st.error("⏰ Tiempo agotado (respuesta incorrecta)")
        time.sleep(1)
        avanzar(correcto=False)

    opciones = pregunta_actual["o"]

    seleccion = st.radio(
        "Selecciona una respuesta:",
        opciones,
        key=f"radio_{st.session_state.indice}"
    )

    if st.button("Confirmar respuesta"):

        if seleccion == pregunta_actual["c"]:
            st.success("✅ ¡Correcto!")
            time.sleep(1)
            avanzar(correcto=True)
        else:
            st.error(f"❌ Incorrecto. La respuesta correcta es: {pregunta_actual['c']}")
            time.sleep(1)
            avanzar(correcto=False)

else:

    st.header("🏁 Fin del examen")

    puntos = st.session_state.puntos
    total = total_preguntas

    st.metric("Puntuación Final", f"{puntos} / {total}")

    porcentaje = (puntos / total) * 100

    if puntos >= 20:
        st.balloons()
        st.snow()
        st.success("🎉🔥🤩 Excelente! Máximo nivel dominado 🔥🎊🥳")
    elif puntos >= 18:
        st.balloons()
        st.success("🎈🚀🌟 ¡Casi perfecto! Muy buen desempeño 🌟🚀🎈")
    elif porcentaje >= 80:
        st.balloons()
        st.success("🌟 Excelente dominio de Electrónica Digital")
    elif porcentaje >= 60:
        st.info("👍 Buen trabajo, pero puedes mejorar")
    else:
        st.warning("📘 Debes repasar los conceptos básicos")

    if st.button("Reintentar"):
        st.session_state.indice = 0
        st.session_state.puntos = 0
        st.session_state.juego_terminado = False
        random.shuffle(st.session_state.pool_preguntas)
        st.session_state.start_time = time.time()
        st.rerun()
