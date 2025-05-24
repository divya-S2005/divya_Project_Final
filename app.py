from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import random

app = Flask(_name_)

# Load chatbot model
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

# Offensive words filter
offensive_words = ["stupid", "idiot", "hate", "kill", "suicide"]

# Empathetic replies
empathetic_replies = [
    "I'm really sorry you're feeling this way.",
    "You're not alone — I'm here to listen.",
    "That sounds tough. Want to talk more about it?",
    "I'm here for you, no judgment at all."
]

# POST endpoint for chatbot
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')  # get message from JSON

    # Check for offensive words
    if any(bad in user_input.lower() for bad in offensive_words):
        return jsonify({"response": "Let's keep our conversation respectful and safe. I'm here to help you."})
    
    # Generate a response from the model
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    output_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    reply = tokenizer.decode(output_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Add empathy
    empathetic_prefix = random.choice(empathetic_replies)
    full_response = f"{empathetic_prefix} {reply}"

    return jsonify({"response": full_response})

# Home route
@app.route('/')
def home():
    return "Mental Health Chatbot API is running!"

if _name_ == '_main_':
    app.run(host="127.0.0.1",port=8000,debug=True)