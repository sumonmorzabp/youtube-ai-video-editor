import streamlit as st
import subprocess
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

st.set_page_config(page_title="YouTube AI Editor", layout="centered")
st.title("🎥 Online AI Video Editor + Sound Enhancer")
st.markdown("**Upload video → Get enhanced sound & cleaned video**")

uploaded_file = st.file_uploader("Upload raw video (max 5-8 minutes recommended)", 
                                type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    input_path = "input_video.mp4"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("✅ Video uploaded!")
    st.video(input_path)

    if st.button("🚀 Start AI Sound Enhancement", type="primary", use_container_width=True):
        with st.spinner("Enhancing audio (noise removal + volume boost)..."):
            try:
                # === Audio Enhancement ===
                audio = AudioSegment.from_file(input_path)
                chunks = split_on_silence(audio, 
                                        min_silence_len=500, 
                                        silence_thresh=-40, 
                                        keep_silence=300)
                
                enhanced_audio = sum(chunks)
                enhanced_audio = enhanced_audio.normalize()
                enhanced_audio.export("enhanced_audio.wav", format="wav")

                output_path = "AI_Edited_YouTube_Video.mp4"

                # === Merge Video + Enhanced Audio using FFmpeg ===
                cmd = [
                    'ffmpeg', '-y',
                    '-i', input_path,
                    '-i', 'enhanced_audio.wav',
                    '-c:v', 'libx264',
                    '-c:a', 'aac',
                    '-b:a', '192k',
                    '-shortest',
                    output_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)

                if os.path.exists(output_path) and os.path.getsize(output_path) > 1_000_000:
                    st.success("✅ Processing Completed!")
                    st.video(output_path)

                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="⬇️ Download Final Edited Video",
                            data=file,
                            file_name="AI_Edited_YouTube_Video.mp4",
                            mime="video/mp4"
                        )
                else:
                    st.error("Processing failed")
                    st.text(result.stderr[-500:])

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Try with a shorter video (under 5 minutes)")

st.caption("Your Online AI Video Editing Agent")
