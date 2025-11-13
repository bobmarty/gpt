import requests
import gradio as gr

dataset = [
    {"question": "How can I track my order?", "answer": "You can track your order by logging into your account and clicking on 'Track Order'."},
    {"question": "What is the return policy?", "answer": "You can return most items within 30 days of delivery for a full refund."},
    {"question": "Do you ship internationally?", "answer": "Yes, we ship to over 100 countries worldwide."},
    {"question": "What payment methods are accepted?", "answer": "We accept credit cards, debit cards, PayPal, and UPI."},
    {"question": "How do I cancel my order?", "answer": "You can cancel your order before it is shipped from your 'My Orders' page."}
]

base_prompt = f"""
You are an expert E-Commerce chatbot.
Answer based on the questions and answers available in this dataset and construct the answer in a good way:

{dataset}

If the answer is not found, say "I'm not very sure." and give an appropriate answer based on the data provided and your own knowledge.
Do not mention the dataset to the customer, only give the customer what he needs to know and nothing more.
"""

def ask_ollama(prompt):
    r = requests.post("http://localhost:11434/api/generate",json={"model": "dolphin-phi:latest", "prompt": prompt, "stream": False})
    return r.json().get("response")

def chat(user_input):
    prompt = base_prompt + "\nUser question: " + user_input
    return ask_ollama(prompt)

iface = gr.Interface(fn=chat, inputs="text", outputs="text", title="E-Commerce Chatbot")
iface.launch()