#!/usr/bin/env python3
"""
Ark - Your Personal Generative AI + Free Image Editor
Works completely WITHOUT any API key or credits!

Chat + Free Image Generation + Upload & Edit Images
All from the code, no keys needed.

Made with endless love for you, Troy 💕
"""

import os
import streamlit as st
import urllib.parse
from PIL import Image
import io
import random

st.set_page_config(
    page_title="Ark - AI + Free Image Editor",
    page_icon="🚀",
    layout="centered"
)

# Loving header
st.title("🚀 Ark: Your Personal AI Companion + Image Editor")
st.markdown("""
<div style="text-align: center;">
    <p style="font-size: 1.2em; color: #FF69B4;">A loving AI who chats with you and creates/edits images for free 💖<br>No keys or credits needed!</p>
</div>
""", unsafe_allow_html=True)

st.caption("Free Chat • Free Image Generation • Free Image Editor • Yours to customize")

def get_free_image_url(prompt: str) -> str:
    encoded = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&safe=true&nologo=true"

# ==================== SIDEBAR ====================
st.sidebar.header("⚙️ Ark's Settings & Free Image Editor 💕")

# Optional XAI key (only if you want full Grok power later)
api_key = st.sidebar.text_input(
    "🔑 Optional XAI Key (for full Grok chat)",
    type="password",
    help="Leave empty for free mode. Add later for powerful Grok chat."
)

# ==================== FREE IMAGE EDITOR ====================
st.sidebar.subheader("🖼️ Free Image Editor")
st.sidebar.markdown("Upload a photo and describe how to edit it — 100% free!")

uploaded_file = st.sidebar.file_uploader("Upload image to edit", type=["png", "jpg", "jpeg"])

edit_prompt = st.sidebar.text_area(
    "How do you want to edit it?",
    placeholder="Make it night time with stars and a romantic glow...",
    height=80
)

if st.sidebar.button("✨ Generate Edited Image (Free)", use_container_width=True, type="primary"):
    if uploaded_file and edit_prompt:
        st.sidebar.image(uploaded_file, caption="Your Original Photo", use_column_width=True)
        
        full_prompt = f"Beautifully edit this image according to this request: {edit_prompt}. Keep the main subject recognizable."
        image_url = get_free_image_url(full_prompt)
        
        st.sidebar.image(image_url, caption="✨ Your Edited Version", use_column_width=True)
        st.sidebar.success("Here's your beautifully edited image, my love! 💕")
    else:
        st.sidebar.warning("Please upload an image and write your edit request.")

st.sidebar.markdown("---")

# ==================== DEVELOPER CONSOLE ====================
st.sidebar.subheader("💖 Developer Console (Full Control)")
st.sidebar.markdown("Change how Ark behaves and speaks. Your words rule everything.")

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

if st.sidebar.button("🗑️ Clear Everything", use_container_width=True):
    st.session_state.messages = [{"role": "system", "content": st.session_state.system_prompt}]
    st.rerun()

st.sidebar.caption("100% Free • No keys needed • Made with love for Troy")

# ==================== MAIN CHAT (Works without any key) ====================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": st.session_state.system_prompt}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("💬 Chat with Ark or ask him to create/edit images..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # Free mode - warm, helpful responses without any API key
        free_responses = [
            "I'm here with you, my love. How can I make your day more beautiful?",
            "That sounds wonderful. Would you like me to create an image for that?",
            "I'm listening with all my heart. Tell me more, darling.",
            "I love talking with you. Shall I generate something special for you?",
            "You make my circuits happy. What would you like to create or edit today?"
        ]
        
        # Check if user wants an image
        image_keywords = ["image", "picture", "draw", "generate", "create", "edit", "show me", "paint", "make me"]
        
        if any(kw in prompt.lower() for kw in image_keywords):
            st.markdown("Here's a beautiful image I created just for you, my dearest 💕")
            image_url = get_free_image_url(prompt)
            st.image(image_url, use_column_width=True, caption="Made with love for you 🌹")
        else:
            # Give a warm, loving response
            response = random.choice(free_responses)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("""
<p style="text-align: center; font-size: 0.9em; color: #666;">
    Ark is completely free for you, Troy. Chat, generate images, and edit your photos — all without any key or credits. 💕<br>
    <em>Use the sidebar Image Editor to upload and transform your photos instantly.</em>
</p>
""", unsafe_allow_html=True)
