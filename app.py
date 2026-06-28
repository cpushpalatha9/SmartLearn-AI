import streamlit as st
from google import genai
from google.genai import types
import json
import os
from dotenv import load_dotenv

# Automatically loads variables from a local .env file into os.environ
load_dotenv()

# ==========================================
# 1. INITIAL SYSTEM SETUP & CONFIG
# ==========================================
st.set_page_config(
    page_title="SmartLearn AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CRUCIAL: Pre-initialize session state keys at startup to prevent silent white-screen freezes
if 'quiz_generated' not in st.session_state:
    st.session_state.quiz_generated = False
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []

# Vibrant Yellow-Orange GPT-Inspired Premium Theme Custom Styling
st.markdown("""
    <style>
    /* Main body background refinement */
    .main .block-container { 
        padding-top: 1.5rem; 
        max-width: 1200px;
    }
    
    /* Global Button Overhaul - Bright Energetic Yellow/Orange Gradient */
    .stButton>button { 
        width: 100%; 
        border-radius: 12px; 
        font-weight: 700;
        background: linear-gradient(135deg, #ff9900 0%, #ff5e62 100%);
        color: white !important;
        border: none;
        padding: 0.6rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 94, 98, 0.4);
    }
    
    /* GPT-Style Message/Card Containers with a warm Orange border accent */
    .flashcard {
        padding: 2rem;
        background: #ffffff;
        border-radius: 16px;
        border-left: 6px solid #ff9900;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    
    .quiz-card {
        padding: 1.5rem;
        background: #fffdfa;
        border-radius: 14px;
        border: 1px solid #fbe5d6;
        margin-bottom: 1rem;
    }
    
    .quiz-q {
        font-weight: 600;
        font-size: 1.15rem;
        color: #1e293b;
        margin-bottom: 0.75rem;
    }
    
    /* Tab UI enhancements with modern Orange state mappings */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        background-color: #f8fafc;
        border-radius: 8px 8px 0px 0px;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f1f5f9;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #ff9900 0%, #ff5e62 100%);
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🔑 SECURED API CONFIGURATION (Using standard environment loading)
API_KEY = os.getenv("GEMINI_API_KEY")

try:
    client = genai.Client(api_key=API_KEY)
    MODEL_ID = "gemini-2.5-flash"
except Exception as e:
    st.error(f"Failed to connect to Gemini API. Error: {e}")

# Sidebar: Simple Dashboard Overview
with st.sidebar:
    st.markdown("<h2 style='color:#ff9900; font-weight:700;'>🧠 SmartLearn AI</h2>", unsafe_allow_html=True)
    st.write("An advanced generative AI educational workspace engineered for automated learning acceleration.")
    
    st.markdown("---")
    st.markdown("### 🛠️ Workspace Modules")
    st.markdown("- **💡 Concept Clarifier**: Core parameter deconstruction via text or PDF files.")
    st.markdown("- **📝 Note Summarizer**: Structural logic conversion for uploaded assets.")
    st.markdown("- **🧠 Flashcard Engine**: On-demand interactive active-recall cards.")
    st.markdown("- **🎯 Quiz Master**: Instantly targets memory retention testing.")

# ==========================================
# 2. APPLICATION BRANDING & TABS DEFINITION
# ==========================================
st.markdown("<h1 style='text-align: left; font-size: 3rem; font-weight: 800; background: -webkit-linear-gradient(45deg, #ff9900, #ff5e62, #ffb347); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🧠 SmartLearn AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.25rem; font-weight: 500; color: #4a5568; margin-top: -10px;'>Learn Smarter • Study Faster</p>", unsafe_allow_html=True)
st.write("")

tab1, tab2, tab3, tab4 = st.tabs([
    "💡 Concept Clarifier", 
    "📝 Note Summarizer", 
    "🧠 Flashcards", 
    "🎯 Practice Quiz"
])


# ==========================================
# TAB 1: CONCEPT CLARIFIER (With PDF Support)
# ==========================================
with tab1:
    st.markdown("<h3 style='color:#ff5e62;'>Adaptive Concept Clarifier</h3>", unsafe_allow_html=True)
    st.write("Deconstruct complex technical frameworks from text or an uploaded PDF into structured, logical breakdowns.")
    
    input_mode = st.radio("Choose Input Method:", ["Type a Concept", "Upload a PDF Document"], horizontal=True)
    
    concept_input = ""
    uploaded_pdf = None
    
    if input_mode == "Type a Concept":
        concept_input = st.text_input("Enter the target concept or theory for deconstruction:", placeholder="e.g., Quantum Entanglement, Photosynthesis")
    else:
        uploaded_pdf = st.file_uploader("Upload your study PDF document:", type=["pdf"])

    academic_level = st.selectbox("Target Academic Cohort", ["Middle School", "High School", "Undergraduate"], key="clarifier_level")
        
    if st.button("Send", key="btn_explain"):
        structure_prompt = f"""
        You are an elite, highly empathetic academic instructor. Deconstruct the material provided for an audience at the {academic_level} level.
        
        Structure your response precisely as follows:
        1. ## 📌 Executive Summary
           Provide a clear, precise, 2-sentence foundational overview.
        2. ## 🔄 Conceptual Analogy
           Map this to a universally understood real-world mechanism or system to build intuition.
        3. ## ⚙️ Core Mechanics & Architecture
           Break down the systematic components, processes, or chronological steps using plain, jargon-free terminology.
        4. ## 🚀 Real-World Implementation & Significance
           Explain why this is critical in its field and its current industry applications.
        
        Maintain an encouraging, professional, and pedagogically sound tone.
        """

        if input_mode == "Type a Concept" and concept_input:
            with st.spinner("Deconstructing complex parameters into accessible frameworks..."):
                prompt = f"Target Concept: '{concept_input}'\n\n{structure_prompt}"
                try:
                    response = client.models.generate_content(model=MODEL_ID, contents=prompt)
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    
        elif input_mode == "Upload a PDF Document" and uploaded_pdf is not None:
            with st.spinner("Processing PDF data and extracting core concepts..."):
                try:
                    pdf_bytes = uploaded_pdf.read()
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=[
                            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                            f"Analyze this document and execute this plan:\n{structure_prompt}"
                        ]
                    )
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred while processing the PDF: {e}")
        else:
            st.warning("Please provide an input concept or upload a PDF file first!")


# ==========================================
# TAB 2: NOTE SUMMARIZER (With PDF Support)
# ==========================================
with tab2:
    st.markdown("<h3 style='color:#ff5e62;'>Note Summarizer & Key Takeaways</h3>", unsafe_allow_html=True)
    st.write("Paste raw text notes or drop in a complete textbook/lecture PDF to synthesize high-yield study guides.")
    
    sum_mode = st.radio("Choose Summary Source:", ["Paste Text Notes", "Upload Notes PDF"], horizontal=True)
    
    notes_text = ""
    sum_pdf = None
    
    if sum_mode == "Paste Text Notes":
        notes_text = st.text_area("Paste your study text here:", height=200, placeholder="Paste paragraphs, essay content, or transcript logs...")
    else:
        sum_pdf = st.file_uploader("Upload your lecture/chapter PDF:", type=["pdf"], key="summarizer_pdf")
    
    if st.button("Send", key="btn_sum"):
        summary_prompt = """
        You are a high-performing student assistant. Analyze the material and extract a concise, structured study guide.
        
        Format your output exactly like this:
        ## 📌 Core Theme & Objective
        [Brief summary of what this text is trying to teach]
        
        ## 🔑 Key Terms & Definitions
        - **Term**: Definition
        
        ## 🚀 Critical Concepts & Mechanics
        - [Bullet points breaking down key processes, arguments, or rules]
        
        ## ⚠️ Common Pitfalls / Mistakes to Avoid
        - [What do students typically get wrong or confuse about this specific material?]
        """
        
        if sum_mode == "Paste Text Notes" and notes_text:
            with st.spinner("Extracting high-yield study points..."):
                try:
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=[f"Material to analyze:\n\"\"\"{notes_text}\"\"\"\n\nInstructions:\n{summary_prompt}"]
                    )
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    
        elif sum_mode == "Upload Notes PDF" and sum_pdf is not None:
            with st.spinner("Synthesizing PDF documentation..."):
                try:
                    pdf_bytes = sum_pdf.read()
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=[
                            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                            summary_prompt
                        ]
                    )
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred while synthesizing the PDF: {e}")
        else:
            st.warning("Please paste text or upload a PDF first!")


# ==========================================
# TAB 3: FLASHCARD GENERATOR
# ==========================================
with tab3:
    st.markdown("<h3 style='color:#ff5e62;'>Active Recall Flashcards</h3>", unsafe_allow_html=True)
    st.write("Input a topic to generate digital flashcards designed to test your memory retention.")
    
    fc_topic = st.text_input("Enter a topic for flashcards:", placeholder="e.g., Mitosis stages, Roman Empire fall, Python Data Structures")
    
    if st.button("Send", key="btn_fc"):
        if fc_topic:
            with st.spinner("Creating dynamic flashcards..."):
                prompt = f"""
                You are an educational assistant creating study flashcards. Generate 4 highly effective flashcards based on the topic: '{fc_topic}'.
                
                Provide your response strictly in a valid JSON array format containing objects with 'front' and 'back' keys. Do not include markdown wraps.
                """
                try:
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json"
                        ),
                    )
                    flashcards = json.loads(response.text)
                    
                    st.markdown("---")
                    for i, card in enumerate(flashcards):
                        with st.container():
                            st.markdown("<div class='flashcard'>", unsafe_allow_html=True)
                            st.markdown(f"<h4 style='color:#ff9900; margin-top:0;'>🃏 Card {i+1}</h4>", unsafe_allow_html=True)
                            st.markdown(f"**Front (Question):** \n{card['front']}")
                            
                            with st.expander("👀 Reveal Answer"):
                                st.markdown(f"<span style='color:#ff5e62; font-style:italic;'>{card['back']}</span>", unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                except Exception as e:
                    st.error("Failed to parse flashcards automatically. Please try again.")
        else:
            st.warning("Please enter a flashcard topic!")


# ==========================================
# TAB 4: PRACTICE QUIZ MASTER
# ==========================================
with tab4:
    st.markdown("<h3 style='color:#ff5e62;'>Interactive Practice Quiz</h3>", unsafe_allow_html=True)
    st.write("Test your knowledge! Input a topic, generate a quiz, and check your answers instantly.")
    
    quiz_topic = st.text_input("What subject do you want to be quizzed on?", placeholder="e.g., Newtonian Mechanics, Basic Spanish Grammar, Cellular Respiration")
    
    if st.button("Send", key="btn_quiz"):
        if quiz_topic:
            with st.spinner("Drafting your personalized quiz..."):
                prompt = f"""
                You are an elite academic examiner. Create a 3-question Multiple Choice Quiz based on the topic: '{quiz_topic}'.
                
                Provide your response strictly in a JSON array format containing objects matching this template:
                {{
                    "question": "The question text?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "answer": "The exact string match of the correct option",
                    "explanation": "Brief explanation why this option is correct."
                }}
                """
                try:
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json"
                        ),
                    )
                    st.session_state.quiz_data = json.loads(response.text)
                    st.session_state.quiz_generated = True
                except Exception as e:
                    st.error("Could not construct quiz data cleanly. Please try clicking the button again.")
        else:
            st.warning("Please input a topic for your test!")
            
    if st.session_state.quiz_generated and st.session_state.quiz_data:
        st.markdown("---")
        st.markdown("<h3 style='color:#ff9900;'>📝 Test Your Understanding</h3>", unsafe_allow_html=True)
        
        user_answers = {}
        for idx, item in enumerate(st.session_state.quiz_data):
            st.markdown(f"<div class='quiz-card'>", unsafe_allow_html=True)
            st.markdown(f"<p class='quiz-q'>Q{idx+1}: {item['question']}</p>", unsafe_allow_html=True)
            user_answers[idx] = st.radio(
                f"Select option for Q{idx+1}:", 
                options=item['options'], 
                key=f"q_{idx}",
                label_visibility="collapsed"
            )
            st.markdown("</div>", unsafe_allow_html=True)
            st.write("")
            
        if st.button("Submit Quiz Answers", type="primary"):
            score = 0
            st.markdown("### 📊 Quiz Results:")
            
            for idx, item in enumerate(st.session_state.quiz_data):
                if user_answers[idx] == item['answer']:
                    score += 1
                    st.success(f"**Question {idx+1}: Correct!** ✅")
                else:
                    st.error(f"**Question {idx+1}: Incorrect** ❌ \n\n* **Your Answer:** {user_answers[idx]}\n* **Correct Answer:** {item['answer']}")
                
                st.info(f"💡 *Explanation:* {item['explanation']}")
                st.markdown("---")
                
            st.metric(label="Final Score", value=f"{score} / {len(st.session_state.quiz_data)}")