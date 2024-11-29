import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Configure API key
genai.configure(api_key="")

prompt = "Convert this into a meaningful 100 to 150-word summary using simple and precise language, only include text in the response."

def generate_test(prompt, transcript=""):
    try:
        model = genai.GenerativeModel("gemini-pro")
        
        # Generate the response
        response = model.generate_content(prompt + transcript)
        
        if response.parts:
            return response.parts[0].text
        else:
            return "No valid text was returned in the response."
    
    except Exception as e:
        return f"An error occurred: {e}"

def trncript_video(video_id):
    try:
        # Retrieve the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Concatenate all transcript entries into a single string
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text
    
    except Exception as e:
        return f"An error occurred: {e}"

st.title("YouTube Video Summary Generator")

# Use session state to preserve values across reruns
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""

youtube_link = st.text_input("Enter YouTube URL or video ID")

if st.button("Get Transcript"):
    
    video_id = youtube_link.split("v=")[-1] if "v=" in youtube_link else youtube_link
    st.session_state.transcript = trncript_video(video_id)
    st.write("### Transcript:")
    st.write(st.session_state.transcript)

if st.session_state.transcript:
    if st.button("Generate Summary"):
        st.session_state.summary = generate_test(prompt, st.session_state.transcript)
    
    if st.session_state.summary:
        st.markdown("## Summary Content")
        st.write(st.session_state.summary)
