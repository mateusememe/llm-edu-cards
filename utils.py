"""
Utility Functions Module

This module contains helper functions used across the application,
such as logging configuration and response parsing.
"""

import logging
import streamlit as st


def setup_logging():
    """Configures the root logger."""
    # This setup logs to both a file and the console
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),  # Log to a file
            logging.StreamHandler(),  # Log to the console
        ],
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)  # Quieten noisy libraries


def parse_subtopics_response(text: str) -> list[str]:
    """
    Processes and cleans the raw LLM response for subtopics.

    Args:
        text (str): The raw text output from the LLM.

    Returns:
        list[str]: A list of 3 cleaned subtopics.
    """
    if not text:
        return []

    # Split by lines and strip whitespace
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    cleaned_lines = []
    for line in lines:
        # Remove common numbering patterns (e.g., "1.", "2.", "-", "*")
        # This uses lstrip to remove leading characters
        cleaned_line = line.lstrip("0123456789.-*• ")

        # Quality filter: ensure the line is not empty and has substance
        if cleaned_line and len(cleaned_line) > 10:
            cleaned_lines.append(cleaned_line)

    # Return only the first 3 relevant items
    return cleaned_lines[:3]


def load_css(file_name: str):
    """Loads a CSS file into the Streamlit app."""
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        logging.warning(f"CSS file not found: {file_name}")
        st.warning(f"Could not load custom styles. {file_name} not found.")
