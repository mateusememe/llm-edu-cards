# 🎓 Sistema Inteligente de Cards Educacionais com LLMs

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Sistema educacional interativo que utiliza modelos de linguagem de grande escala (LLMs) para gerar conteúdo educacional estruturado em formato de cards, desenvolvido como trabalho prático da disciplina de **Aprendizado Profundo** do [Programa de Pós-Graduação em Ciência da Computação (PPGCC)](https://www.ibilce.unesp.br/#!/pos-graduacao/programas-de-pos-graduacao/ciencia-da-computacao/) da **UNESP**, ministrada pelo **Prof. Dr. Denis Henrique Pinheiro Salvadeo**.

## ✨ Funcionalidades

- 🤖 **Modelo LLM Avançado**: Integração com Meta-Llama-3-8B-Instruct
- 🌐 **Sistema Bilíngue**: Interface em Português e Inglês
- 📝 **Geração de Resumos**: Explicações claras e objetivas de qualquer tema
- 🔗 **Subtemas Relacionados**: Explore conceitos de forma hierárquica
- 🎨 **Interface Moderna**: Design responsivo e intuitivo com Streamlit
- 💾 **Histórico de Exploração**: Revise todos os cards gerados na sessão
- ⚙️ **Configurações Avançadas**: Ajuste temperatura e max_tokens
- 📊 **Sistema Modular**: Código organizado em módulos reutilizáveis

## 🚀 Quick Start

### Pré-requisitos

- Python 3.8 ou superior
- Conta no [HuggingFace](https://huggingface.co/)
- Token de API do HuggingFace

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/llm-edu-cards.git
cd llm-edu-cards

# Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### Execução

```bash
# Execute a aplicação
streamlit run app.py
```

Acesse `http://localhost:8501` no seu navegador.

## 🔑 Configuração da API

1. Crie uma conta no [HuggingFace](https://huggingface.co/join)
2. Gere um token de API em [Settings → Access Tokens](https://huggingface.co/settings/tokens)
3. Na interface do Streamlit, insira o token no campo da sidebar
4. Ou configure como variável de ambiente: `HUGGINGFACEHUB_API_TOKEN`

> ⚠️ **Nota de Segurança:** Nunca compartilhe seu token de API publicamente

## 🤖 Modelo LLM Utilizado

### Meta-Llama-3-8B-Instruct

**Características:**
- Parâmetros: 8 bilhões
- Arquitetura: Transformer otimizado
- Desenvolvido por: Meta AI
- Especialização: Instruções e conversação

**Vantagens:**
- ⚡ Rápido e eficiente
- 🎯 Respostas precisas e bem estruturadas
- 🌍 Suporte multilíngue nativo
- 💡 Excelente compreensão de contexto

**Configuração:**
```python
{
    "temperature": 0.3,
    "max_tokens": 800
}
```

## 🎯 Exemplos de Uso

### Exemplo 1: Explorando IA (Português)

```
Input: "Redes Neurais Convolucionais"

Output:
- Resumo: Explicação detalhada sobre CNNs...
- Subtemas:
  1. Camadas de Convolução e Pooling
  2. Arquiteturas Clássicas
  3. Transfer Learning
```

### Exemplo 2: Exploring AI (English)

```
Input: "Convolutional Neural Networks"

Output:
- Summary: Detailed explanation about CNNs...
- Subtopics:
  1. Convolution and Pooling Layers
  2. Classic Architectures
  3. Transfer Learning
```

## ⚙️ Configurações Avançadas

### Hiperparâmetros

| Parâmetro        | Descrição             | Valores    | Recomendação      |
| ---------------- | --------------------- | ---------- | ----------------- |
| `temperature`    | Controla criatividade | 0.0 - 1.0  | 0.3 para educação |
| `max_new_tokens` | Limite de tokens      | 100 - 2048 | 800 padrão        |

### Personalização

Os prompts podem ser customizados no arquivo `config.py`:

```python
TRANSLATIONS = {
    "pt": {
        "summary_template": """...""",
        "subtopics_template": """..."""
    }
}
```

## 📝 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🎓 Informações Acadêmicas

**Disciplina:** Aprendizado Profundo  
**Instituição:** Programa de Pós-Graduação em Ciência da Computação (PPGCC) - UNESP  
**Professor:** Prof. Dr. Denis Henrique Pinheiro Salvadeo  
**Site PPGCC:** [Link para o programa](https://www.ibilce.unesp.br/#!/pos-graduacao/programas-de-pos-graduacao/ciencia-da-computacao/)

## 👥 Contribuidores

Este projeto foi desenvolvido colaborativamente como trabalho em grupo para a disciplina de Aprendizado Profundo do PPGCC-UNESP:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/ViniciusARZ">
        <img src="https://github.com/ViniciusARZ.png" width="100px;" alt="Vinicius Ramos"/><br />
        <sub><b>Vinicius Ramos</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/omiguelsma">
        <img src="https://github.com/omiguelsma.png" width="100px;" alt="Miguel Martins"/><br />
        <sub><b>Miguel Martins</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/mateusememe">
        <img src="https://github.com/mateusememe.png" width="100px;" alt="Mateus Mendonça"/><br />
        <sub><b>Mateus Mendonça</b></sub>
      </a>
    </td>
  </tr>
</table>
