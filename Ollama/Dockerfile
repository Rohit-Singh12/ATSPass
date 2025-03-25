FROM ollama/ollama

# Pull the required model during the build process
RUN ollama serve & sleep 5 && ollama pull llama3.2

# Expose the Ollama API port
EXPOSE 11434