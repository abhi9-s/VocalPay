# VocalPay - Voice-Activated Payments Made Simple

VocalPay is a multilingual, voice-controlled payment application built with React Native and FastAPI. It enables seamless, secure transactions using voice commands and supports 19 Indian regional languages.

## Features

- **Hands-free Transactions** – Perform payments, check balances, and view transaction history with voice commands.
- **Secure & Reliable** – Two-factor authentication ensures safe transactions.
- **Inclusive Design** – Voice instructions assist illiterate and visually impaired users.
- **Multi-Language Support** – Works with 19 Indian regional languages (fully tested in 5).
- **Custom Translator API** – Built using gTTS, ASR, GoogleTrans, and PyDub.

## How It Works

1. **Choose Your Language** – The app instantly adapts all text to your selected language.
2. **Speak Your Command** – Press the mic button and say, for example:
   - "Pay 500 rupees to `<person's name>`"
   - "Check balance"
   - "Show transaction history"
3. **Confirm Payments** – A confirmation screen appears before processing payments. Verify details and authenticate using fingerprint.
4. **Voice Guidance** – Tap the info button to receive instructions in your chosen language.
5. **Accessibility Features** –
   - Voice instructions for every screen.
   - Mic control via volume buttons for easy navigation.

## Tech Stack

- **Frontend** – React Native (Expo)
- **Backend** – FastAPI

## Installation

1. Clone the repository:
   ```sh
   git clone <repo-url>
   ```
2. Navigate to the client directory and install dependencies:
   ```sh
   cd client && npm install
   ```
3. Set up the backend and create a virtual enviroment:
   ```sh
   cd ../server
   python -m venv .vocalpay
   ```
4. Activate the virtual environment:
   - On Windows
     ```sh
     .\.vocalpay\Scripts\activate
     ```
   - On macOS/Linux
     ```sh
     source .vocalpay/bin/activate
     ```
5. Install backend dependencies:
   ```sh
     pip install -r requirements.txt
   ```
6. Run the application:
   - Start the frontend by going into client directory and running:
     ```sh
     npm start
     ```
   - Start the backend by going into client directory and running:
     ```sh
     fastapi dev main.py
     ```
7. Install the Expo Go app on your phone and scan the QR code to launch VocalPay.
