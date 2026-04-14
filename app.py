import streamlit as st
from api_calling import note_generator, audio_transcription, quiz_generator
from PIL import Image  # to handle image upload to gemini
import string



st.title('Note Summary and Quiz Generator', anchor=False)
st.markdown("Upload upto 3 images to generate Note Summary ans Quizzes")
st.divider()


with st.sidebar:             # everything will be under sidebar
    
    st.header("Controls")
    
    # image
    images = st.file_uploader(
        'Upload the photos of your note',
        type=['jpg','jpeg','png'],
        accept_multiple_files=True
    )
    
    if images:
        if(len(images)>3):
            st.error("Upload at max 3 images")
        
        else:
            pil_images=[]
            for img in images:
                pil_img = Image.open(img)
                pil_images.append(pil_img)

            st.subheader("Uploaded images")
            col = st.columns(len(images))
            for i,per_image in enumerate(images):
                with col[i]:
                    st.image(per_image)
    
    # difficulty
    difficulty = st.selectbox(
        'Enter the difficulty of Quiz',
        ('Easy', 'Medium', "Hard"),
        index=None
    )
    if difficulty:
        st.markdown(f'You selected **{difficulty}** as the difficulty of Quiz')
    # else:
    #     st.error("You must select a difficulty")
        
        
    button = st.button('Click the button to initiate AI' ,type='primary') 

# error handling   
if button:
    if not images:
        st.error("Upload at least 1 image")
        
    if not difficulty:
        st.error("Select a difficulty")
        
    if images and difficulty:
        
        #note
        with st.container( border=True):
            st.subheader('Your Note:', anchor=False)
            
            with st.spinner("AI is generating notes for you"):
                generated_note = note_generator(pil_images)
                st.markdown(generated_note)
            
            st.divider()
        
            #audio
            st.subheader('Audio Transcription:', anchor=False)
            with st.spinner("AI is generating audio for you"):
                
                modified_note = generated_note.translate(
                    str.maketrans(string.punctuation, ' ' * len(string.punctuation))
                    )
                
                generated_audio = audio_transcription(modified_note) 
                st.audio(generated_audio)
 
        st.divider()
           
        #quiz
        with st.container( border=True):
            st.subheader(f'Quiz ({difficulty} Level):', anchor=False)
            with st.spinner("AI is generating quiz for you"):
                generated_quiz = quiz_generator(pil_images,difficulty)
                st.markdown(generated_quiz)
 
   
       
        
    
    