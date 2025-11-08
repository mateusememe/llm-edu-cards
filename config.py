"""
Configuration File

This file stores all constants, model definitions, and prompt templates
for the application.
"""

MODELS = {
    "meta-llama/Meta-Llama-3-8B-Instruct": {
        "repo_id": "meta-llama/Meta-Llama-3-8B-Instruct",
        "temperature": 0.3,
        "max_tokens": 800,
    },
}

DEFAULT_TOPIC = "Reinforcement Learning"

TRANSLATIONS = {
    "en": {
        "app_title": "Intelligent Educational Card System",
        "app_subtitle": "Educational content generator with LLMs",
        "settings_header": "Settings",
        "api_token_label": "HuggingFace API Token",
        "api_token_help": "Enter your HuggingFace API Token. You can also set this as HUGGINGFACEHUB_API_TOKEN in your environment.",
        "model_select_label": "Select LLM Model",
        "model_select_help": "Choose the language model",
        "model_desc_llama": "Efficient and accurate model, great for structured answers.",
        "advanced_params_header": "Advanced Parameters",
        "temperature_label": "Temperature",
        "temperature_help": "Controls the creativity of the responses",
        "max_tokens_label": "Max New Tokens",
        "max_tokens_help": "Limit of tokens in the response",
        "project_about_header": "About the Project",
        "project_about_course": "Course",
        "project_about_institution": "Institution",
        "project_about_professor": "Professor",
        "clear_history_button": "Clear History",
        "language_select_label": "Language / Idioma",
        "explore_topic_header": "Explore a Topic",
        "topic_input_label": "Enter a topic to explore:",
        "topic_input_placeholder": "E.g., Convolutional Neural Networks",
        "topic_input_help": "Enter an educational topic to generate content",
        "generate_button": "Generate Cards",
        "example_button": "Use Example",
        "stats_header": "Statistics",
        "stats_cards_generated": "Cards Generated",
        "stats_current_model": "Current Model",
        "search_help": "Press enter to search cards by topic",
        "spinner_message": "Processing with",
        "db_stats_expander": "Database Statistics",
        "stats_total_metric": "Cards Generated",
        "stats_recent_cards": "Recent Cards (7 days)",
        "stats_by_language": "By Language",
        "topic_search_input_placeholder": "Enter a topic to search...",
        "topic_search_header": "Search Cards",
        "error_no_token": "Please enter your HuggingFace API Token in the sidebar!",
        "error_generation_failed": "API Error: Invalid HuggingFace API Token. Please check your token in the sidebar.",
        "error_generic": "An error occurred",
        "error_check_console": "Please check the console or logs for more details.",
        "success_message": "Cards generated successfully using",
        "generated_cards_header": "Generated Cards",
        "summary_box_header": "Explanatory Summary",
        "subtopics_header": "Related Subtopics",
        "subtopic_card_header": "Subtopic",
        "explore_button": "Explore",
        "welcome_message": "👆 Enter a topic above and click 'Generate Cards' to start!",
        "example_topics_header": "Example Topics",
        "example_topics": [
            "Transformers in NLP",
            "Generative Adversarial Networks",
            "Transfer Learning",
        ],
        "footer_title": "System developed for the Deep Learning course - PPGCC/UNESP",
        "footer_devs": "Developed by",
        "footer_license": "MIT License - Free use for educational purposes",
        "summary_template": """
You are an expert educator. Explain the concept of "{question}" clearly, objectively, and educationally.
Your response must be in **English**.

Include the following:
1.  Main definition
2.  Key related concepts
3.  Practical applications

Keep the entire response to a maximum of 150 words.
""",
        "subtopics_template": """
You are a curriculum designer. List EXACTLY 3 specific and relevant subtopics related to "{question}".
Your response must be in **English**.

Expected format:
1. [Specific Subtopic 1]
2. [Specific Subtopic 2]
3. [Specific Subtopic 3]

Be specific and educational. Respond ONLY with the 3 items, with no introduction or conclusion.
""",
    },
    "pt": {
        "app_title": "Sistema Inteligente de Cards Educacionais",
        "app_subtitle": "Gerador de conteúdo educacional com LLMs",
        "settings_header": "Configurações",
        "api_token_label": "Token da API HuggingFace",
        "api_token_help": "Insira seu Token da API HuggingFace. Você também pode defini-lo como HUGGINGFACEHUB_API_TOKEN em seu ambiente.",
        "model_select_label": "Selecione o Modelo LLM",
        "model_select_help": "Escolha o modelo de linguagem",
        "model_desc_llama": "Modelo eficiente e preciso, ótimo para respostas estruturadas.",
        "advanced_params_header": "Parâmetros Avançados",
        "temperature_label": "Temperatura",
        "temperature_help": "Controla a criatividade das respostas",
        "max_tokens_label": "Máximo de Tokens",
        "max_tokens_help": "Limite de tokens na resposta",
        "project_about_header": "Sobre o Projeto",
        "project_about_course": "Disciplina",
        "project_about_institution": "Instituição",
        "project_about_professor": "Professor",
        "clear_history_button": "Limpar Histórico",
        "language_select_label": "Language / Idioma",
        "explore_topic_header": "Explore um Tema",
        "topic_input_label": "Digite um tema para explorar:",
        "topic_input_placeholder": "Ex: Redes Neurais Convolucionais",
        "topic_input_help": "Insira um tema educacional para gerar conteúdo",
        "generate_button": "Gerar Cards",
        "example_button": "Usar Exemplo",
        "stats_header": "Estatísticas",
        "stats_cards_generated": "Cards Gerados",
        "stats_current_model": "Modelo Atual",
        "db_stats_expander": "Estatísticas do Banco de Dados",
        "stats_total_metric": "Total de Cards",
        "stats_recent_cards": "Cards Recentes (7 dias)",
        "stats_by_language": "Por Idioma",
        "search_help": "Pressione Enter para buscar cards relacionados ao tema.",
        "topic_search_input_placeholder": "Digite um tema para buscar...",
        "topic_search_header": "Buscar cards",
        "spinner_message": "Processando com",
        "error_no_token": "Por favor, insira seu Token da API HuggingFace na barra lateral!",
        "error_generation_failed": "Erro de API: Token da API HuggingFace inválido. Por favor, verifique seu token na barra lateral.",
        "error_generic": "Ocorreu um erro",
        "error_check_console": "Por favor, verifique o console ou os logs para mais detalhes.",
        "success_message": "Cards gerados com sucesso usando",
        "generated_cards_header": "Cards Gerados",
        "summary_box_header": "Resumo Explicativo",
        "subtopics_header": "Subtemas Relacionados",
        "subtopic_card_header": "Subtema",
        "explore_button": "Explorar",
        "welcome_message": "👆 Digite um tema acima e clique em 'Gerar Cards' para começar!",
        "example_topics_header": "Exemplos de Temas",
        "example_topics": [
            "Transformers em PLN",
            "Redes Generativas Adversariais",
            "Aprendizagem por Transferência",
        ],
        "footer_title": "Sistema desenvolvido para a disciplina de Aprendizado Profundo - PPGCC/UNESP",
        "footer_devs": "Desenvolvido por",
        "footer_license": "Licença MIT - Uso livre para fins educacionais",
        "summary_template": """
Você é um educador especialista. Explique o conceito de "{question}" de forma clara, objetiva e educacional.
Sua resposta deve ser em **Português**.

Inclua o seguinte:
1.  Definição principal
2.  Conceitos relacionados importantes
3.  Aplicações práticas

Mantenha a resposta inteira com um máximo de 150 palavras.
""",
        "subtopics_template": """
Você é um designer instrucional. Liste EXATAMENTE 3 subtemas específicos e relevantes relacionados a "{question}".
Sua resposta deve ser em **Português**.

Formato esperado:
1. [Subtema específico 1]
2. [Subtema específico 2]
3. [Subtema específico 3]

Seja específico e educacional. Responda APENAS com os 3 itens, sem introdução ou conclusão.
""",
    },
}
