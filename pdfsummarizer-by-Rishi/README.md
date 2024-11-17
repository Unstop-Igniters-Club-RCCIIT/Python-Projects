
# AI Document Summarizer [RAG Project]
This project enables you to upload a PDF and ask questions from it, which is particularly useful during exams or in sensitive scenarios where minimizing model hallucination is crucial.

## Technologies Used: Python, GroqAI, Streamlit

### Installation Guide
1. Install the requirements with `pip install -r requirements.txt`.
2. Create a `.env` file.
3. In the `.env` file, provide the following keys: `GROQ_API_KEY` and `AIMODEL_API_KEY`.
4. You may choose any model ranging from Gemma to Llama 3B.
5. Launch the app by executing `streamlit run app.py`.
