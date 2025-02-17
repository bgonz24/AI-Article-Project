import os
from dotenv import load_dotenv
from langchain_openai import OpenAI, OpenAIEmbeddings
from scripts import *
import firebase_admin
from firebase_admin import firestore, credentials

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

llm = OpenAI(openai_api_key = openai_api_key)
embeddings = OpenAIEmbeddings(model= "text-embedding-3-large", openai_api_key=openai_api_key)

#Sets up firestore access
cred = credentials.Certificate(google_api_key)
app = firebase_admin.initialize_app(credential= cred)
db = firestore.client()
docs = db.collection("articles").stream()



article_list = get_article_slugs(docs)

jstories_embeddings = open("jstories_embeddings.txt", "w")
jstories_summaries = open("jstories_summaries.txt", "w")
count = 1
#Reads the slugs from article_list.txt, summarises the articles, and embeds them
for line in article_list:
    #Accesses the article from J-stories
    slug = line.strip()
    link = f"https://j-stories.com/{slug}"
    #Summarises the article and embeds it, saving to a file
    summary = summarise_article(link)
    jstories_summaries.write(summary + "\n")
    embedding = embed_text(summary)
    jstories_embeddings.write(str(embedding).strip("[]"))
    jstories_embeddings.write("\n")

    #Progress tracker
    print(f"Article {count}/131 processed")
    count += 1

#Closes the files
article_list.close()
jstories_embeddings.close()
jstories_summaries.close()