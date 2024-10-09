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
import streamlit as st
import stripe
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Function to create a payment intent
def create_payment_intent(amount):
    return stripe.PaymentIntent.create(
        amount=amount,
        currency='usd',
    )

def main():
    st.title("Payment Example App")

    st.subheader("Make a Payment")
    
    # Input for payment amount
    amount = st.number_input("Enter amount (in cents):", min_value=100)  # Minimum $1

    if st.button("Pay"):
        if amount:
            try:
                # Create a Payment Intent
                payment_intent = create_payment_intent(amount)

                # Get the client secret
                client_secret = payment_intent['client_secret']

                # Display Stripe.js form
                st.markdown("""
                <form action="" method="POST" id="payment-form">
                    <div id="card-element"></div>
                    <button id="submit">Pay</button>
                    <div id="payment-result"></div>
                </form>
                <script src="https://js.stripe.com/v3/"></script>
                <script>
                    var stripe = Stripe('YOUR_PUBLIC_STRIPE_KEY');
                    var elements = stripe.elements();
                    var cardElement = elements.create('card');
                    cardElement.mount('#card-element');

                    document.getElementById('payment-form').addEventListener('submit', function(event) {
                        event.preventDefault();
                        stripe.confirmCardPayment('""" + client_secret + """', {
                            payment_method: {
                                card: cardElement,
                            }
                        }).then(function(result) {
                            if (result.error) {
                                document.getElementById('payment-result').innerText = result.error.message;
                            } else {
                                if (result.paymentIntent.status === 'succeeded') {
                                    document.getElementById('payment-result').innerText = 'Payment successful!';
                                }
                            }
                        });
                    });
                </script>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error creating payment: {e}")

if __name__ == "__main__":
    main()
