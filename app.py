from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from ai import ask_ai
from notion_reader import get_pages_and_summaries

app = FastAPI()

# Página HTML com formulário
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head><title>Notion AI Bot</title></head>
        <body>
            <h1>Faça sua pergunta</h1>
            <form action="/ask" method="post">
                <input type="text" name="question" placeholder="Digite sua pergunta" size="50"/>
                <input type="submit" value="Perguntar"/>
            </form>
        </body>
    </html>
    """

# Endpoint que processa a pergunta
@app.post("/ask", response_class=HTMLResponse)
def ask(question: str = Form(...)):
    pages = get_pages_and_summaries()
    summaries = [p["summary"] for p in pages]
    answer = ask_ai(question=question, summaries=summaries)
    return f"""
    <html>
        <body>
            <h2>Pergunta:</h2>
            <p>{question}</p>
            <h2>Resposta:</h2>
            <p>{answer}</p>
            <a href="/">Fazer outra pergunta</a>
        </body>
    </html>
    """
