import requests
from bs4 import BeautifulSoup

def search_movies(genre):
    """Searches for Netflix movies on the web using Google Search and displays the top 5 results.

    Args:
        genre: The movie genre to search for.

    Returns:
        None
    """
    # IMDB Url
    search_url = f"https://www.google.com/search?q={genre}+"+" movies"
    response = requests.get(search_url)
    print(response.status_code)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        arquivo = open('soup.txt','w', encoding="utf-8")
        arquivo.write(soup.prettify())
        arquivo.close()

        movie_titles = []
        for div in soup.find_all("div", class_="RWuggc kCrYT"):
            title_div = div.find("div", class_="BNeawe s3v9rd AP7Wnd")
            if title_div:
                movie_title = title_div.text.strip()
                movie_titles.append(movie_title)
        # for result in soup.find_all("div",attrs={"data-ttl": True}):
        #     movie_title = result.find("data-ttl").strip()
        #     movie_titles.append(movie_title)

        print("Top 5 movies:")
        for i, title in enumerate(movie_titles[:5]):
            print(f"{i+1}. {title}")
    else:
        print("Error:", response.status_code)

if __name__ == "__main__":
    # Get the movie genre from the user
    genre = input("Enter the movie genre you want to search for: ")

    # Search for Netflix movies in the specified genre
    search_movies(genre)
