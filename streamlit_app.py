import streamlit as st
import openai

# Obtener claves desde secrets de Streamlit
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

# Configurar OpenAI
openai.api_key = OPENAI_API_KEY

# Título de la app
st.set_page_config(page_title="Asistente Personal", page_icon="🤖")
st.title("🧠 Asistente Personal")

# Inicializar sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar el historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada de usuario
if prompt := st.chat_input("Escribe tu pregunta..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Pensando..."):

        try:
            # Crear hilo
            thread = openai.beta.threads.create()
            openai.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=prompt
            )

            # Ejecutar el asistente
            run = openai.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=ASSISTANT_ID
            )

            # Obtener respuesta
            if run.status == "completed":
                messages = openai.beta.threads.messages.list(thread_id=thread.id)
                answer = messages.data[0].content[0].text.value
            else:
                answer = "⚠️ Lo siento, hubo un error al procesar la respuesta."

        except Exception as e:
            answer = f"❌ Error: {str(e)}"

        # Mostrar respuesta
        st.chat_message("assistant").markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
