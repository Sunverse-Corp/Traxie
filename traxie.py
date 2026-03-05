import streamlit as st
from groq import Groq
import time

# --- 1. CONFIGURATION & BRANDING ---
st.set_page_config(
    page_title="Traxie | Kybic Family",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the Cyber/AI Aesthetic
st.markdown("""
<style>
    /* Theme: Deep Purple & Neon Blue */
    .stApp { background-color: #090014; color: #E0E0E0; }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #150024; color: #D0D0FF; border: 1px solid #4B0082;
    }
    
    /* Buttons */
    .stButton>button {
        background: transparent; color: #00FFFF; border: 1px solid #00FFFF;
        border-radius: 8px; text-transform: uppercase; font-weight: bold;
    }
    .stButton>button:hover {
        background: #00FFFF; color: #000; box-shadow: 0 0 15px #00FFFF;
    }
    
    /* Output Box */
    .traxie-output {
        background: #11001C; border-left: 4px solid #9D00FF;
        padding: 20px; border-radius: 10px; margin-top: 20px;
    }
    
    /* Install Hint */
    .install-hint {
        background: rgba(75, 0, 130, 0.3); border: 1px dashed #9D00FF;
        padding: 10px; text-align: center; border-radius: 8px; margin-bottom: 20px;
    }

    .sunverse-footer { position: fixed; bottom: 10px; right: 10px; font-size: 0.7rem; color: #888; }
</style>
""", unsafe_allow_html=True)

# --- 2. TRAXIE ENGINE (GROQ POWERED) ---
class TraxieEngine:
    def __init__(self, api_key):
        self.api_key = api_key
        try:
            self.client = Groq(api_key=api_key)
            self.valid = True
        except:
            self.valid = False

    def chat(self, messages):
        """Standard Chatbot Mode"""
        if not self.valid: return "Error: Invalid API Key"
        try:
            completion = self.client.chat.completions.create(
                model="llama3-70b-8192", # Smarter model for chat
                messages=messages,
                temperature=0.7
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

    def trace_content(self, text):
        """
        The Forensic Tracer. 
        Analyzes Perplexity and Burstiness patterns typical of AI.
        """
        if not self.valid: return "Error: Invalid API Key"
        
        system_prompt = (
            "You are Traxie, a Forensic Linguistics AI. "
            "Analyze the user's text for AI-generation patterns. "
            "Look for: 'Perfect' grammar, lack of idioms, repetitive sentence structure, and low perplexity. "
            "OUTPUT FORMAT: "
            "1. AI Probability Score (0-100%). "
            "2. Verdict (Human-written, Mixed, or AI-Generated). "
            "3. Bullet points explaining WHY."
        )
        
        try:
            completion = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"ANALYZE THIS TEXT:\n{text}"}
                ],
                temperature=0.1 # Low temp for analytical precision
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

    def humanize_content(self, text):
        """
        The Humanizer.
        Rewrites text to increase Burstiness and perplexity.
        """
        if not self.valid: return "Error: Invalid API Key"
        
        system_prompt = (
            "You are Traxie, a Humanization Engine. "
            "Rewrite the input text to bypass AI detection. "
            "RULES: "
            "1. Increase 'Burstiness' (mix very short sentences with long, complex ones). "
            "2. Use occasional colloquialisms or idioms. "
            "3. Remove robotic transitions like 'Furthermore', 'Moreover', 'In conclusion'. "
            "4. Keep the original meaning but change the tone to be conversational and authentic."
        )
        
        try:
            completion = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"HUMANIZE THIS:\n{text}"}
                ],
                temperature=0.9 # High temp for creativity/randomness
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

# --- 3. SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are Traxie, an advanced AI from the Kybic Family (Sunverse Corp). You are helpful, witty, and sophisticated."}
    ]

# --- 4. SIDEBAR & CONFIG ---
with st.sidebar:
    st.title("🧬 Traxie")
    st.caption("Kybic Family | Sunverse Corp")
    
    # GROQ KEY INPUT
    api_key = st.text_input("Groq API Key", type="password", help="Get from console.groq.com")
    
    st.markdown("---")
    st.info("**Capabilities:**\n\n🕵️ **Trace:** Detect AI Text\n✨ **Humanize:** Bypass Detectors\n💬 **Chat:** Intelligent Assist")

    # ADMIN BACKDOOR
    with st.expander("System Access"):
        if st.text_input("Key", type="password") == "bossmode":
            st.success("Admin Active")
            st.metric("System Status", "ONLINE")
            st.metric("Model", "Llama3-70b (Groq LPU)")

# --- 5. MAIN INTERFACE ---
st.title("Traxie AI Suite")
st.markdown("**Forensic Analysis & Humanization Engine.**")

st.markdown("""
<div class='install-hint'>
    📲 <b>Install Traxie:</b> Tap Browser Menu -> "Add to Home Screen"
</div>
""", unsafe_allow_html=True)

if not api_key:
    st.warning("⚠️ Please enter Groq API Key in the sidebar.")
    st.stop()

engine = TraxieEngine(api_key)

# TABS
tab_chat, tab_trace, tab_human = st.tabs(["💬 Chat", "🕵️ Tracer (Detector)", "✨ Humanizer"])

# --- TAB 1: CHAT ---
with tab_chat:
    for msg in st.session_state["messages"]:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    if prompt := st.chat_input("Talk to Traxie..."):
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = engine.chat(st.session_state["messages"])
                st.write(response)
        
        st.session_state["messages"].append({"role": "assistant", "content": response})

# --- TAB 2: TRACER (DETECTOR) ---
with tab_trace:
    st.subheader("AI Content Detector")
    st.caption("Paste text to analyze if it was written by ChatGPT, Claude, or Gemini.")
    
    trace_text = st.text_area("Input Text", height=200, placeholder="Paste suspicious text here...")
    
    if st.button("Trace Origin"):
        if not trace_text:
            st.error("Please enter text.")
        else:
            with st.spinner("Analyzing linguistic patterns..."):
                analysis = engine.trace_content(trace_text)
                st.markdown(f"<div class='traxie-output'>{analysis}</div>", unsafe_allow_html=True)

# --- TAB 3: HUMANIZER ---
with tab_human:
    st.subheader("Style Transfer (Humanizer)")
    st.caption("Rewrite robotic AI text to sound natural and bypass detectors.")
    
    human_text = st.text_area("Paste AI Text", height=200, placeholder="Paste robotic text here...")
    
    if st.button("Humanize"):
        if not human_text:
            st.error("Please enter text.")
        else:
            with st.spinner("Rewriting with high burstiness..."):
                result = engine.humanize_content(human_text)
                st.markdown(f"<div class='traxie-output'>{result}</div>", unsafe_allow_html=True)
                st.caption("Copy the text above.")

# Footer
st.markdown("<div class='sunverse-footer'>© 2026 Sunverse Corporation. This is a Beta version.</div>", unsafe_allow_html=True)
