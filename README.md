# Streamlit Chat Interface with Groq API

This Streamlit application provides a user-friendly chat interface that integrates with the Groq API, enabling users to engage in conversations with cutting-edge language models. The app offers a choice between various models, each with unique capabilities, to enrich the user experience.

## Features

- **Model Selection**: Choose from 3 models including `mixtral-8x7b-32768`,  `Gemma-7b-it` and `lama3-8b-8192` to customize the conversation dynamics. Default is : `lama3-8b-8192`
- **Chat History**: Retains a session-based chat history for a coherent conversational experience throughout the user's session via `llama-index chat engine`.
- **Dynamic Response Generation**: Leverages a generator function to fetch and stream responses dynamically from the Groq API for a fluid chat interaction.


## Requirements

- Streamlit
- Groq Python API
- Python 3.7 or higher

## Setup and Installation

1. **Install Dependencies**:
   ```shell
   pip install -r requirements.txt

2. **GROQ API Key**:
Update your GROQ API Key in : .streamlit/secrets.toml
`GROQ_API_KEY="your_api_key_here"`

3. **Run the App**:
   ```shell
   streamlit run main.py

## Usage :
- Start the app to see a welcoming title and a dropdown for model selection.
- Enter your GROQ API Key in the Sidebar menu.
- Select your desired model to begin interacting with the chat interface.
- Enter your prompts, and the app will display both the user’s inquiries and the AI’s responses, enabling an engaging dialogue. 

Enjoy !




