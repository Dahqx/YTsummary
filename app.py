import os
import openai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_video_transcript(video_url):
    try:
        video_id = video_url.split("v=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ""
        for entry in transcript:
            text += entry['text'] + " "
        return text
    except Exception as e:
        return str(e)

def summarize_text(text_to_summarize):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"you are an expert in summarizing text,capture main points,key arguments,the summary should be informative,well structured,beneficial.written as keypoints: {text_to_summarize}",
            },
        ],
    )
    return response.choices[0].message.content

def main():
    st.title("YouTube Video Summarizer")
    video_url = st.text_input("Enter YouTube URL:")
    
    if st.button("Summarize"):
        if video_url:
            text_to_summarize = get_video_transcript(video_url)
            summary = summarize_text(text_to_summarize)
            st.subheader("Summary:")
            st.write(summary)
        else:
            st.warning("Please enter a valid YouTube URL.")

if __name__ == "__main__":
    main()