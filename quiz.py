import requests
import json
import os
import time
from scrap import find_by_preference, search_movies

def clear():
    if os.name == 'nt': 
        os.system('cls')
    else:
        os.system('clear')

def get_pergunta_1():
    global IDgenre, Gernename
    url = "http://localhost:8000/genres/"
    response = requests.get(url)
    if response.status_code == 200:
        genres = response.json()
        genre_dict = {i+1: genre for i, genre in enumerate(genres)}
        genre_str = "\n".join(f"{num}. {genre['GenreName']}" for num, genre in genre_dict.items())
        print(f"1. Qual seu gênero de filme favorito?\n{genre_str}")
        while True:
            try:
                gen = int(input())
                if gen in genre_dict:
                    genre_choosed = genre_dict[gen]
                    IDgenre = genre_choosed['IDGenre']
                    Gernename = genre_choosed['GenreName']                  
                    return 
                else:
                    print("Número de gênero inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número")            
    else:
        print(f"Erro ao buscar opções: {response.status_code}")
        exit()

def get_pergunta_2():
    global IDStorytype, Storytype
    url = "http://localhost:8000/storytype/"
    response = requests.get(url)
    if response.status_code == 200:
        storytypes = response.json()
        storytype_dict = {i+1: storytype for i, storytype in enumerate(storytypes)}
        storytype_str = "\n".join(f"{num}. {storytype['StoryType']}" for num, storytype in storytype_dict.items())
        print(f"2. Você prefere filmes que são:\n{storytype_str}")
        while True:
            try:
                storytype_number = int(input())
                if storytype_number in storytype_dict:
                    storytype_choosed = storytype_dict[storytype_number]
                    IDStorytype = storytype_choosed['IDStoryType']
                    Storytype = storytype_choosed['StoryType']    
                    return
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número")            
    else:
        print(f"Erro ao buscar opções: {response.status_code}")
        exit()
    
def get_pergunta_3():
    global IDAgemovie, Agemovie
    url = "http://localhost:8000/agemovie/"
    response = requests.get(url)
    if response.status_code == 200:
        agemovies = response.json()
        agemovie_dict = {i+1: agemovie for i, agemovie in enumerate(agemovies)}
        agemovie_str = "\n".join(f"{num}. {agemovie['AgeMovie']}" for num, agemovie in agemovie_dict.items())
        print(f"3. Qual a sua década de filmes favorita?:\n{agemovie_str}")
        while True:
            try:
                agemovie_number = int(input())
                if agemovie_number in agemovie_dict:
                    agemovie_choosed = agemovie_dict[agemovie_number]
                    IDAgemovie = agemovie_choosed['IDAgeMovie']
                    Agemovie = agemovie_choosed['AgeMovie']    
                    return
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número")            
    else:
        print(f"Erro ao buscar opções: {response.status_code}")
        exit()       

def get_pergunta_4():
    global IDendmovie, Endmovie
    url = "http://localhost:8000/endmovie/"
    response = requests.get(url)
    if response.status_code == 200:
        endmovies = response.json()
        endmovie_dict = {i+1: endmovie for i, endmovie in enumerate(endmovies)}
        endmovie_str = "\n".join(f"{num}. {endmovie['EndMovie']}" for num, endmovie in endmovie_dict.items())
        print(f"4. Você prefere assistir a filmes:\n{endmovie_str}")
        while True:
            try:
                endmovie_number = int(input())
                if endmovie_number in endmovie_dict:
                    endmovie_choosed = endmovie_dict[endmovie_number]
                    IDendmovie = endmovie_choosed['IDEndMovie']
                    Endmovie = endmovie_choosed['EndMovie']    
                    return
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número")            
    else:
        print(f"Erro ao buscar opções: {response.status_code}")
        exit()   

def get_pergunta_5():
    global IDkindmovie, Kindmovie
    url = "http://localhost:8000/kindmovie/"
    response = requests.get(url)
    if response.status_code == 200:
        kindmovies = response.json()
        kindmovie_dict = {i+1: kindmovie for i, kindmovie in enumerate(kindmovies)}
        kindmovie_str = "\n".join(f"{num}. {kindmovie['KindMovie']}" for num, kindmovie in kindmovie_dict.items())
        print(f"5. Que tipo de cenários você mais gosta em um filme?\n{kindmovie_str}")
        while True:
            try:
                kindmovie_number = int(input())
                if kindmovie_number in kindmovie_dict:
                    kindmovie_choosed = kindmovie_dict[kindmovie_number]
                    IDkindmovie = kindmovie_choosed['IDKindMovie']
                    Kindmovie = kindmovie_choosed['KindMovie']
                    return
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número")            
    else:
        print(f"Erro ao buscar opções: {response.status_code}")
        exit()  
        
def quiz(iduser,nameuser):
    print("Bora começar seu Quiz? Ele é importante para podermos melhorar as buscas por sua preferência.")
    get_pergunta_1()
    get_pergunta_2()
    get_pergunta_3()
    get_pergunta_4()
    get_pergunta_5()

    data = { 
        "IDUser": iduser,
        "IDGenre": IDgenre,
        "GenreName": Gernename,
        "IDStoryType": IDStorytype,
        "StoryType": Storytype,
        "IDAgeMovie": IDAgemovie,
        "AgeMovie": Agemovie,
        "IDEndMovie": IDendmovie,
        "EndMovie": Endmovie,
        "IDKindMovie": IDkindmovie,
        "KindMovie": Kindmovie
    }
    
    response = requests.post("http://localhost:8000/preferences/", json=data)
   
    if response.status_code == 201:
        print("Preferências salvas com sucesso!")
        time.sleep(1)
        clear()
        print(f"Bem vindo, {nameuser}.\n\n"
              +"Gostaria de pesquisar os filmes de que forma hoje?\n"
              +"1. Pesquisando através de minhas preferências.\n"
              +"2. Pesquisa por gênero.")
        kind_search = int(input())
        while kind_search not in [1,2]:
            print("Insira um valor válido.\n")
        
        if kind_search == 1:
            find_by_preference(iduser,nameuser)
        elif kind_search == 2:
            search_movies(iduser) 
    else:
        print(f"Erro ao salvar preferências: {response.status_code}")

if __name__ == "__main__":
    quiz()
