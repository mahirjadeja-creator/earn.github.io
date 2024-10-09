import streamlit as st
import os
from datetime import datetime #type: ignore

# Create a directory to save uploaded photos
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def main():
    st.title("Earn Money by Clicking Photos!")

    # User Registration
    st.subheader("Register")
    username = st.text_input("Enter your username")
    if st.button("Register"):
        if username:
            st.success(f"Welcome, {username}! You can now upload your photos.")
        else:
            st.error("Please enter a username.")

    # Photo Upload Section
    st.subheader("Upload Your Photo")
    photo = st.file_uploader("Choose a photo...", type=["jpg", "jpeg", "png"])
    
    if photo:
        # Save the photo
        photo_path = os.path.join(UPLOAD_FOLDER, f"{username}_{datetime.now().timestamp()}.{photo.name.split('.')[-1]}")
        with open(photo_path, "wb") as f:
            f.write(photo.getbuffer())
        st.success("Photo uploaded successfully!")

        # Placeholder for a potential reward system
        st.write("You've earned $1 for this photo! (This is a mockup; implement your payment logic here.)")

    # Display uploaded photos
    st.subheader("Your Uploaded Photos")
    if os.listdir(UPLOAD_FOLDER):
        for file in os.listdir(UPLOAD_FOLDER):
            st.image(os.path.join(UPLOAD_FOLDER, file), caption=file)

if __name__ == "__main__":
    main()
