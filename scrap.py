import requests
import os
import time
import json
from bs4 import BeautifulSoup

def clear():
    if os.name == 'nt': 
        os.system('cls')
    else:
        os.system('clear')

def recap(aprox_movie):
    print("Certo. Pesquisando...")
    time.sleep(1)
    clear()
    search_url = f"https://www.google.com/search?q=filmes+similares+{aprox_movie}"
    response = requests.get(search_url)
    if response.status_code == 200:
        soup_recap = BeautifulSoup(response.content, "html.parser")
    with open("soup_recap.txt", "w", encoding='utf-8') as arquivo:
        arquivo.write(str(soup_recap))
    with open("soup_recap.txt", "r", encoding='utf-8') as arquivo:
        soup_content = arquivo.read()
        soup_recap = BeautifulSoup(soup_content, "html.parser")
    movie_titles_recap = []
    for movie_div in soup_recap.find_all("div", class_="RWuggc kCrYT"):
        title_div = movie_div.find("div", class_="BNeawe s3v9rd AP7Wnd")
        year_div = movie_div.find("div", class_="BNeawe tAd8D AP7Wnd")
        if title_div and year_div:
            if "..." not in title_div.text.strip():
                title = title_div.text.strip()
                year = year_div.text.strip()
                full_movie_title = f"{title} ({year})"
                movie_titles_recap.append(full_movie_title)
    clear()       
    print("Top 10 Filmes:")
    for i, title in enumerate(movie_titles_recap[:10]):
        print(f"{i+1}. {title}")
    print("\nE aí, gostou de algum filme? Se sim, digite <S>im, se não gostou, digite <N>ão.")
    boolValid = input()
    while boolValid not in ['s','S','n','N']:
        boolValid = input("Insira um valor válido!\n")
    if boolValid in ['S', 's']:
        movie_number = input("Que ótimo! Digite o número do filme que você gostou: ")
        while not movie_number.isdigit() or int(movie_number) < 1 or int(movie_number) > 10:
            movie_number = input("Número inválido! Digite um número entre 1 e 10: ")
        movie_index = int(movie_number) - 1
        print(f"Você escolheu: {movie_titles_recap[movie_index]}.\nAproveite seu filme!")
        return
    else:
        movie_number = input("Que pena! Pode nos informar qual filme chegou mais próximo do seu gosto? Digite aqui: ")
        while not movie_number.isdigit() or int(movie_number) < 1 or int(movie_number) > 10:
            movie_number = input("Número inválido! Digite um número entre 1 e 10: ")
        movie_index = int(movie_number) - 1
        aprox_movie = movie_titles_recap[movie_index]
        while not movie_number.isdigit() or int(movie_number) < 1 or int(movie_number) > 10:
            movie_number = input("Número inválido! Digite um número entre 1 e 10: ")
        movie_index = int(movie_number) - 1
        aprox_movie = movie_titles_recap[movie_index]
        bool_recap = input(f"certo, o mais próximo do que você esperava é: {aprox_movie}."
              +"\nQuer pesquisar de forma mais apurada, com base nele?\n")
        while bool_recap not in ['s','S','n','N']:
            bool_recap = input("Insira um valor válido!\n")

        if bool_recap in ['S', 's']:
            recap(aprox_movie)

def search_movies(iduser):
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

        data = {
            "IDUser": iduser, 
            "IDGenre": genero_dict[gen]['IDGenre'], 
            "GenreName": genero_dict[gen]['GenreName']}
        response = requests.post("http://localhost:8000/search/", json=data)
         
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
                    full_movie_title = f"{title} - ({year})"
                    movie_titles.append(full_movie_title)
        clear()       
        print("Top 10 Filmes:")
        for i, title in enumerate(movie_titles[:10]):
            print(f"{i+1}. {title}")
        print("\nE aí, gostou de algum filme? Se sim, digite <S>im, se não gostou, digite <N>ão.")
        boolValid = input()
        while boolValid not in ['s','S','n','N']:
            boolValid = input("Insira um valor válido!\n")
    
        if boolValid in ['S', 's']:
            movie_number = input("Que ótimo! Digite o número do filme que você gostou: ")
            while not movie_number.isdigit() or int(movie_number) < 1 or int(movie_number) > 10:
                movie_number = input("Número inválido! Digite um número entre 1 e 10: ")
            movie_index = int(movie_number) - 1
            data = {
                "IDUser":iduser,
                "IDGenre": genero_dict[gen]['IDGenre'],
                "GenreName": genero_dict[gen]['GenreName'],
                "MovieName": movie_titles[movie_index]}
            requests.post("http://localhost:8000/choose/", json=data)

            print(f"Você escolheu: {movie_titles[movie_index]}.\nAproveite seu filme!")
            return
        else:
            movie_number = input("Que pena! Pode nos informar qual filme chegou mais próximo do seu gosto? Digite aqui: ")
            while not movie_number.isdigit() or int(movie_number) < 1 or int(movie_number) > 10:
                movie_number = input("Número inválido! Digite um número entre 1 e 10: ")
            movie_index = int(movie_number) - 1
            aprox_movie = movie_titles[movie_index]
            bool_recap = input(f"certo, o mais próximo do que você esperava é: {aprox_movie}."
                  +"\nQuer pesquisar de forma mais apurada, com base nele?\n")
            print(bool_recap)
            while bool_recap not in ['s','S','n','N']:
                bool_recap = input("Insira um valor válido!\n")

            if bool_recap in ['S', 's']:
                recap(aprox_movie)

def find_by_preference(iduser,nameuser):
    requests.get("http://localhost:8000/choose/")
    print(f"Certo, {nameuser}. Iremos pesquisar por filmes com:")


if __name__ == "__main__":
    genre = input("Escreva o gênero que você quer assistir: ")
    search_movies()