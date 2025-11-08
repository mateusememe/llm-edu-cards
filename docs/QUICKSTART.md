# 🚀 Guia Rápido de Instalação e Uso

## Sistema de Cards Educacionais com LLMs

### ⚡ Início Rápido (5 minutos)

#### 1. Pré-requisitos

Antes de começar, certifique-se de ter:

- ✅ Python 3.8 ou superior instalado
- ✅ Conexão com internet
- ✅ Conta no HuggingFace (gratuita)

#### 2. Obter Token do HuggingFace

1. Acesse: https://huggingface.co/join
2. Crie sua conta (gratuita)
3. Vá em: Settings → Access Tokens
4. Clique em "New token"
5. Dê um nome (ex: "llm-cards")
6. Selecione permissão "Read"
7. Copie o token gerado

**Formato do token:** `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## 📦 Instalação

### Opção 1: Instalação Básica

```bash
# Clone o repositório
git clone https://github.com/mateusememe/llm-edu-cards.git
cd llm-cards-educacionais

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run app.py
```

### Opção 2: Ambiente Virtual (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/mateusememe/llm-edu-cards.git
cd llm-cards-educacionais

# Crie ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run app.py
```

### Opção 3: Google Colab

```python
# Execute no Google Colab
!pip install streamlit langchain langchain-community huggingface-hub

# Baixe o arquivo app.py
!wget https://raw.githubusercontent.com/mateusememe/llm-edu-cards/main/app.py

# Execute com tunnel
!streamlit run app.py & npx localtunnel --port 8501
```

---

## 🖥️ Uso da Interface

### 1. Primeira Execução

Após executar `streamlit run app.py`, o navegador abrirá automaticamente em:
```
http://localhost:8501
```

### 2. Configuração Inicial

**Na barra lateral esquerda:**

1. **Insira seu Token:**
   - Cole o token do HuggingFace
   - Clique fora do campo para salvar

2. **(Opcional) Ajuste Parâmetros:**
   - Expanda "Parâmetros Avançados"
   - Ajuste Temperature (0.0 - 1.0)
   - Ajuste Max Tokens (100 - 1000)

### 3. Gerando Cards

**Na área principal:**

1. **Digite um tema:**
   ```
   Ex: Redes Neurais Convolucionais
   ```

2. **Clique em "Gerar Cards"**
   - Aguarde o processamento (2-5 segundos)

3. **Visualize os resultados:**
   - Resumo explicativo aparece primeiro
   - 3 subtemas relacionados aparecem em cards

4. **Explore subtemas:**
   - Clique em "🔍 Explorar" em qualquer card
   - Sistema gera novos cards para aquele subtema

### 4. Comparando Modelos

Para comparar modelos no mesmo tema:

1. Gere cards com o primeiro modelo
2. Mude o modelo na sidebar
3. Digite o mesmo tema novamente
4. Compare os resultados no histórico

---

## 💡 Exemplos Práticos

### Exemplo 1: Explorando IA

```
1. Digite: "Inteligência Artificial"
2. Clique em "Gerar Cards"
3. Explore subtema: "Machine Learning"
4. Explore subtema: "Redes Neurais"
5. Continue explorando...
```

### Exemplo 2: Estudando Matemática

```
1. Digite: "Álgebra Linear"
2. Clique em "Gerar Cards"
3. Explore subtema: "Matrizes e Determinantes"
4. Use um modelo diferente
5. Compare as explicações
```

### Exemplo 3: Temas Interdisciplinares

```
1. Digite: "Computação Quântica"
2. Clique em "Gerar Cards"
3. Observe os subtemas gerados
4. Explore progressivamente
```

---

## ⚙️ Ajuste de Parâmetros

### Temperature

**O que faz:** Controla a "criatividade" do modelo

```
0.0 - 0.3: Respostas muito precisas e determinísticas
          Recomendado para: Conteúdo técnico, matemática

0.3 - 0.7: Equilíbrio entre precisão e criatividade
          Recomendado para: Conteúdo educacional geral

0.7 - 1.0: Respostas mais criativas e variadas
          Recomendado para: Brainstorming, ideias
```

**Recomendação:** Mantenha entre 0.3 - 0.4 para uso educacional

### Max Tokens

**O que faz:** Limita o tamanho da resposta

```
100 - 300:  Respostas curtas e diretas
300 - 600:  Respostas médias (recomendado)
600 - 1000: Respostas detalhadas
```

**Recomendação:** Mantenha em 800 para equilíbrio

---

## 🐛 Solução de Problemas

### Erro: "Invalid API token"

**Causa:** Token do HuggingFace incorreto

**Solução:**
1. Verifique se copiou o token completo
2. Gere um novo token no HuggingFace
3. Cole novamente na interface

### Erro: "Model loading failed"

**Causa:** Modelo não disponível ou sobrecarga

**Solução:**

1. Tente outro modelo
2. Aguarde alguns minutos
3. Verifique sua conexão com internet

### Interface não carrega

**Causa:** Porta 8501 ocupada

**Solução:**

```bash
# Use outra porta
streamlit run app.py --server.port 8502
```

### Respostas muito lentas

**Causa:** Latência da API do HuggingFace

**Solução:**
1. Aguarde em horários de pico
2. Reduza max_tokens

### Erro de dependências

**Causa:** Versões incompatíveis

**Solução:**
```bash
# Desinstale tudo
pip uninstall -y streamlit langchain langchain-community

# Reinstale
pip install -r requirements.txt
```

---

## 📱 Uso Avançado

### 1. Executar Testes Comparativos

```bash
# Execute o script de testes
python test_comparative.py

# Siga as instruções
# Digite seu token quando solicitado
```

**O script irá:**
- Testar todos os 3 modelos
- Usar 5 temas pré-definidos
- Gerar relatório comparativo
- Exportar resultados em JSON

### 2. Personalizar Prompts

Edite o arquivo `app.py`:

```python
# Localize a função gerar_resumo()
# Modifique o template:

template = """Seu prompt personalizado aqui...
{question}
"""
```

### 3. Adicionar Novos Modelos

```python
# No app.py, adicione em MODELS:

MODELS = {
    # ... modelos existentes ...
    "Seu-Modelo": {
        "repo_id": "org/modelo-nome",
        "temperature": 0.4,
        "max_tokens": 800,
        "description": "Descrição do modelo"
    }
}
```

---

## 📊 Interpretando Resultados

### Qualidade do Resumo

**Bom resumo contém:**

- ✅ Definição clara do conceito
- ✅ Contexto e importância
- ✅ Exemplos ou aplicações
- ✅ Linguagem acessível

**Evite resumos que:**

- ❌ São muito vagos ou genéricos
- ❌ Contêm informações incorretas
- ❌ São difíceis de entender
- ❌ Fogem do tema principal

### Qualidade dos Subtemas

**Bons subtemas são:**

- ✅ Específicos e relevantes
- ✅ Relacionados ao tema principal
- ✅ Exploráveis (geram novos cards)
- ✅ Educacionalmente úteis

---

## 🎯 Dicas de Uso

### Para Estudantes

1. **Comece Amplo, Aprofunde Gradualmente**
   ```
   "Machine Learning" → "Redes Neurais" → "CNNs"
   ```

2. **Compare Modelos**
   - Teste o mesmo tema em modelos diferentes
   - Observe diferentes abordagens explicativas

3. **Use o Histórico**
   - Revise cards anteriores
   - Crie um "mapa mental" do tema

4. **Ajuste para seu Estilo**
   - Temperature mais baixa = mais objetivo
   - Temperature mais alta = mais exemplos

### Para Professores

1. **Preparação de Aulas**
   - Gere outlines de tópicos
   - Identifique conceitos relacionados

2. **Avaliação de Modelos**
   - Compare qualidade educacional
   - Identifique melhores abordagens

3. **Criação de Exercícios**
   - Use subtemas como base
   - Explore conexões entre conceitos

---

## 🔒 Segurança e Privacidade

### Sobre seu Token

- ✅ O token NÃO é armazenado permanentemente
- ✅ Válido apenas durante a sessão
- ✅ Não é compartilhado com terceiros
- ⚠️ Não commite o token no Git

### Dados Gerados

- ✅ Cards ficam apenas na sua sessão
- ✅ Nada é salvo no servidor
- ✅ Histórico é local
- ✅ Privacidade total

---

## 📚 Recursos Adicionais

### Documentação

- **README.md**: Visão geral do projeto
- **DOCUMENTACAO.md**: Documentação técnica completa
- **test_comparative.py**: Código de testes

### Links Úteis

- **HuggingFace:** https://huggingface.co/
- **Streamlit Docs:** https://docs.streamlit.io/
- **LangChain Docs:** https://python.langchain.com/
- **PPGCC-UNESP:** https://www.ibilce.unesp.br/#!/pos-graduacao/

### Comunidade

- 📧 Suporte: Via canais da disciplina
- 💬 Discussões: GitHub Issues
- 🐛 Bugs: GitHub Issues
- 💡 Sugestões: GitHub Discussions

---

## ✅ Checklist de Uso

### Antes de Começar

- [ ] Python instalado (3.8+)
- [ ] Dependências instaladas
- [ ] Token HuggingFace obtido
- [ ] Aplicação executando

### Primeiro Uso

- [ ] Token inserido na sidebar
- [ ] Modelo selecionado
- [ ] Primeiro tema testado
- [ ] Cards gerados com sucesso

## 💪 Próximos Passos

### Após Instalação

1. ✅ Teste com 3-5 temas diferentes
2. ✅ Compare os 3 modelos
3. ✅ Leia a documentação completa

---

## 🙋 Perguntas Frequentes

### P: Preciso pagar pelo token do HuggingFace?
**R:** Não! O tier gratuito é suficiente para este projeto.

### P: Posso usar offline?
**R:** Não, os modelos rodam na nuvem do HuggingFace.

### P: Quanto tempo demora cada consulta?
**R:** Entre 2-5 segundos, dependendo do modelo e carga do servidor.

### P: Posso adicionar mais modelos?
**R:** Sim! Qualquer modelo do HuggingFace compatível com LangChain.

### P: Como exporto meus cards?
**R:** Atualmente, use print/screenshot. Export em PDF é melhoria futura.

### P: Funciona em qual navegador?
**R:** Chrome, Firefox, Safari, Edge - qualquer navegador moderno.

---

*Sistema desenvolvido para a disciplina de Aprendizado Profundo - PPGCC/UNESP*
