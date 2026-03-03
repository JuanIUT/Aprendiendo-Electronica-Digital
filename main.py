import streamlit as st
import random
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Aprendiendo Electrónica Digital ⚡", page_icon="⚡", layout="centered")

# --- ESTILO VISUAL TECNOLÓGICO ---
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #020024, #043d7a, #021b3a);
    background-size: cover;
}

/* Efecto de patrón tecnológico */
.stApp::before {
    content:"";
    position: fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    opacity:0.08;
    background-image:
        radial-gradient(circle at 25px 25px, #00e5ff 2px, transparent 0),
        radial-gradient(circle at 75px 75px, #00e5ff 2px, transparent 0);
    background-size: 100px 100px;
    pointer-events:none;
}

h1, h2, h3, p {
    color: #e6f7ff;
}

</style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS DE PREGUNTAS ---
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
        {"p": "¿Qué número decimal representa el binario 1101?",
         "o": ["11", "12", "13", "14"],
         "c": "13"},
        {"p": "¿Qué compuerta da salida 1 solo cuando las entradas son diferentes?",
         "o": ["AND", "OR", "XOR", "NAND"],
         "c": "XOR"},
        {"p": "¿Qué compuerta es la negación de AND?",
         "o": ["NOR", "NAND", "XOR", "NOT"],
         "c": "NAND"},
        {"p": "¿Qué compuerta es la negación de OR?",
         "o": ["NAND", "NOR", "XOR", "NOT"],
         "c": "NOR"},
        {"p": "En sistema binario solo existen los valores:",
         "o": ["0 y 1", "0,1,2", "1 y 2", "0 y 2"],
         "c": "0 y 1"},
        {"p": "Un flip-flop se utiliza principalmente para:",
         "o": ["Sumar", "Almacenar un bit", "Multiplicar", "Convertir señales"],
         "c": "Almacenar un bit"},
        {"p": "¿Qué dispositivo realiza operaciones aritméticas y lógicas?",
         "o": ["ALU", "RAM", "Fuente", "Display"],
         "c": "ALU"},
        {"p": "El código ASCII se utiliza para:",
         "o": ["Representar caracteres", "Medir voltaje", "Multiplicar binarios", "Diseñar circuitos"],
         "c": "Representar caracteres"},
        {"p": "¿Cuántos valores puede representar 3 bits?",
         "o": ["4", "6", "8", "16"],
         "c": "8"},
        {"p": "¿Cuál es el resultado de 1 AND 0?",
         "o": ["0", "1", "Indefinido", "Depende"],
         "c": "0"},
        {"p": "¿Cuál es el resultado de 1 OR 0?",
         "o": ["0", "1", "Indefinido", "Depende"],
         "c": "1"},
        {"p": "¿Cuál es el resultado de NOT 1?",
         "o": ["0", "1", "Indefinido", "2"],
         "c": "0"},
        {"p": "Un contador digital se utiliza para:",
         "o": ["Contar pulsos", "Sumar voltaje", "Medir resistencia", "Convertir corriente"],
         "c": "Contar pulsos"},
        {"p": "¿Qué sistema numérico utiliza base 16?",
         "o": ["Binario", "Decimal", "Hexadecimal", "Octal"],
         "c": "Hexadecimal"},
        {"p": "¿Cuántos valores puede representar 4 bits?",
         "o": ["8", "12", "16", "32"],
         "c": "16"},
    ]

    random.shuffle(st.session_state.pool_preguntas)

# --- ESTADO DEL JUEGO ---
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.puntos = 0
    st.session_state.juego_terminado = False
    st.session_state.start_time = time.time()

# --- INTERFAZ ---
st.title("⚡ Aprendiendo Electrónica Digital")
st.divider()

total_preguntas = len(st.session_state.pool_preguntas)

# Barra de progreso
progreso = st.session_state.indice / total_preguntas
st.progress(progreso)

# ================= TIMER LOGIC =================
TIEMPO_LIMITE = 10
# ================= TIMER QUE CORRE AUTOMÁTICAMENTE =================

def tiempo_restante():
    """Calcula el tiempo restante desde que inicia la pregunta"""
    transcurrido = time.time() - st.session_state.start_time
    return max(0, int(TIEMPO_LIMITE - transcurrido))

def verificar_tiempo_y_avanzar():
    """Si el tiempo se acaba, cuenta como incorrecto y pasa a la siguiente pregunta"""
    st.error("⏰ Tiempo agotado! Se cuenta como respuesta incorrecta.")
    time.sleep(1)
    avanzar_pregunta(correcto=False)

def avanzar_pregunta(correcto=False):
    """Avanza a la siguiente pregunta y reinicia timer"""
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

    # Verificar tiempo
    tiempo_restante = tiempo_restante()

# Si el tiempo termina automáticamente
if tiempo_restante <= 0:
    verificar_tiempo_y_avanzar()

    st.subheader(f"Pregunta {st.session_state.indice + 1} de {total_preguntas}")
    st.write(f"### {pregunta_actual['p']}")

    st.info(f"⏳ Tiempo restante: {tiempo_restante} s")

    opciones = pregunta_actual['o']
    seleccion = st.radio("Selecciona una respuesta:", opciones, key=f"radio_{st.session_state.indice}")

    if st.button("Confirmar respuesta"):

        if seleccion == pregunta_actual['c']:
            st.success("✅ ¡Correcto!")
            time.sleep(1)
            avanzar_pregunta(correcto=True)

        else:
            st.error(f"❌ Incorrecto. La respuesta correcta es: {pregunta_actual['c']}")
            time.sleep(1)
            avanzar_pregunta(correcto=False)

else:
    st.header("🏁 Fin del examen")

    puntos = st.session_state.puntos
    total = total_preguntas

    st.metric("Puntuación Final", f"{puntos} / {total}")

    porcentaje = (puntos / total) * 100

    # Celebraciones especiales
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


