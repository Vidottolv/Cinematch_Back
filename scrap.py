import requests
from bs4 import BeautifulSoup

def get_full_movie_name(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        print(soup)
        title_div = soup.find("div", class_="LC20lb MBeuO DKV0Md")
        if title_div:
            return title_div.text.strip()
    return None

def search_movies(genre):
    search_url = f"https://www.google.com/search?q=filmes+de+{genre}"
    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        movie_titles = []
        for div in soup.find_all("div", class_="RWuggc kCrYT"):
            title_div = div.find("div", class_="BNeawe s3v9rd AP7Wnd")
            if title_div:
                movie_title = title_div.text.strip()
                movie_titles.append(movie_title)
                # if "..." in movie_title:
                #     url_name_full = f"https://www.google.com/search?q={movie_title}"
                #     if url_name_full:
                #         full_movie_name = get_full_movie_name(url_name_full)
                #         movie_titles.append(full_movie_name)
                # else:
                #     movie_titles.append(movie_title)

        print("Top 10 Filmes:")
        for i, title in enumerate(movie_titles[:10]):
            print(f"{i+1}. {title}")
    else:
        print("Error:", response.status_code)

if __name__ == "__main__":
    genre = input("Escreva o gênero que você quer assistir: ")
    search_movies(genre)
