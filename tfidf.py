import requests, json
from sklearn.feature_extraction.text import TfidfVectorizer

dataset = [
    {"title": "Interstellar", "description": "A sci-fi film about love and space exploration.", "genre": "Sci-Fi, Drama"},
    {"title": "Inception", "description": "A mind-bending heist through shared dreams.", "genre": "Sci-Fi, Thriller"},
    {"title": "The Shawshank Redemption", "description": "Two imprisoned men bond over years, finding hope.", "genre": "Drama"},
    {"title": "The Dark Knight", "description": "A vigilante faces moral choices in a city of chaos.", "genre": "Action, Crime, Drama"}
]

#This is addedin the case of personalised movie recommendation system
vectorizer = TfidfVectorizer()
vectorizer.fit([json.dumps(dataset)])

base_prompt = f"""
You are a movie recommendation assistant.
Use only the dataset below to suggest movies.
{dataset}
Based on the user's preference, recommend 2-3 movies and explain briefly.
"""

def ask_ollama(prompt):
    r = requests.post("http://localhost:11434/api/generate",json={"model": "dolphin-phi:latest", "prompt": prompt, "stream": False})
    return r.json()["response"]

def recommend():
    prefix = base_prompt + "\nUser preference: "
    while True:
        q = input("You: ")
        if q.lower() == "exit":
            break

#This is addedin the case of personalised movie recommendation system
        vectorizer.transform([q])
        print("Bot:", ask_ollama(prefix + q), "\n")

recommend()
