import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.schema import Document
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Streamlit app title
st.markdown("""
    <style>
    @keyframes typewriter {
        from {
            width: 0;
        }
        to {
            width: 100%;
        }
    }

    .animated-title {
        overflow: hidden;
        white-space: nowrap;
        animation: typewriter 2s cubic-bezier(0.25, 0.1, 0.25, 1) 0s 1 normal both;
        text-align: center; /* Center the text horizontally */
    }
    </style>
    <h1 class="animated-title">Rogue AI 🤖</h1>
""", unsafe_allow_html=True)

# Custom header
st.markdown("""
    <style>
    @keyframes typewriter {
        from {
            width: 0;
        }
        to {
            width: 100%;
        }
    }

    .animated-header {
        overflow: hidden;
        white-space: nowrap;
        animation: typewriter 2s cubic-bezier(0.25, 0.1, 0.25, 1) 0s 1 normal both;
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        padding: 10px;
    }
    </style>
    <h1 class="animated-header"> Your Study Assistant</h1>
""", unsafe_allow_html=True)

# Navbar
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["Home", "About"])

# Custom footer
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        text-align: center;
        padding: 10px;
        font-size: 16px;
        color: #2c3e50;
        z-index: 3;
    }
    </style>
    <div class="footer">Built with 💖 by Rishi © 2024</div>
""", unsafe_allow_html=True)

if page == "Home":
    # Friendly greeting
    st.markdown("""
    <style>
    @keyframes typewriter {
        from {
            width: 0;
        }
        to {
            width: 100%;
        }
    }

    .animated-header {
        font-size: 3vw; /* Set font size relative to viewport width */
        overflow: hidden;
        white-space: nowrap;
        animation: typewriter 2s cubic-bezier(0.25, 0.1, 0.25, 1) 0s 1 normal both;
        text-align: center; /* Center the text horizontally */
    }
    </style>
    <h3 class="animated-header">Upload Files Using the sidebar.</h3>
""", unsafe_allow_html=True)

    # Initialize LLM and prompt template
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma-7b-it")
    prompt = ChatPromptTemplate.from_template(
        """Answer the questions based on the provided context and also from the internet if the context isn't present.
        Please provide the most accurate and long detailed responses based on the question.
        <context>
        {context}
        <context>
        Questions: {input}
        """
    )

    # Initialize session state variables
    if "vectors" not in st.session_state:
        st.session_state.vectors = None
    if "embeddings" not in st.session_state:
        st.session_state.embeddings = None
    if "docs" not in st.session_state:
        st.session_state.docs = None
    if "text_splitter" not in st.session_state:
        st.session_state.text_splitter = None
    if "final_documents" not in st.session_state:
        st.session_state.final_documents = None

    def process_uploaded_files(uploaded_files):
        temp_dir = "temp_files"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        documents = []
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        return documents

    def get_youtube_transcripts(video_urls):
        transcripts = []
        for url in video_urls:
            if url.strip():  # Check if URL is not empty
                video_id = url.split("v=")[-1].split("&")[0]
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                    transcript = " ".join([entry['text'] for entry in transcript_list])
                    transcripts.append(Document(page_content=transcript, metadata={"source": url}))
                except Exception as e:
                    st.warning(f"Could not retrieve transcript for video {url}: {e}")
        return transcripts

    def vector_embedding(uploaded_files, video_urls):
        if st.session_state.vectors is None:
            st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            
            # Process PDF documents
            pdf_docs = process_uploaded_files(uploaded_files)
            
            # Process YouTube video transcripts
            youtube_docs = get_youtube_transcripts(video_urls) if video_urls else []
            
            # Convert pdf_docs to Document objects
            pdf_docs = [Document(page_content=doc.page_content, metadata={"source": "pdf"}) for doc in pdf_docs]
            
            # Combine documents
            all_docs = pdf_docs + youtube_docs
            
            # Ensure documents are not empty
            if not all_docs:
                st.error("No valid documents or transcripts found.")
                return
            
            # Split documents into chunks
            st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            st.session_state.final_documents = st.session_state.text_splitter.split_documents(all_docs)
            
            # Ensure there are valid chunks
            if not st.session_state.final_documents:
                st.error("No valid document chunks generated.")
                return
            
            # Create vector embeddings
            st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

    # Sidebar for file upload and video URLs
    with st.sidebar:
        st.header("Upload Your Files and Enter Video URLs")
        uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type="pdf")
        video_urls = st.text_area("Enter YouTube video URLs (one per line)").split("\n")
        st.write("###")

    # User input for question
    prompt1 = st.text_input("What's your question?")

    # Custom button for processing
    if st.button("Ask me Daddy 🫦"):
        if uploaded_files or any(video_urls):
            with st.spinner("Processing documents... Please wait."):
                vector_embedding(uploaded_files, video_urls)
                st.success("Documents processed successfully.")
            
            if prompt1:
                if st.session_state.vectors is not None:
                    document_chain = create_stuff_documents_chain(llm, prompt)
                    retriever = st.session_state.vectors.as_retriever()
                    retrieval_chain = create_retrieval_chain(retriever, document_chain)
                    
                    start = time.process_time()
                    response = retrieval_chain.invoke({'input': prompt1})
                    st.write(f"Response time: {time.process_time() - start} seconds")
                    
                    st.write("### Here's the answer to your question:")
                    st.markdown(f"**{response['answer']}**")
                    
                    # With a Streamlit expander
                    with st.expander("Document Similarity Search"):
                        st.write("### Relevant Document Chunks:")
                        for i, doc in enumerate(response["context"]):
                            st.write(doc.page_content)
                            st.write("--------------------------------")
                else:
                    st.warning("Processing documents... Please wait.")
        else:
            st.warning("Please upload some PDF files or enter YouTube video URLs.")

elif page == "About":
    st.title("About the Project")
    st.markdown("## Tech Stack")
    st.markdown(" Python, Streamlit, FAISS, GROQ API, YouTube Transcript API")
    st.markdown("## Purpose")
    st.markdown("This is a study assistant AI that helps you answer questions based on the context provided in the uploaded PDF files and YouTube video transcripts.")
    st.markdown("## Follow Me 🚀")
    st.markdown("[GitHub](https://github.com/rishicds) | [LinkedIn](https://www.linkedin.com/in/rishi-paul04/) | [Website](https://rishi-paul04.vercel.app/)")
