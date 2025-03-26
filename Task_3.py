import requests
import csv
from prefect import task, flow


@task
def fetch_anime_data(query="Attack on Titan"):
    url = f"https://api.jikan.moe/v4/anime?q={query}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")



@task
def save_to_csv(anime_data):
    with open('anime_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Score', 'Episodes', 'URL'])
        for anime in anime_data:
            title = anime['title']
            score = anime['score']
            episodes = anime.get('episodes', 'N/A')
            url = anime['url']
            writer.writerow([title, score, episodes, url])



@flow
def scrape_and_save_anime_data(query="Attack on Titan"):
    anime_data = fetch_anime_data(query=query)
    save_to_csv(anime_data)



if __name__ == '__main__':
    scrape_and_save_anime_data("Naruto")

