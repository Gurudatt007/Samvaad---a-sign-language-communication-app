📘 **Samvaad — An App to Talk to the Hearing-Impaired**

Samvaad is a web application designed to bridge the communication gap between hearing-impaired individuals and the non-hearing-impaired community.
It converts spoken audio input into Indian Sign Language (ISL) animations, enabling intuitive and accessible communication.


🚀 **Overview**

Millions of hearing-impaired individuals face barriers due to differences in spoken and sign language.
Samvaad helps close this gap by translating speech → text → ISL gesture animations using modern web technologies and Natural Language Processing.

The system:
- Accepts recorded audio input through the browser
- Converts audio to text using the JavaScript Web Speech API
- Processes and interprets the text using NLP techniques
- Displays the corresponding ISL animation sequence
- This enables smoother communication between hearing and hearing-impaired individuals in multilingual environments.


✨ **Key Features**

🎤 Speech-to-Text Conversion
Converts spoken sentences into text using the JavaScript Web Speech API.

🧠 Natural Language Processing (NLP)
Interprets and transforms the transcribed text into an ISL-friendly phrase.

🖐 ISL Gesture Animation Rendering
Displays animated ISL gestures based on the system-generated phrase.

💻 Web-Based and Lightweight
Fully browser-based, no installations needed.

🌍 Bridges Communication Barriers
Helps simplify interactions with the hearing-impaired community.


🛠 **Tech Stack**
Component	Technology
Speech Recognition	          ->           JavaScript Web Speech API
NLP	                          ->           Custom text-processing logic
Animation Rendering	          ->           Web-based ISL models & animations
Frontend	                    ->           HTML, CSS, JavaScript


▶️ **How It Works**

- User clicks Start and speaks into the microphone
- The system captures and converts the audio to text
- NLP module generates the nearest matching ISL phrase
- The app renders the corresponding ISL animations to the user
