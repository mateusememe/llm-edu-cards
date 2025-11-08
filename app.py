"""
Educational Card Generation System with LLMs
(Bilingual Version)
"""

import streamlit as st
import time
import logging
from dotenv import load_dotenv
import os

# Import modules from our project
from config import MODELS, DEFAULT_TOPIC, TRANSLATIONS  # Import TRANSLATIONS
from llm_services import initialize_model, generate_summary, generate_subtopics
from utils import setup_logging, load_css

# --- Setup ---
load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="LLM Edu Card System",  # Title is set dynamically later
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)
load_css("style.css")

# --- Session State Initialization ---
if "history" not in st.session_state:
    st.session_state.history = []
if "api_token" not in st.session_state:
    st.session_state.api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
if "language" not in st.session_state:
    st.session_state.language = "pt"  # Default to Portuguese
# Default topic_input
if "topic_input" not in st.session_state:  ### ALTERADO ###
    st.session_state.topic_input = ""


# --- Helper Functions (UI Logic) ---


### NOVO: Função de Callback ###
def update_topic_input(new_topic):
    """
    Callback function to update the topic input field's session state.
    This runs *before* the widget is rendered, avoiding the API error.
    """
    logger.info(f"Setting topic input via callback: {new_topic}")
    st.session_state.topic_input = new_topic


### FIM NOVO ###


def setup_sidebar(lang, current_lang_code):
    """Configures and displays the Streamlit sidebar."""
    with st.sidebar:
        # Language Selector
        lang_map = {"EN 🇬🇧": "en", "PT 🇧🇷": "pt"}
        lang_options = list(lang_map.keys())
        current_index = (
            lang_options.index("PT 🇧🇷")
            if current_lang_code == "pt"
            else lang_options.index("EN 🇬🇧")
        )

        lang_choice = st.radio(
            lang["language_select_label"],
            lang_options,
            index=current_index,
            horizontal=True,
        )
        selected_lang_code = lang_map[lang_choice]

        # If language changed, update session state and rerun
        if selected_lang_code != current_lang_code:
            st.session_state.language = selected_lang_code
            logger.info(f"Language changed to: {selected_lang_code}")
            st.rerun()

        st.header(f"⚙️ {lang['settings_header']}")

        # API Token Input
        api_token = st.text_input(
            lang["api_token_label"],
            type="password",
            value=st.session_state.api_token,
            help=lang["api_token_help"],
        )
        if api_token:
            st.session_state.api_token = api_token

        # Model Selection
        selected_model_key = st.selectbox(
            lang["model_select_label"],
            options=list(MODELS.keys()),
            help=lang["model_select_help"],
        )
        # Get model description from translations
        if selected_model_key == "meta-llama/Meta-Llama-3-8B-Instruct":
            st.info(lang["model_desc_llama"])

        # Advanced Parameters
        with st.expander(f"🔧 {lang['advanced_params_header']}"):
            temperature = st.slider(
                lang["temperature_label"],
                0.0,
                1.0,
                MODELS[selected_model_key]["temperature"],
                0.1,
                help=lang["temperature_help"],
            )
            max_tokens = st.slider(
                lang["max_tokens_label"],
                100,
                2048,
                MODELS[selected_model_key]["max_tokens"],
                50,
                help=lang["max_tokens_help"],
            )

        # Project Info
        st.markdown("---")
        st.markdown(f"### 📚 {lang['project_about_header']}")
        st.markdown(
            f"""
            **{lang['project_about_course']}:** Aprendizado Profundo  
            **{lang['project_about_institution']}:** PPGCC - UNESP  
            **{lang['project_about_professor']}:** Dr. Denis Henrique Pinheiro Salvadeo
            """
        )

        # Clear History Button
        if st.button(f"🗑️ {lang['clear_history_button']}", use_container_width=True):
            st.session_state.history = []
            st.session_state.topic_input = ""  ### NOVO: Limpa o input também ###
            logger.info("History cleared by user.")
            st.rerun()

    return selected_model_key, temperature, max_tokens


def display_generated_cards(lang):
    """Displays the generated content cards from session state."""
    if st.session_state.history:
        st.markdown("---")
        st.markdown(f"## 📑 {lang['generated_cards_header']}")

        for idx, item in enumerate(st.session_state.history):
            with st.container():
                # Card Header
                col_header1, col_header2 = st.columns([3, 1])
                with col_header1:
                    st.markdown(f"### 🎯 {item['topic']}")
                with col_header2:
                    st.caption(f"🕐 {item['timestamp']} | 🤖 {item['model']}")

                # Summary Box
                st.markdown(
                    f"""
                    <div class="summary-box">
                        <h4>📝 {lang['summary_box_header']}</h4>
                        <p>{item['summary']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Subtopics
                st.markdown(f"#### 🔗 {lang['subtopics_header']}")
                cols = st.columns(3)
                for i, subtopic in enumerate(item["subtopics"]):
                    with cols[i % 3]:
                        st.markdown(
                            f"""
                            <div class="card">
                                <h5>{lang['subtopic_card_header']} {i+1}</h5>
                                <p>{subtopic}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        ### ALTERADO ###
                        # Button to explore subtopic
                        # Usamos on_click para chamar a função de callback
                        st.button(
                            f"🔍 {lang['explore_button']}",
                            key=f"explore_{idx}_{i}",
                            on_click=update_topic_input,  # Chama o callback
                            args=(subtopic,),  # Passa o subtema como argumento
                        )
                        ### FIM ALTERADO ###
                st.markdown("---")


def display_welcome_message(lang):
    """Shows a welcome message and examples if history is empty."""
    if not st.session_state.history:
        st.info(f"👆 {lang['welcome_message']}")
        st.markdown(f"### 💡 {lang['example_topics_header']}")
        col_ex1, col_ex2, col_ex3 = st.columns(3)

        # Load examples from the correct language
        for col, example in zip([col_ex1, col_ex2, col_ex3], lang["example_topics"]):
            with col:

                ### ALTERADO ###
                # Usamos on_click para chamar a função de callback
                st.button(
                    example,
                    use_container_width=True,
                    on_click=update_topic_input,  # Chama o callback
                    args=(example,),  # Passa o exemplo como argumento
                )
                ### FIM ALTERADO ###


def display_footer(lang):
    """Displays the application footer."""
    st.markdown("---")
    st.markdown(
        f"""
        <div style='text-align: center; color: #666;'>
            <p><strong>{lang['footer_title']}</strong></p>
            <p>Professor: Dr. Denis Henrique Pinheiro Salvadeo</p>
            <p>{lang['footer_devs']}: 
                <a href="https://github.com/ViniciusARZ" target="_blank">Vinicius Ramos</a>, 
                <a href="https://github.com/omiguelsma" target="_blank">Miguel Martins</a> & 
                <a href="https://github.com/mateusememe" target="_blank">Mateus Mendonça</a>
            </p>
            <p>{lang['footer_license']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def handle_generation(topic, model_name, temp, tokens, api_key, lang, lang_code):
    """Handles the logic for generating content."""
    if not api_key:
        st.error(f"⚠️ {lang['error_no_token']}")
        logger.warning("Generation attempt without API key.")
        return

    try:
        with st.spinner(f"🤖 {lang['spinner_message']} {model_name}..."):
            logger.info(f"Initializing model: {model_name}")
            llm = initialize_model(model_name, api_key, temp, tokens)

            # Generate content - PASS LANGUAGE CODE
            progress_bar = st.progress(0, text=f"{lang['spinner_message']}...")

            # Pass lang_code to service functions
            summary = generate_summary(llm, topic, lang_code)
            progress_bar.progress(50, text=f"{lang['spinner_message']}...")
            subtopics = generate_subtopics(llm, topic, lang_code)
            progress_bar.progress(100, text="Done!")
            time.sleep(1)
            progress_bar.empty()

            # Store in history
            st.session_state.history.insert(
                0,
                {
                    "topic": topic,
                    "summary": summary,
                    "subtopics": subtopics,
                    "model": model_name,
                    "timestamp": time.strftime("%H:%M:%S"),
                },
            )
            logger.info(f"Successfully generated cards for topic: {topic}")
            st.success(f"✅ {lang['success_message']} {model_name}!")

    except Exception as e:
        logger.error(
            f"Error during card generation for topic '{topic}': {str(e)}", exc_info=True
        )
        if "authorization" in str(e).lower() or "401" in str(e):
            st.error(f"❌ {lang['error_generation_failed']}")
        else:
            st.error(f"❌ {lang['error_generic']}: {str(e)}")
        st.info(lang["error_check_console"])


# --- Main Application ---
def main():
    """Main function to run the Streamlit app."""

    # Load the correct language dictionary
    lang_code = st.session_state.language
    lang = TRANSLATIONS[lang_code]

    # Set page title dynamically
    st.set_page_config(
        page_title=lang["app_title"],
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title(f"🎓 {lang['app_title']}")
    st.markdown(f"### {lang['app_subtitle']}")

    # Setup sidebar and get parameters
    model_name, temp, tokens = setup_sidebar(lang, lang_code)

    # Main area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"### 🔍 {lang['explore_topic_header']}")

        # O key="topic_input" irá ler automaticamente do st.session_state
        topic_input = st.text_input(
            lang["topic_input_label"],
            placeholder=lang["topic_input_placeholder"],
            help=lang["topic_input_help"],
            key="topic_input",  # Não mude isso!
        )

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            generate_btn = st.button(
                f"🚀 {lang['generate_button']}",
                type="primary",
                use_container_width=True,
            )

        with col_btn2:
            ### ALTERADO ###
            # Botão "Usar Exemplo" também usa o callback
            st.button(
                f"💡 {lang['example_button']}",
                use_container_width=True,
                on_click=update_topic_input,  # Chama o callback
                args=(DEFAULT_TOPIC,),  # Passa o tópico padrão
            )
            ### FIM ALTERADO ###

    with col2:
        st.markdown(f"### 📊 {lang['stats_header']}")
        st.metric(lang["stats_cards_generated"], len(st.session_state.history))
        st.metric(lang["stats_current_model"], model_name)

    # Handle generation logic
    # Usamos st.session_state.topic_input aqui, que é a "fonte da verdade"
    if generate_btn and st.session_state.topic_input:  ### ALTERADO ###
        logger.info(f"User requested generation for: {st.session_state.topic_input}")
        handle_generation(
            st.session_state.topic_input,
            model_name,
            temp,
            tokens,
            st.session_state.api_token,
            lang,
            lang_code,
        )

    # Display generated cards or welcome message
    if st.session_state.history:
        display_generated_cards(lang)
    else:
        display_welcome_message(lang)

    # Footer
    display_footer(lang)


if __name__ == "__main__":
    main()
