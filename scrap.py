import requests
import os
from bs4 import BeautifulSoup

def clear():
    if os.name == 'nt': 
        os.system('cls')
    else:
        os.system('clear')

def search_movies():
    url = "http://localhost:8000/genres/"
    response = requests.get(url)
    
    if response.status_code == 200:
        generos = response.json()
        genero_dict = {i+1: genero for i, genero in enumerate(generos)}
        genero_str = "\n".join(f"{num}. {genero['GenreName']}" for num, genero in genero_dict.items())
        print(f"Agora, qual o gênero de filme que você quer assistir? Escolha um número:\n{genero_str}")
        gen = int(input())            
        if gen not in genero_dict:
            print("Número de gênero inválido. Tente novamente.")
            exit()
        genre = genero_dict[gen]['GenreName']
        
    search_url = f"https://www.google.com/search?q=filmes+de+{genre}"
    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        with open("soup.txt", "w", encoding='utf-8') as arquivo:
            arquivo.write(str(soup))
        with open("soup.txt", "r", encoding='utf-8') as arquivo:
            soup_content = arquivo.read()
            soup = BeautifulSoup(soup_content, "html.parser")
        movie_titles = []
        for movie_div in soup.find_all("div", class_="RWuggc kCrYT"):
            title_div = movie_div.find("div", class_="BNeawe s3v9rd AP7Wnd")
            year_div = movie_div.find("div", class_="BNeawe tAd8D AP7Wnd")

            if title_div and year_div:
                if "..." not in title_div.text.strip():
                    title = title_div.text.strip()
                    year = year_div.text.strip()
                    full_movie_title = f"{title} ({year})"
                    movie_titles.append(full_movie_title)
        clear()       
        print("Top 10 Filmes:")
        for i, title in enumerate(movie_titles[:10]):
            print(f"{i+1}. {title}")

if __name__ == "__main__":
    genre = input("Escreva o gênero que você quer assistir: ")
    search_movies()
