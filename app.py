import os

from io import BytesIO

from datetime import datetime


import streamlit as st

from dotenv import load_dotenv

from pypdf import PdfReader

from docx import Document


# =====================================================
# LANGCHAIN + OPENAI
# =====================================================

from langchain_openai import (
    ChatOpenAI,
    OpenAIEmbeddings
)

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser


# =====================================================
# CHROMADB
# =====================================================

from langchain_chroma import Chroma

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


# =====================================================
# TOKEN COUNTING
# =====================================================

import tiktoken


# =====================================================
# LOAD ENV VARIABLES
# =====================================================

load_dotenv()


# =====================================================
# STREAMLIT PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="AI Resume Screening Platform",

    page_icon="📄",

    layout="wide"

)


st.title("📄 AI Resume Screening Platform")

st.write(
    "Upload resumes and compare candidates with job requirements using OpenAI + ChromaDB."
)


# =====================================================
# VERIFY OPENAI API KEY
# =====================================================

api_key_loaded = os.getenv("OPENAI_API_KEY") is not None

st.write("✅ OpenAI API Key Loaded:", api_key_loaded)


# =====================================================
# OPENAI EMBEDDINGS
# =====================================================

embeddings = OpenAIEmbeddings(

    model="text-embedding-3-small"

)


# =====================================================
# TOKEN COUNTER
# =====================================================

def count_tokens(text, model="gpt-4o-mini"):

    encoding = tiktoken.encoding_for_model(model)

    return len(encoding.encode(text))


# =====================================================
# READ PDF FILE
# =====================================================

def read_pdf(uploaded_file):

    pdf_reader = PdfReader(
        BytesIO(uploaded_file.read())
    )

    text = ""

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


# =====================================================
# READ DOCX FILE
# =====================================================

def read_docx(uploaded_file):

    document = Document(uploaded_file)

    text = ""

    for paragraph in document.paragraphs:

        text += paragraph.text + "\n"

    return text


# =====================================================
# READ TXT FILE
# =====================================================

def read_txt(uploaded_file):

    return uploaded_file.read().decode("utf-8")


# =====================================================
# EXTRACT RESUME TEXT
# =====================================================

def extract_resume_text(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):

        return read_pdf(uploaded_file)

    elif file_name.endswith(".docx"):

        return read_docx(uploaded_file)

    elif file_name.endswith(".txt"):

        return read_txt(uploaded_file)

    else:

        return ""


# =====================================================
# SPLIT TEXT INTO CHUNKS
# =====================================================

def split_resume_text(text):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200

    )

    return splitter.split_text(text)


# =====================================================
# STORE IN CHROMADB
# =====================================================

def store_resume_in_chroma(chunks):

    vectorstore = Chroma(

        collection_name="resumes",

        embedding_function=embeddings,

        persist_directory="./chroma_db"

    )

    vectorstore.add_texts(chunks)

    return vectorstore


# =====================================================
# JOB DESCRIPTION INPUT
# =====================================================

job_requirements = st.text_area(

    "Enter Job Requirements",

    height=250,

    placeholder=(
        "Example: Senior Python Developer with "
        "5+ years experience, FastAPI, SQL, "
        "Cloud, REST APIs..."
    )

)


# =====================================================
# FILE UPLOAD
# =====================================================

uploaded_resume = st.file_uploader(

    "Upload Resume",

    type=["pdf", "docx", "txt"]

)


# =====================================================
# ANALYZE BUTTON
# =====================================================

if st.button("Analyze Resume"):


    # -------------------------------------------------
    # CHECK API KEY
    # -------------------------------------------------

    if not os.getenv("OPENAI_API_KEY"):

        st.error(
            "OpenAI API key not found. "
            "Please add OPENAI_API_KEY in .env file."
        )

        st.stop()


    # -------------------------------------------------
    # VALIDATE JOB REQUIREMENTS
    # -------------------------------------------------

    if not job_requirements:

        st.error("Please enter job requirements.")

        st.stop()


    # -------------------------------------------------
    # VALIDATE FILE
    # -------------------------------------------------

    if uploaded_resume is None:

        st.error("Please upload a resume.")

        st.stop()


    # -------------------------------------------------
    # EXTRACT RESUME TEXT
    # -------------------------------------------------

    resume_text = extract_resume_text(uploaded_resume)


    if not resume_text.strip():

        st.error(
            "Could not extract text from resume."
        )

        st.stop()


    # -------------------------------------------------
    # SHOW EXTRACTED TEXT
    # -------------------------------------------------

    with st.expander("📄 View Extracted Resume Text"):

        st.write(resume_text)


    # -------------------------------------------------
    # TOKEN COUNTING
    # -------------------------------------------------

    resume_tokens = count_tokens(resume_text)

    jd_tokens = count_tokens(job_requirements)

    total_tokens = resume_tokens + jd_tokens


    st.info(f"""

📊 Token Usage Estimate

- Resume Tokens: {resume_tokens}
- Job Description Tokens: {jd_tokens}
- Total Input Tokens: {total_tokens}

""")


    # -------------------------------------------------
    # SPLIT RESUME INTO CHUNKS
    # -------------------------------------------------

    chunks = split_resume_text(resume_text)


    st.success(
        f"✅ Resume split into {len(chunks)} chunks"
    )


    # -------------------------------------------------
    # STORE IN CHROMADB
    # -------------------------------------------------

    vectorstore = store_resume_in_chroma(chunks)


    st.success(
        "✅ Resume embeddings stored in ChromaDB"
    )


    # =================================================
    # CREATE PROMPT
    # =================================================

    prompt = ChatPromptTemplate.from_messages([

        (

            "system",

            """
You are an expert HR resume screening assistant.

Your task is to compare a candidate resume
with the job requirements.

Rules:
- Use only resume information
- Do not assume missing details
- Keep evaluation fair and objective
- Focus only on professional relevance
"""

        ),

        (

            "human",

            """
Job Requirements:
{job_requirements}

Candidate Resume:
{resume_text}

Create a detailed resume screening report.

Include:

1. Candidate Fit Summary

2. Overall Match Score (0-100)

3. Matched Skills

4. Missing Skills

5. Experience Relevance

6. Education Evaluation

7. Strengths

8. Weaknesses / Gaps

9. HR Recommendation

Choose one:
- Strongly Shortlist
- Shortlist
- Hold / Needs Review
- Do Not Shortlist

10. Suggested Interview Questions

Generate 5 interview questions.
"""

        )

    ])


    # =================================================
    # OPENAI MODEL
    # =================================================

    llm = ChatOpenAI(

        model="gpt-4o-mini",

        temperature=0.2

    )


    # =================================================
    # CREATE CHAIN
    # =================================================

    chain = prompt | llm | StrOutputParser()


    # =================================================
    # GENERATE REPORT
    # =================================================

    with st.spinner("🤖 Analyzing Resume..."):

        report = chain.invoke({

            "job_requirements": job_requirements,

            "resume_text": resume_text

        })


    # =================================================
    # DISPLAY REPORT
    # =================================================

    st.subheader("📋 Resume Screening Report")

    st.write(report)


    # =================================================
    # DOWNLOAD REPORT
    # =================================================

    file_name = (

        "resume_screening_report_"

        + datetime.now().strftime("%Y%m%d_%H%M%S")

        + ".txt"

    )


    st.download_button(

        label="⬇️ Download Report",

        data=report,

        file_name=file_name,

        mime="text/plain"

    )