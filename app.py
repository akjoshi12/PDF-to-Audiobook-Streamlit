import streamlit as st
import os
import uuid
import asyncio
import shutil
import logic
import io

# --- Page Config ---
st.set_page_config(
    page_title="PDF to Audiobook Converter",
    page_icon="📚",
    layout="centered",
)

# --- App State ---
if "voices" not in st.session_state:
    st.session_state.voices = []
if "selected_voice" not in st.session_state:
    st.session_state.selected_voice = None
if "conversion_task" not in st.session_state:
    st.session_state.conversion_task = None
if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None
if "error" not in st.session_state:
    st.session_state.error = None

# --- UI Components ---
st.title("📖 PDF to Audiobook Converter")
st.markdown(
    "Upload a PDF file, choose a voice, and convert your document into an audiobook."
)

uploaded_file = st.file_uploader(
    "Upload your PDF", type="pdf", help="Select the PDF file you want to convert."
)

# --- Voice Selection ---
async def load_voices():
    """Loads voices into the session state."""
    if not st.session_state.voices:
        try:
            voices = await logic.get_voices()
            st.session_state.voices = voices
            # Set a default voice if none is selected
            if not st.session_state.selected_voice and voices:
                st.session_state.selected_voice = voices[0]
        except Exception as e:
            st.error(f"Could not load voices: {e}")
            st.session_state.voices = logic.DEFAULT_VOICES

# Run the async function to load voices
asyncio.run(load_voices())

if st.session_state.voices:
    st.session_state.selected_voice = st.selectbox(
        "Choose a voice",
        st.session_state.voices,
        index=st.session_state.voices.index(st.session_state.selected_voice)
        if st.session_state.selected_voice in st.session_state.voices
        else 0,
        help="Select the voice for your audiobook.",
    )

# --- Conversion Logic ---
async def run_conversion_async(task_id: str, file_bytes: bytes, voice: str, progress_bar, status_text):
    """The main async worker for processing the PDF conversion in Streamlit."""
    temp_dir = f"output/{task_id}_temp"
    try:
        status_text.text("Status: Processing...")
        progress_bar.progress(5)

        # Extract text
        status_text.text("Status: Extracting text from PDF...")
        raw_text = logic.extract_text_from_pdf(io.BytesIO(file_bytes))
        if not raw_text.strip():
            raise ValueError("Could not extract any text from the PDF.")
        
        cleaned_text = logic.clean_text(raw_text)
        chunks = logic.chunk_text(cleaned_text)
        total_chunks = len(chunks)
        os.makedirs(temp_dir, exist_ok=True)

        # Convert chunks to speech
        status_text.text(f"Status: Converting {total_chunks} text chunks to audio...")
        temp_audio_files = []
        for i, chunk in enumerate(chunks):
            chunk_filename = os.path.join(temp_dir, f"chunk_{i:04d}.mp3")
            try:
                await logic.convert_chunk_to_speech(chunk, voice, chunk_filename)
                temp_audio_files.append(chunk_filename)
                # Update progress (scaled between 10% and 85%)
                progress = 10 + int(((i + 1) / total_chunks) * 75)
                progress_bar.progress(progress)
            except Exception as e:
                st.warning(f"Skipping a chunk due to an error: {e}")

        if not temp_audio_files:
            raise ValueError("No audio chunks were successfully created.")

        # Merge audio files
        status_text.text("Status: Merging audio files...")
        progress_bar.progress(90)
        combined_audio = logic.merge_audio_files(temp_audio_files)
        
        # Export to bytes
        audio_bytes_io = logic.export_audio_to_bytes(combined_audio)
        st.session_state.audio_bytes = audio_bytes_io.getvalue()
        
        status_text.text("Status: Complete!")
        progress_bar.progress(100)
        st.session_state.error = None

    except Exception as e:
        st.session_state.error = f"An error occurred: {e}"
        status_text.text(f"Status: Failed. {st.session_state.error}")
        st.error(st.session_state.error)
    finally:
        # Clean up temporary files
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

# --- Convert Button ---
if st.button("Convert to Audiobook", disabled=not uploaded_file or not st.session_state.selected_voice):
    st.session_state.audio_bytes = None
    st.session_state.error = None
    task_id = str(uuid.uuid4())
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    file_bytes = uploaded_file.getvalue()
    
    # Run the async conversion
    asyncio.run(
        run_conversion_async(
            task_id, file_bytes, st.session_state.selected_voice, progress_bar, status_text
        )
    )

# --- Display Results ---
if st.session_state.audio_bytes:
    st.subheader("Your Audiobook is Ready!")
    st.audio(st.session_state.audio_bytes, format="audio/mp3")
    st.download_button(
        label="Download Audiobook (MP3)",
        data=st.session_state.audio_bytes,
        file_name="audiobook.mp3",
        mime="audio/mp3",
    )

if st.session_state.error:
    st.error(f"Conversion failed: {st.session_state.error}")

# --- Footer ---
st.markdown("---")
st.markdown("Powered by [Streamlit](https://streamlit.io) and [edge-tts](https://github.com/rany2/edge-tts).")
