import streamlit as st
import time
import logging
from dotenv import load_dotenv
import os

from config import MODELS, DEFAULT_TOPIC, TRANSLATIONS
from llm_services import initialize_model, generate_summary, generate_subtopics
from utils import setup_logging, load_css
from database import CardDatabase

load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="LLM Edu Card System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)
load_css("style.css")

if "history" not in st.session_state:
    st.session_state.history = []
if "api_token" not in st.session_state:
    st.session_state.api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
if "language" not in st.session_state:
    st.session_state.language = "pt"
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""

if "db" not in st.session_state:
    st.session_state.db = CardDatabase()
    st.session_state.history = st.session_state.db.get_all_cards(limit=50)

if "show_modal" not in st.session_state:
    st.session_state.show_modal = False
if "selected_card" not in st.session_state:
    st.session_state.selected_card = None


def update_topic_input(new_topic):
    """
    Callback function to update the topic input field's session state.
    This runs *before* the widget is rendered, avoiding the API error.
    """
    logger.info(f"Setting topic input via callback: {new_topic}")
    st.session_state.topic_input = new_topic


def setup_sidebar(lang, current_lang_code):
    """Configures and displays the Streamlit sidebar."""
    with st.sidebar:
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

        if selected_lang_code != current_lang_code:
            st.session_state.language = selected_lang_code
            logger.info(f"Language changed to: {selected_lang_code}")
            st.rerun()

        st.header(f"⚙️ {lang['settings_header']}")

        api_token = st.text_input(
            lang["api_token_label"],
            type="password",
            value=st.session_state.api_token,
            help=lang["api_token_help"],
        )
        if api_token:
            st.session_state.api_token = api_token

        selected_model_key = st.selectbox(
            lang["model_select_label"],
            options=list(MODELS.keys()),
            help=lang["model_select_help"],
        )

        if selected_model_key == "meta-llama/Meta-Llama-3-8B-Instruct":
            st.info(lang["model_desc_llama"])

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

        with st.expander(f"📊 {lang["db_stats_expander"]}"):
            stats = st.session_state.db.get_statistics()

            col1, col2 = st.columns(2)
            with col1:
                st.metric(f"{lang["stats_total_metric"]}", stats["total_cards"])
                st.metric(f"{lang["stats_recent_cards"]}", stats["recent_cards"])

            with col2:
                if stats["by_language"]:
                    st.write(f"**{lang["stats_by_language"]}:**")
                    for language_code, count in stats[
                        "by_language"
                    ].items():
                        st.write(f"- {language_code.upper()}: {count}")

        st.divider()
        st.markdown(f"### 📚 {lang['project_about_header']}")
        st.markdown(
            f"""
            **{lang['project_about_course']}:** Aprendizado Profundo  
            **{lang['project_about_institution']}:** PPGCC - UNESP  
            **{lang['project_about_professor']}:** Dr. Denis Henrique Pinheiro Salvadeo
            """
        )

        if st.session_state.get("show_clear_confirm", False):
            st.warning("⚠️ Tem certeza que deseja excluir todo o histórico?")
            col_confirm1, col_confirm2 = st.columns(2)

            with col_confirm1:
                if st.button(
                    "✅ Sim, excluir tudo", key="confirm_yes", use_container_width=True
                ):
                    st.session_state.db.clear_all_cards()
                    st.session_state.history = []
                    st.session_state.show_clear_confirm = False
                    logger.info("History cleared by user (including database).")
                    st.success("Histórico limpo permanentemente!")
                    st.rerun()

            with col_confirm2:
                if st.button("❌ Cancelar", key="confirm_no", use_container_width=True):
                    st.session_state.show_clear_confirm = False
                    st.rerun()
        else:
            if "show_clear_confirm" not in st.session_state:
                st.session_state.show_clear_confirm = False

    return selected_model_key, temperature, max_tokens


def display_generated_cards(lang):
    """Displays the generated content cards in grid layout."""
    if st.session_state.history:
        st.divider()

        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            st.markdown(f"### 📑 {lang['generated_cards_header']}")
        with col_h2:
            stats = st.session_state.db.get_statistics()
            st.metric("Total de Cards", stats["total_cards"])

        search_query = st.text_input(
            f"🔍 {lang["topic_search_header"]}",
            placeholder=f"{lang['topic_search_input_placeholder']}",
            key="card_search",
            help=f"{lang['search_help']}",
        )

        if search_query:
            cards_to_show = st.session_state.db.search_cards(search_query)
            if not cards_to_show:
                st.info(f"Nenhum card encontrado para '{search_query}'")
                return
        else:
            cards_to_show = st.session_state.history

        st.markdown('<div class="card-grid">', unsafe_allow_html=True)

        num_cols = 3
        for i in range(0, len(cards_to_show), num_cols):
            cols = st.columns(num_cols)

            for j, col in enumerate(cols):
                card_idx = i + j
                if card_idx < len(cards_to_show):
                    card = cards_to_show[card_idx]

                    with col:
                        st.markdown(
                            f"""
                            <div class="card">
                                <div class="card-topic">{card['topic']}</div>
                                <div class="card-preview">
                                    {card['summary'][:80]}...
                                </div>
                                <div class="card-meta">
                                    <span>{card.get('timestamp', 'N/A')}</span>
                                    <span class="card-model">{card['model'].split('/')[-1]}</span>
                                </div>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )

                        if st.button(
                            "👁️ Ver Detalhes",
                            key=f"view_{card['id']}",
                            use_container_width=True,
                        ):
                            st.session_state.selected_card = card
                            st.session_state.show_modal = True
                            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.show_modal and st.session_state.selected_card:
        show_card_modal(st.session_state.selected_card, lang)


def display_welcome_message(lang):
    """Shows a welcome message and examples if history is empty."""
    if not st.session_state.history:
        st.info(f"👆 {lang['welcome_message']}")
        st.markdown(f"### 💡 {lang['example_topics_header']}")
        col_ex1, col_ex2, col_ex3 = st.columns(3)

        for col, example in zip([col_ex1, col_ex2, col_ex3], lang["example_topics"]):
            with col:
                st.button(
                    example,
                    use_container_width=True,
                    on_click=update_topic_input,
                    args=(example,),
                )

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

            progress_bar = st.progress(0, text=f"{lang['spinner_message']}...")

            summary = generate_summary(llm, topic, lang_code)
            progress_bar.progress(50, text=f"{lang['spinner_message']}...")
            subtopics = generate_subtopics(llm, topic, lang_code)
            progress_bar.progress(100, text="Done!")
            time.sleep(1)
            progress_bar.empty()

            card_id = st.session_state.db.save_card(
                topic=topic,
                summary=summary,
                subtopics=subtopics,
                model=model_name,
                language=lang_code,
                temperature=temp,
                max_tokens=tokens,
            )

            card_data = {
                "id": card_id,
                "topic": topic,
                "summary": summary,
                "subtopics": subtopics,
                "model": model_name,
                "language": lang_code,
                "timestamp": time.strftime("%H:%M:%S"),
                "temperature": temp,
                "max_tokens": tokens,
            }

            st.session_state.history.insert(0, card_data)
            logger.info(f"Successfully generated and saved card with ID: {card_id}")
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


@st.dialog(title=" ", width="medium")
def show_card_modal(card, lang):
    """Displays a card in modal format using Streamlit dialog"""

    st.markdown(f"## 🎯 {card['topic']}")
    st.caption(f"🤖 {card['model']} | 🕐 {card.get('timestamp', 'N/A')} | Tokens: {card.get('max_tokens', 'N/A')} | Temperature: {card.get('temperature', 'N/A')}")

    st.markdown("### 📝 Resumo Explicativo")
    st.info(card["summary"])

    st.divider()

    st.markdown("### 🔗 Subtemas Relacionados")

    cols = st.columns(len(card["subtopics"]))
    for i, (col, subtopic) in enumerate(zip(cols, card["subtopics"]), 1):
        with col:
            st.markdown(f"**Subtema {i}**")
            st.write(subtopic)
            if st.button(f"🔍 Explorar", key=f"explore_modal_{card['id']}_{i}"):
                st.session_state.topic_input = subtopic
                st.session_state.show_modal = False
                st.rerun()

    st.divider()

    if st.button(
        "🗑️ Excluir Card", key=f"delete_modal_{card['id']}", type="secondary"
    ):
        st.session_state.db.delete_card(card["id"])
        st.session_state.history = [
            c for c in st.session_state.history if c["id"] != card["id"]
        ]
        st.session_state.show_modal = False
        st.success("Card excluído!")
        time.sleep(0.5)
        st.rerun()


def main():
    """Main function to run the Streamlit app."""

    lang_code = st.session_state.language
    lang = TRANSLATIONS[lang_code]

    st.set_page_config(
        page_title=lang["app_title"],
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title(f"🎓 {lang['app_title']}")
    st.markdown(f"### {lang['app_subtitle']}")

    model_name, temp, tokens = setup_sidebar(lang, lang_code)


    st.markdown(f"### 🔍 {lang['explore_topic_header']}")

    topic_input = st.text_input(
        lang["topic_input_label"],
        placeholder=lang["topic_input_placeholder"],
        help=lang["topic_input_help"],
        key="topic_input",
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        generate_btn = st.button(
            f"🚀 {lang['generate_button']}",
            type="primary",
            use_container_width=True,
        )

    with col_btn2:
        st.button(
            f"💡 {lang['example_button']}",
            use_container_width=True,
            on_click=update_topic_input,
            args=(DEFAULT_TOPIC,),
        )

    if generate_btn and st.session_state.topic_input:
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

    if st.session_state.history:
        display_generated_cards(lang)
    else:
        display_welcome_message(lang)

    display_footer(lang)


if __name__ == "__main__":
    main()
