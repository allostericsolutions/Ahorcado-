import streamlit as st
import random
from PIL import Image
import requests
from io import BytesIO
import time

# ... (Definiciones de órganos y ecogenicidad como en el código original) ...

# Diccionario de imágenes de órganos (reemplaza con URLs reales)
organ_images = {
    "Diaphragm": "https://example.com/diaphragm.png",
    "Renal sinus": "https://example.com/renal_sinus.png",
    # ... agregar más imágenes ...
}

def mostrar_logo():
    """Muestra el logo de Allosteric Solutions."""
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        st.image(image, width=200, caption='Allosteric Solutions')
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading image: {e}")
    except Exception as e:
        st.error(f"Error processing image: {e}")

def generar_pregunta(used_combinations):
    """Genera una pregunta de ecogenicidad."""
    organ1, organ2 = get_unique_pair(used_combinations)

    # Elegir aleatoriamente entre "más ecogénico" o "menos ecogénico"
    pregunta_tipo = random.choice(["más", "menos"])
    if pregunta_tipo == "más":
        correct = organ1 if real_echogenicity[organ1] < real_echogenicity[organ2] else organ2
    else:
        correct = organ1 if real_echogenicity[organ1] > real_echogenicity[organ2] else organ2

    return organ1, organ2, correct, pregunta_tipo

def mostrar_pregunta(organ1, organ2, pregunta_tipo):
    """Muestra la pregunta del juego."""
    st.write(f"**Pregunta:** ¿Cuál órgano es **{pregunta_tipo}** ecogénico?")

    col1, col2 = st.columns(2)
    with col1:
        st.image(Image.open(BytesIO(requests.get(organ_images[organ1]).content)), caption=organ1)
    with col2:
        st.image(Image.open(BytesIO(requests.get(organ_images[organ2]).content)), caption=organ2)

def actualizar_estado(selected_organ, correct, score, combinations_made):
    """Actualiza el estado del juego."""
    if selected_organ == correct:
        score += 1
        st.success("¡Correcto!")
    else:
        score -= 1
        st.error(f"Incorrecto. {correct} es {('más' if real_echogenicity[correct] < real_echogenicity[selected_organ] else 'menos')} ecogénico.")

    combinations_made += 1
    return score, combinations_made

def main():
    st.title("Juego de Ecogenicidad")

    mostrar_logo()
    st.markdown('<a href="https://www.allostericsolutions.com/" target="_blank">Visit our website</a>', unsafe_allow_html=True)

    # Inicializar variables de estado de la sesión
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "combinations_made" not in st.session_state:
        st.session_state.combinations_made = 0
    if "used_combinations" not in st.session_state:
        st.session_state.used_combinations = set()

    max_combinations = 10
    
    # Barra de progreso
    progress_bar = st.progress(0)

    while st.session_state.combinations_made < max_combinations:
        organ1, organ2, correct, pregunta_tipo = generar_pregunta(st.session_state.used_combinations)
        mostrar_pregunta(organ1, organ2, pregunta_tipo)

        # Botones de respuesta con animación de resaltado
        col1, col2 = st.columns(2)
        with col1:
            if st.button(organ1, key=f"button_{organ1}", on_click=lambda: actualizar_estado(organ1, correct, st.session_state.score, st.session_state.combinations_made)):
                st.session_state.score, st.session_state.combinations_made = actualizar_estado(organ1, correct, st.session_state.score, st.session_state.combinations_made)
                time.sleep(1) # Pausa para la animación
                st.rerun()
        with col2:
            if st.button(organ2, key=f"button_{organ2}", on_click=lambda: actualizar_estado(organ2, correct, st.session_state.score, st.session_state.combinations_made)):
                st.session_state.score, st.session_state.combinations_made = actualizar_estado(organ2, correct, st.session_state.score, st.session_state.combinations_made)
                time.sleep(1) # Pausa para la animación
                st.rerun()

        # Actualizar la barra de progreso
        progress_bar.progress((st.session_state.combinations_made + 1) / max_combinations)

    st.write(f"Juego terminado! Tu puntuación final es: {st.session_state.score}")
    if st.button("Jugar de nuevo"):
        st.session_state.score = 0
        st.session_state.combinations_made = 0
        st.session_state.used_combinations.clear()
        st.rerun()

if __name__ == "__main__":
    main()
