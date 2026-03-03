import streamlit as st
import random
import time
import pandas as pd
import os

# ================= CONFIGURACIÓN =================

st.set_page_config(page_title="Aprendiendo Electrónica Digital ⚡", page_icon="⚡", layout="centered")

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #020024, #043d7a, #021b3a);
}

h1,h2,h3,p{
    color:#e6f7ff;
}

</style>
""", unsafe_allow_html=True)

# ================= RANKING SISTEMA =================

ARCHIVO_RANKING = "ranking_electronica.csv"

if not os.path.exists(ARCHIVO_RANKING):
    df = pd.DataFrame(columns=["Nombre", "Puntaje"])
    df.to_csv(ARCHIVO_RANKING, index=False)

def guardar_ranking(nombre, puntaje):

    df = pd.read_csv(ARCHIVO_RANKING)

    nueva_fila = pd.DataFrame([{
        "Nombre": nombre,
        "Puntaje": puntaje
    }])

    df = pd.concat([df, nueva_fila], ignore_index=True)
    df.to_csv(ARCHIVO_RANKING, index=False)

def asignar_medalla(pos):

    if pos == 0:
        return "🥇 Oro"
    elif pos == 1:
        return "🥈 Plata"
    elif pos == 2:
        return "🥉 Bronce"
    else:
        return "⭐ Participación"

# ================= BIENVENIDA =================

if "nombre_usuario" not in st.session_state:
    st.session_state.nombre_usuario = ""

def pantalla_bienvenida():

    st.title("🎯 BIENVENIDO A LA PRUEBA DE ELECTRONICA-DIGITAL")

    nombre = st.text_input("POR FAVOR INGRESE SU NOMBRE:")

    if st.button("Comenzar prueba"):

        if nombre.strip() == "":
            st.warning("Debe ingresar un nombre para continuar")
            return

        st.session_state.nombre_usuario = nombre
        st.session_state.start_time = time.time()
        st.rerun()

if st.session_state.nombre_usuario == "":
    pantalla_bienvenida()
    st.stop()

# ================= PREGUNTAS =================

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

# ================= ESTADO DEL JUEGO =================

if "indice" not in st.session_state:
    st.session_state.indice = 0
    st.session_state.puntos = 0
    st.session_state.juego_terminado = False
    st.session_state.start_time = time.time()

total_preguntas = len(st.session_state.pool_preguntas)

# ================= TIMER =================

TIEMPO_LIMITE = 10

def obtener_tiempo_restante():
    transcurrido = time.time() - st.session_state.start_time
    return max(0, TIEMPO_LIMITE - int(transcurrido))

def avanzar_pregunta(correcto=False):

    if correcto:
        st.session_state.puntos += 1

    st.session_state.indice += 1
    st.session_state.start_time = time.time()

    if st.session_state.indice >= total_preguntas:
        st.session_state.juego_terminado = True

    st.rerun()

# ================= INTERFAZ =================

st.title("⚡ Aprendiendo Electrónica Digital")
st.divider()

st.progress(st.session_state.indice / total_preguntas)

# ================= PANTALLA DEL JUEGO =================

if not st.session_state.juego_terminado:

    pregunta_actual = st.session_state.pool_preguntas[st.session_state.indice]

    tiempo = obtener_tiempo_restante()

    st.subheader(f"Pregunta {st.session_state.indice + 1} de {total_preguntas}")
    st.write(f"### {pregunta_actual['p']}")

    st.info(f"⏳ Tiempo restante: {tiempo} s")

    if tiempo <= 0:
        st.error("⏰ Tiempo agotado! Se cuenta como respuesta incorrecta.")
        time.sleep(1)
        avanzar_pregunta(False)

    seleccion = st.radio(
        "Selecciona una respuesta:",
        pregunta_actual["o"],
        key=f"radio_{st.session_state.indice}"
    )

    if st.button("Confirmar respuesta"):

        if seleccion == pregunta_actual["c"]:
            st.success("✅ ¡Correcto!")
            time.sleep(1)
            avanzar_pregunta(True)

        else:
            st.error(f"❌ Incorrecto. La respuesta correcta es: {pregunta_actual['c']}")
            time.sleep(1)
            avanzar_pregunta(False)

# ================= RESULTADOS =================

else:

    st.header("🏁 Fin del examen")

    puntos = st.session_state.puntos
    total = total_preguntas

    # Guardar ranking
    guardar_ranking(st.session_state.nombre_usuario, puntos)

    st.metric("Puntuación Final", f"{puntos} / {total}")

    st.success(f"👤 Nombre: {st.session_state.nombre_usuario}")
    st.success(f"📊 Puntaje obtenido: {puntos} / {total}")

    st.subheader("🏆 Ranking Histórico")

    ranking_df = pd.read_csv(ARCHIVO_RANKING)
    ranking_df = ranking_df.sort_values(by="Puntaje", ascending=False).reset_index(drop=True)

    ranking_df["Posición"] = ranking_df.index
    ranking_df["Medalla"] = ranking_df["Posición"].apply(asignar_medalla)

    st.dataframe(ranking_df[["Posición", "Nombre", "Puntaje", "Medalla"]])

    if st.button("Reintentar"):

        st.session_state.indice = 0
        st.session_state.puntos = 0
        st.session_state.juego_terminado = False

        random.shuffle(st.session_state.pool_preguntas)

        st.session_state.start_time = time.time()
        st.rerun()

