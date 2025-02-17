import os
from dotenv import load_dotenv
from scripts import *
from langchain_openai import OpenAI, OpenAIEmbeddings
from newsapi import NewsApiClient

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")

llm = OpenAI(openai_api_key = openai_api_key)
embeddings = OpenAIEmbeddings(model= "text-embedding-3-large", openai_api_key=openai_api_key)
newsapi = NewsApiClient(api_key = news_api_key)

article_count = 10
news_embeddings = []
news_similarities = [0] * article_count
jstories_similarities = [0] * article_count
news_embeddings = generate_news_embeddings(article_count)
headlines = get_news()

#Opens the input files and saves all J-stories article slugs into a list
jstories_embeddings = []
file = open("jstories_embeddings.txt", "r")
jstories_article_file = open("article_list.txt", "r")
jstories_articles = jstories_article_file.readlines()

#Processes the embeddings from the file into a list of embeddings
raw_embeddings = file.readlines()
for i in range(len(raw_embeddings)):
    jstories_embeddings.append(raw_embeddings[i].strip().split(','))

#Calculates the similarity between each news article and each J-stories article
for i in range(article_count):
    for j in range(len(jstories_embeddings)):
        similarity = calculate_similarity(news_embeddings[i], jstories_embeddings[j])
        #If the similarity is greater than the current similarity, update the saved similarity and the J-stories article slug
        if similarity > news_similarities[i]:
            news_similarities[i] = similarity
            jstories_similarities[i] = jstories_articles[j]

#Prints the results
for i in range(article_count):
    if news_similarities[i] > 0.35:
        print(f"{headlines['articles'][i]['title']} has a similar article in J-stories with a similarity of {news_similarities[i]}")
        print(f"J-stories article: {jstories_similarities[i]}")


file.close()
jstories_article_file.close()