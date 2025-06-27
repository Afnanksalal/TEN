FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- ADD THESE LINES TO DOWNLOAD NLTK DATA ---
# Set NLTK_DATA environment variable for where to store/find data
ENV NLTK_DATA=/usr/local/share/nltk_data
# Create the directory
RUN mkdir -p ${NLTK_DATA}
# Download the lexicon into the specified directory
RUN python -c "import nltk; nltk.download('vader_lexicon', download_dir='${NLTK_DATA}')"
# --- END NLTK DATA ADDITION ---

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]