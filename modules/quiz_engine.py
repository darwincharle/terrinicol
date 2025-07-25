import random
import streamlit as st
from modules.data_manager import load_data

df = load_data()  # Para generar preguntas

def show_quiz(df):
    st.header("🧠 Cuestionario Interactivo")
    
    if df.empty:
        st.warning("Necesitas elementos filtrados para el cuestionario")
        return
    
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
        st.session_state.current_question = 0
        st.session_state.questions = generate_questions(df)
    
    question_data = st.session_state.questions[st.session_state.current_question]
    
    st.subheader(f"Pregunta {st.session_state.current_question + 1}")
    st.markdown(f"**{question_data['question']}**")
    
    user_answer = st.radio(
        "Selecciona tu respuesta:",
        question_data['options'],
        key=f"question_{st.session_state.current_question}"
    )
    
    if st.button("Enviar respuesta"):
        if user_answer == question_data['correct']:
            st.session_state.quiz_score += 1
            st.success("¡Correcto!")
        else:
            st.error(f"Incorrecto. La respuesta correcta es: {question_data['correct']}")
        
        st.session_state.current_question += 1
        if st.session_state.current_question >= len(st.session_state.questions):
            st.balloons()
            st.success(f"Cuestionario completado! Puntuación: {st.session_state.quiz_score}/{len(st.session_state.questions)}")
            if st.button("Reiniciar cuestionario"):
                st.session_state.pop('quiz_score')
                st.session_state.pop('current_question')
                st.session_state.pop('questions')
                st.experimental_rerun()
        else:
            st.experimental_rerun()

def generate_questions(df):
    questions = []
    for _, element in df.iterrows():
        # Pregunta sobre número atómico
        questions.append({
            "question": f"¿Cuál es el número atómico de {element['nombre']}?",
            "options": sorted([
                str(element['numero_atomico']),
                str(random.randint(1, 100)),
                str(random.randint(1, 100)),
                str(random.randint(1, 100))
            ], key=lambda x: random.random()),
            "correct": str(element['numero_atomico'])
        })
        
        # Pregunta sobre usos
        if element['usos']:
            questions.append({
                "question": f"¿Cuál NO es un uso de {element['nombre']}?",
                "options": [
                    random.choice(element['usos']),
                    random.choice(df[df['nombre'] != element['nombre']]['usos'].iloc[0]),
                    "Fabricación de agua",
                    random.choice(element['usos'])
                ],
                "correct": "Fabricación de agua"
            })
    
    random.shuffle(questions)
    return questions[:10]  # Limitar a 10 preguntas