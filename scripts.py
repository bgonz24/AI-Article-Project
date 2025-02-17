import os
from dotenv import load_dotenv
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from newsapi import NewsApiClient
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")

llm = OpenAI(openai_api_key = openai_api_key)
embeddings = OpenAIEmbeddings(model= "text-embedding-3-large", openai_api_key = openai_api_key)
newsapi = NewsApiClient(api_key = news_api_key)

# Summarises the input text in one sentence
def summarise_text(text):
    summarise_template = PromptTemplate.from_template("Summarise the following text in one sentence: {text}")
    summarise_runnable = summarise_template | llm
    return summarise_runnable.invoke({"text": text})

# Summarises the linked article in one sentence
def summarise_article(link):
    summarise_template = PromptTemplate.from_template("Summarise the linked article in one sentence: {link}")
    summarise_runnable = summarise_template | llm
    return summarise_runnable.invoke({"link": link})

# Extracts the main topic of the news article in 3 words or less
def extract_news_topic(text):
    prompt = PromptTemplate.from_template("From the following summary of a news article, extract the main topic of the article in 3 words or less: {text}")
    extract_runnable = prompt | llm
    return extract_runnable.invoke({"text": text})

# Creates a list embedding from the input text
def embed_text(text):
    return embeddings.embed_query(text)

# Uses the cosine similarity to calculate the similarity between two embeddings between -1 and 1
def calculate_similarity(embedding1, embedding2):
    array1 = np.asarray(embedding1).reshape(1, -1)
    array2 = np.asarray(embedding2).reshape(1, -1)
    return cosine_similarity(array1, array2)[0][0]

# Gets the top headlines from the News API
def get_news():
    top_headlines = newsapi.get_top_headlines(category = "science", language = "en")
    return top_headlines

# Gets the top 10 news articles, summarises them, and embeds them
def generate_news_embeddings(article_count):
    news = get_news()
    embedding_list = []

    for i in range(article_count):
        summary = summarise_article(news["articles"][i]["url"])
        #topic = extract_news_topic(summary)
        article_embedding = embed_text(summary)
        embedding_list.append(article_embedding)
    return embedding_list

# Gets the slugs for all J-stories articles and saves them to a file
def get_article_slugs(docs):
    article_list = open("article_list.txt", "w")
#Gets all J-stories slugs from the Firestore database and saves only the text articles to a file
    for doc in docs:
    #Checks if the article is in English and not a video or a test page
        if doc.to_dict().get("en") != None:
            if doc.to_dict().get("en").get("category") != None and doc.to_dict().get("en").get("category") != "video":
            #Writes the slug to article_list.txt
                article_list.write(doc.to_dict().get("slug") + "\n")
    article_list.close()
    return article_list