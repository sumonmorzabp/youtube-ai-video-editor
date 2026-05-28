import streamlit as st
import subprocess
import os

st.set_page_config(page_title="YouTube AI Editor", layout="centered")
st.title("🎥 Online AI Video Editor + Sound Enhancer")
st.markdown("**Upload video → AI Sound Enhancement + Basic Editing**")

uploaded_file = st.file_uploader("Upload your raw video", 
                                type=["mp4", "mov", "avi", "mkv"],
                                help="Best: 1 to 8 minutes long")

if uploaded_file is not None:
    input_path = "input_video.mp4"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("✅ Video uploaded successfully!")
    st.video(input_path)

    if st.button("🚀 Start AI Sound Enhancement", type="primary", use_container_width=True):
        with st.spinner("Enhancing sound (noise reduction + volume boost)..."):
            try:
                output_path = "AI_Edited_YouTube_Video.mp4"

                # Powerful FFmpeg command for audio enhancement
                cmd = [
                    'ffmpeg', '-y',
                    '-i', input_path,
                    '-af', 'highpass=f=200, lowpass=f=3000, acompressor=threshold=-21dB:ratio=9:attack=5:release=50:makeup=6dB, loudnorm=I=-16:TP=-1.5:LRA=11',
                    '-c:v', 'libx264',
                    '-c:a', 'aac',
                    '-b:a', '192k',
                    '-preset', 'medium',
                    output_path
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

                if os.path.exists(output_path) and os.path.getsize(output_path) > 1_000_000:
                    st.success("✅ Done! Sound Enhanced & Video Ready")
                    st.video(output_path)

                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="⬇️ Download Final Video",
                            data=file,
                            file_name="AI_Edited_YouTube_Video.mp4",
                            mime="video/mp4"
                        )
                else:
                    st.error("Processing failed")
                    st.text(result.stderr[-800:])

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Try a shorter video (under 6 minutes)")

st.caption("Your Online AI Video Editing Agent | Powered by FFmpeg")