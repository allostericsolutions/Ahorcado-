import streamlit as st
import random

# Ruta de la imagen en GitHub
image_url = "https://raw.githubusercontent.com/allostericsolutions/Ahorcado-/main/Allosteric%20-Solutions.png"

# Definición de los órganos y sus ecogenicidades
real_echogenicity = {
    "Diaphragm": 1,
    "Renal sinus": 2,
    "Pancreas": 3,
    "Spleen": 4,
    "Liver": 5,
    "Renal cortex": 6,
    "Renal medulla": 7,
    "Gallbladder": 8,
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

    # Mostrar el logo usando markdown y HTML
    st.markdown(
        f'<img src="{image_url}" width="300">',
        unsafe_allow_html=True
    )

    # Enlace a tu página web
    st.markdown('<a href="https://www.allostericsolutions.com/" target="_blank">Visit our website</a>', unsafe_allow_html=True)

    if "score" not in st.session_state:
        st.session_state.score = 0
    if "combinations_made" not in st.session_state:
        st.session_state.combinations_made = 0
    if "hangman_state" not in st.session_state:
        st.session_state.hangman_state = 0
    if "used_combinations" not in st.session_state:
        st.session_state.used_combinations = set()

    max_combinations = 10

    organ1, organ2 = get_unique_pair(st.session_state.used_combinations)

    if random.choice([True, False]):
        question = "Which is more echogenic?"
        correct = organ1 if real_echogenicity[organ1] < real_echogenicity[organ2] else organ2
    else:
        question = "Which is less echogenic?"
        correct = organ1 if real_echogenicity[organ1] > real_echogenicity[organ2] else organ2

    st.write(f"**Question:** {question}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(organ1):
            if organ1 == correct:
                st.session_state.score += 1
                st.session_state.hangman_state += 1
                st.success("Correct!")
            else:
                st.error("Incorrect.")
            st.session_state.combinations_made += 1
            st.experimental_rerun()

    with col2:
        if st.button(organ2):
            if organ2 == correct:
                st.session_state.score += 1
                st.session_state.hangman_state += 1
                st.success("Correct!")
            else:
                st.error("Incorrect.")
            st.session_state.combinations_made += 1
            st.experimental_rerun()

    # Mostrar el estado del juego (ahorcado simplificado)
    hangman_stages = [
        "________        ",
        "|      |        ",
        "|      O        ",
        "|     /|\\       ",
        "|     / \\       ",
        "|               ",
        "----           ",
    ]
    st.write("\n".join(hangman_stages[:st.session_state.hangman_state]))

    if st.session_state.hangman_state >= 7:
        st.write("¡You Win! 😄")
    elif st.session_state.combinations_made >= max_combinations:
        st.write(f"You Lose! 😔 Final Score: {st.session_state.score}")

    if st.button("Try Again"):
        st.session_state.score = 0
        st.session_state.combinations_made = 0
        st.session_state.hangman_state = 0
        st.session_state.used_combinations.clear()
        st.experimental_rerun()

if __name__ == "__main__":
    main()
