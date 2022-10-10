from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import nltk
from textblob import TextBlob
from newspaper import Article
import uvicorn

nltk.download('punkt')

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request:Request):    
    return templates.TemplateResponse("index.html", {"request":request})


@app.post("/predict", response_class=HTMLResponse)
async def form_input(request:Request, URL: str = Form(...)):
    article = Article(URL)
    article.download()
    article.parse()
    article.nlp()
    Title = (f'Title: {article.title}')
    Authors = (f'Authors: {article.authors}')
    Publication_Date = (f'Publication Date: {article.publish_date}')
    Summary = (f'Summary: {article.summary}')
    return templates.TemplateResponse("index.html",
    {"request":request,
    "Title": Title,
    "Authors": Authors,
    "Publication_Date": Publication_Date,
    "Summary": Summary})


if __name__ == "__main__":
    uvicorn.run(app)



# python -m flask run
# uvicorn app:app --reload 





