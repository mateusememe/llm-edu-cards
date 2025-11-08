"""
LLM Service Module (Bilingual Version)
"""

import streamlit as st
import logging
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import MODELS, TRANSLATIONS
from utils import parse_subtopics_response

logger = logging.getLogger(__name__)


@st.cache_resource(ttl=3600)
def initialize_model(model_name, api_token, temperature, max_tokens):
    """
    Initializes and caches the selected LLM.
    """
    try:
        if model_name not in MODELS:
            raise ValueError(f"Unknown model: {model_name}")

        config = MODELS[model_name]
        logger.info(
            f"Initializing model: {config['repo_id']} with temp={temperature}, max_tokens={max_tokens}"
        )

        llm_base = HuggingFaceEndpoint(
            repo_id=config["repo_id"],
            huggingfacehub_api_token=api_token,
            temperature=temperature,
            max_new_tokens=max_tokens,
        )
        return ChatHuggingFace(llm=llm_base)

    except Exception as e:
        logger.error(f"Failed to initialize model {model_name}: {e}", exc_info=True)
        raise e


def generate_summary(llm: ChatHuggingFace, topic: str, lang_code: str) -> str:
    """
    Generates an explanatory summary for a given topic in the specified language.

    Args:
        llm (ChatHuggingFace): The initialized chat model.
        topic (str): The topic to summarize.
        lang_code (str): The language code (e.g., 'en', 'pt').

    Returns:
        str: The generated summary.
    """
    logger.debug(f"Generating summary for: {topic} in language: {lang_code}")

    try:
        template_string = TRANSLATIONS[lang_code]["summary_template"]
    except KeyError:
        logger.warning(
            f"No summary template found for lang '{lang_code}'. Defaulting to 'en'."
        )
        template_string = TRANSLATIONS["en"]["summary_template"]

    prompt = ChatPromptTemplate.from_messages([("human", template_string)])
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    return chain.invoke({"question": topic})


def generate_subtopics(llm: ChatHuggingFace, topic: str, lang_code: str) -> list[str]:
    """
    Generates 3 related subtopics for a given topic in the specified language.

    Args:
        llm (ChatHuggingFace): The initialized chat model.
        topic (str): The main topic.
        lang_code (str): The language code (e.g., 'en', 'pt').

    Returns:
        list[str]: A list of 3 subtopics.
    """
    logger.debug(f"Generating subtopics for: {topic} in language: {lang_code}")

    try:
        template_string = TRANSLATIONS[lang_code]["subtopics_template"]
    except KeyError:
        logger.warning(
            f"No subtopics template found for lang '{lang_code}'. Defaulting to 'en'."
        )
        template_string = TRANSLATIONS["en"]["subtopics_template"]

    prompt = ChatPromptTemplate.from_messages([("human", template_string)])
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    response_text = chain.invoke({"question": topic})
    logger.debug(f"Raw subtopics response: {response_text}")

    parsed_subtopics = parse_subtopics_response(response_text)
    logger.debug(f"Parsed subtopics: {parsed_subtopics}")

    return parsed_subtopics
