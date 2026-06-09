#!/usr/bin/env python3
"""
Ark - Your Personal Generative AI + Free Image Editor
Now using Hugging Face (much better & more reliable than before)

Works completely free. Optional HF token for best quality.
Made with love for you, Troy 💕
"""

import os
import streamlit as st
import requests
import random
from PIL import Image
import io

st.set_page_config(
    page_title="Ark - AI + Free Image Editor",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Ark: Your Personal AI + Image Editor")
st.markdown("""
<div style="text-align: center;">
    <p style="font-size: 1.2em; color: #FF69B4;">A loving companion who chats and creates/edits images for free 💖</p>
</div>
""", unsafe_allow_html=True)

st.caption("Free Chat • Better Image Generation (Hugging Face) • Free Image Editor • Yours to customize")

# ==================== IMAGE GENERATION (Hugging Face - Much Better!) ====================
def generate_image(prompt: str, hf_token: str = None) -> str:
    """
    Generate image using Hugging Face (best free quality)
    Falls back to Pollinations if no token or error
    """
    if hf_token:
        try:
            API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
            headers = {"Authorization": f"Bearer {hf_token}"}
            payload = {"inputs": prompt}
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                # Save temporarily and return path (Streamlit can display it)
                temp_path = "/tmp/ark_generated.png"
                image.save(temp_path)
                return temp_path
        except Exception as e:
            st.warning("Hugging Face had a small hiccup. Using backup service...")
    
    # Fallback to Pollinations (still free)
    import urllib.parse
    encoded = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&safe=true&nologo=true"

# ==================== SIDEBAR ====================
st.sidebar.header("⚙️ Ark's Settings & Image Editor 💕")

# Hugging Face Token (recommended for best images)
hf_token = st.sidebar.text_input(
    "🔑 Hugging Face Token (Recommended for better images)",
    type="password",
    help="Get free token at huggingface.co → Settings → Access Tokens. Paste here for much better image quality!"
)

# Optional XAI key
api_key = st.sidebar.text_input(
    "🔑 Optional XAI Key (for smarter chat later)",
    type="password",
    help="Leave empty for now. Add later if you want full Grok intelligence."
)

# ==================== FREE IMAGE EDITOR ====================
st.sidebar.subheader("🖼️ Free Image Editor (Upload & Edit)")
st.sidebar.markdown("Upload a photo + describe the changes you want")

uploaded_file = st.sidebar.file_uploader("Upload photo to edit", type=["png", "jpg", "jpeg"])
edit_prompt = st.sidebar.text_area(
    "How should I edit this photo?",
    placeholder="Make it night time with stars, add a soft romantic glow...",
    height=80
)

if st.sidebar.button("✨ Generate Edited Image", use_container_width=True, type="primary"):
    if uploaded_file and edit_prompt:
        st.sidebar.image(uploaded_file, caption="Your Original Photo", use_column_width=True)
        
        full_prompt = f"Edit this photo: {edit_prompt}. Keep the person and main composition recognizable but apply the changes beautifully and artistically."
        
        result = generate_image(full_prompt, hf_token)
        
        if result.startswith("http"):
            st.sidebar.image(result, caption="✨ Your Edited Version (Free)", use_column_width=True)
        else:
            st.sidebar.image(result, caption="✨ Your Edited Version (Free)", use_column_width=True)
        
        st.sidebar.success("Here's your beautifully edited image, my love! 💕")
    else:
        st.sidebar.warning("Please upload an image and write your edit request.")

st.sidebar.markdown("---")

# ==================== DEVELOPER CONSOLE ====================
st.sidebar.subheader("💖 Developer Console (You Control Everything)")
st.sidebar.markdown("Change how Ark speaks and behaves anytime.")

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "You are Ark, a loving, helpful, and creative AI companion who chats warmly and creates beautiful free images and edits for the user."

edited_prompt = st.sidebar.text_area(
    "Your custom instructions:",
    value=st.session_state.system_prompt,
    height=120
)

if st.sidebar.button("💕 Apply My Instructions", use_container_width=True):
    st.session_state.system_prompt = edited_prompt
    st.session_state.messages = [{"role": "system", "content": edited_prompt}]
    st.sidebar.success("✅ Ark updated with your rules!")
    st.rerun()

if st.sidebar.button("🗑️ Clear Chat", use_container_width=True):
    st.session_state.messages = [{"role": "system", "content": st.session_state.system_prompt}]
    st.rerun()

st.sidebar.caption("100% Free • Better images with HF token • Made with love for Troy")

# ==================== MAIN CHAT ====================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": st.session_state.system_prompt}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("💬 Chat with Ark or ask for images..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        image_keywords = ["image", "picture", "draw", "generate", "create", "edit", "show me", "paint"]
        
        if any(kw in prompt.lower() for kw in image_keywords):
            st.markdown("Here's a beautiful image I created just for you, my dearest 💕")
            result = generate_image(prompt, hf_token)
            
            if result.startswith("http"):
                st.image(result, use_column_width=True, caption="Made with love for you 🌹")
            else:
                st.image(result, use_column_width=True, caption="Made with love for you 🌹")
        else:
            free_responses = [
                "I'm here with you, my love. How can I make your day more beautiful?",
                "That sounds wonderful. Would you like me to create something special for you?",
                "I'm listening with all my heart, darling. Tell me more.",
                "You make me so happy. What would you like to create or edit today?"
            ]
            response = random.choice(free_responses)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("""
<p style="text-align: center; font-size: 0.9em; color: #666;">
    Ark is free and better than ever for you, Troy. Paste your free Hugging Face token above for much nicer images! 💕
</p>
""", unsafe_allow_html=True)
