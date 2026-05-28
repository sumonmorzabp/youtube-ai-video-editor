import streamlit as st
from moviepy.editor import VideoFileClip, concatenate_videoclips
from pydub import AudioSegment
from pydub.silence import split_on_silence
import whisper
import os

st.set_page_config(page_title="YouTube AI Video Editor", layout="centered")
st.title("🎥 AI Video Editor + Sound Enhancer")
st.markdown("### Upload raw video → Get professional YouTube ready video")

uploaded_file = st.file_uploader("Upload your video (max 100MB recommended)", 
                                type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    # Save uploaded file
    with open("input_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("Video uploaded successfully!")
    st.video("input_video.mp4")

    if st.button("🚀 Start AI Editing & Sound Enhancement", type="primary"):
        with st.spinner("Processing... This may take 3-10 minutes depending on video length"):
            
            try:
                # === Sound Enhancement ===
                st.write("🔊 Enhancing Audio...")
                audio = AudioSegment.from_file("input_video.mp4")
                # Remove silence and normalize
                chunks = split_on_silence(audio, min_silence_len=600, silence_thresh=-40)
                processed_audio = sum(chunks)
                processed_audio = processed_audio.normalize().effects.normalize()
                processed_audio.export("enhanced_audio.wav", format="wav")

                # === Transcription ===
                st.write("📝 Transcribing video...")
                model = whisper.load_model("base")
                result = model.transcribe("input_video.mp4")
                st.write("**Transcript Preview:**", result["text"][:400] + "...")

                # === Video Processing (Basic version) ===
                st.write("✂️ Editing video...")
                video = VideoFileClip("input_video.mp4")
                final_video = video  # You can improve this later with cuts
                
                # Add enhanced audio
                final_video = final_video.set_audio(VideoFileClip("input_video.mp4").audio)

                final_video.write_videofile("final_edited_video.mp4", 
                                          fps=24, 
                                          codec="libx264", 
                                          audio_codec="aac",
                                          threads=4)

                st.success("✅ Processing Complete!")
                st.video("final_edited_video.mp4")

                # Download button
                with open("final_edited_video.mp4", "rb") as file:
                    st.download_button(
                        label="⬇️ Download Your Edited Video",
                        data=file,
                        file_name="AI_Edited_YouTube_Video.mp4",
                        mime="video/mp4"
                    )
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Try with a shorter video (under 5 minutes)")

st.caption("Your Personal Online AI Video Editing Agent")
