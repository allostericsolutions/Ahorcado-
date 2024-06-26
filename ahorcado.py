import streamlit as st
import random
from PIL import Image
import requests
from io import BytesIO

# URL de la imagen (asegúrate de que el bucket tenga acceso público)
image_url = "https://storage.googleapis.com/allostericsolutionsr/Allosteric_Solutions.png"

# Definición de los órganos y sus ecogenicidades (orden descendente)
real_echogenicity = {
    "Gallbladder": 8,
    "Renal medulla": 7,
    "Renal cortex": 6,
    "Liver": 5,
    "Spleen": 4,
    "Pancreas": 3,
    "Renal sinus": 2,
    "Diaphragm": 1,
}

echogenicity_list = list(real_echogenicity.keys())

def get_unique_pair(used_combinations):
    while True:
        organ1, organ2 = random.sample(echogenicity_list, 2)
        if (organ1, organ2) not in used_combinations and (organ2, organ1) not in used_combinations:
            used_combinations.add((organ1, organ2))
            return organ1, organ2

def main():
    st.title("Echogenicity Game")

    # Mostrar el logo usando st.image con ancho personalizado
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Check if the request was successful
        image = Image.open(BytesIO(response.content))
        st.image(image, width=200, caption='Allosteric Solutions')  # Ancho de 200 píxeles
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading image: {e}")
    except Exception as e:
        st.error(f"Error processing image: {e}")

    # Enlace a tu página web
    st.markdown('<a href="https://www.allostericsolutions.com/" target="_blank">Visit our website</a>', unsafe_allow_html=True)

    if "score" not in st.session_state:
        st.session_state.score = 0
    if "combinations_made" not in st.session_state:
        st.session_state.combinations_made = 0
    if "used_combinations" not in st.session_state:
        st.session_state.used_combinations = set()

    max_combinations = 10

    organ1, organ2 = get_unique_pair(st.session_state.used_combinations)

    if random.choice([True, False]):
        question = "Which is more echogenic?"
        correct = organ1 if real_echogenicity[organ1] > real_echogenicity[organ2] else organ2
    else:
        question = "Which is less echogenic?"
        correct = organ1 if real_echogenicity[organ1] < real_echogenicity[organ2] else organ2

    st.write(f"**Question:** {question}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(organ1):
            if organ1 == correct:
                st.session_state.score += 1
                st.success("Correct!")
            else:
                st.session_state.score -= 1
                st.error("Incorrect.")
            st.session_state.combinations_made += 1
            if st.session_state.combinations_made >= max_combinations:
                st.experimental_rerun()

    with col2:
        if st.button(organ2):
            if organ2 == correct:
                st.session_state.score += 1
                st.success("Correct!")
            else:
                st.session_state.score -= 1
                st.error("Incorrect.")
            st.session_state.combinations_made += 1
            if st.session_state.combinations_made >= max_combinations:
                st.experimental_rerun()

    # Mostrar el puntaje en un cuadro rojo, más grande y con el número más grande
    st.markdown(f'<div style="background-color: red; padding: 20px; font-size: 30px; text-align: center;">**Score:** {st.session_state.score}</div>', unsafe_allow_html=True)

    if st.session_state.combinations_made >= max_combinations:
        st.write(f"Game Over! 😔 Final Score: {st.session_state.score}")
        if st.button("Try Again"):
            st.session_state.score = 0
            st.session_state.combinations_made = 0
            st.session_state.used_combinations.clear()
            st.experimental_rerun()

if __name__ == "__main__":
    main()
