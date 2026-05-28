import streamlit as st
import subprocess
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

st.set_page_config(page_title="YouTube AI Editor", layout="wide")
st.title("🎥 Online AI Video Editor + Sound Enhancer")
st.markdown("**Upload → Auto Sound Enhancement & Basic Editing**")

uploaded_file = st.file_uploader("Upload your raw video", 
                                type=["mp4", "mov", "avi", "mkv"], 
                                help="Recommended: under 5 minutes for free tier")

if uploaded_file is not None:
    input_path = "input_video.mp4"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("✅ Video uploaded successfully!")
    st.video(input_path)

    if st.button("🚀 Start AI Sound Enhancement & Editing", type="primary"):
        with st.spinner("Processing audio enhancement... (please wait)"):
            try:
                # Sound Enhancement
                audio = AudioSegment.from_file(input_path)
                chunks = split_on_silence(audio, 
                                        min_silence_len=500, 
                                        silence_thresh=-40, 
                                        keep_silence=250)
                
                enhanced = sum(chunks)
                enhanced = enhanced.normalize()
                enhanced.export("enhanced_audio.wav", format="wav")

                output_path = "AI_Edited_Video.mp4"

                # Merge with FFmpeg
                cmd = [
                    'ffmpeg', '-y',
                    '-i', input_path,
                    '-i', 'enhanced_audio.wav',
                    '-c:v', 'libx264',
                    '-c:a', 'aac',
                    '-shortest',
                    output_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)

                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    st.success("✅ Processing Completed Successfully!")
                    st.video(output_path)

                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="⬇️ Download Final Video",
                            data=file,
                            file_name="AI_Edited_YouTube_Video.mp4",
                            mime="video/mp4"
                        )
                else:
                    st.error("Processing failed. Check logs.")
                    st.text(result.stderr)

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Try a very short video (1-3 minutes)")

st.caption("Your Online AI Video Editing Agent")
