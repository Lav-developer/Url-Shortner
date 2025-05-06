import streamlit as st
from urllib.parse import urlencode
from urllib.request import urlopen
import contextlib
import validators
import pyperclip

# Function to shorten URL using TinyURL API
def make_short(url):
    try:
        request_url = "https://tinyurl.com/api-create.php?" + urlencode({'url': url})
        with contextlib.closing(urlopen(request_url)) as response:
            return response.read().decode('utf-8'), None
    except Exception as e:
        return None, f"Error shortening URL: {str(e)}"

# Streamlit app configuration
st.set_page_config(
    page_title="Pro URL Shortener",
    page_icon="🔗",
    layout="centered"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        padding: 10px;
    }
    .result-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #e0e0e0;
        margin-top: 10px;
        word-break: break-all;
        color: #2c3e50; /* Set text color to dark gray for visibility */
        font-size: 16px; /* Ensure readable font size */
    }
    .title {
        color: #2c3e50;
        font-size: 2.5em;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .subtitle {
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2em;
    }
    </style>
""", unsafe_allow_html=True)

# App title and description
st.markdown('<h1 class="title">Pro URL Shortener</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform long URLs into short, shareable links with ease.</p>', unsafe_allow_html=True)

# Input form
with st.form(key="url_form"):
    url_input = st.text_input("Enter your URL", placeholder="https://example.com", key="url")
    submit_button = st.form_submit_button(label="Shorten URL")

# Handle form submission
if submit_button and url_input:
    # Validate URL
    if not validators.url(url_input):
        st.error("Please enter a valid URL (e.g., https://example.com)")
    else:
        with st.spinner("Shortening your URL..."):
            short_url, error = make_short(url_input)
            if short_url:
                st.session_state['short_url'] = short_url  # Store in session state
                st.success("URL shortened successfully!")
            else:
                st.error(error)

# Display result and copy button
if 'short_url' in st.session_state:
    st.markdown(f'<div class="result-box">{st.session_state["short_url"]}</div>', unsafe_allow_html=True)
    if st.button("Copy to Clipboard"):
        try:
            pyperclip.copy(st.session_state['short_url'])
            st.info("Short URL copied to clipboard!")
        except Exception as e:
            st.warning("Failed to copy to clipboard. Please copy the URL manually.")

# Footer
st.markdown("""
    <hr>
    <p style='text-align: center; color: #7f8c8d;'>
        Developed by Lav Kush | Powered by TinyURL & Streamlit
    </p>
""", unsafe_allow_html=True)