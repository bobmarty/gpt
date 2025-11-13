import requests, gradio as gr
from PyPDF2 import PdfReader
from docx import Document

def read_file(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file.name)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    elif file.name.endswith(".docx"):
        doc = Document(file.name)
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        return file.read().decode("utf-8")

def ask_ollama(prompt):
    r = requests.post("http://localhost:11434/api/generate",json={"model": "dolphin-phi:latest", "prompt": prompt, "stream": False})
    d=r.json()
    return d.get("response",d)

def answer_question(file, question):
    if not file or not question:
        return "Please upload a file and enter a question."
    text = read_file(file)
    prompt = f"You are an expert document analyst.\nDocument:\n{text}\n\nQuestion: {question}\nAnswer clearly."
    res=ask_ollama(prompt)
    print(res)
    return res


iface = gr.Interface(
    fn=answer_question,
    inputs=[gr.File(label="Upload File"), gr.Textbox(label="Your Question")],
    outputs="text",
    title="File Q&A"
)
iface.launch()
