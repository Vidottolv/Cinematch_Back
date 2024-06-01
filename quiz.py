import requests
import json

respostas = []

def get_pergunta_1():
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
                    respostas.append(genre_choosed)
                    return 
                else:
                    print("Número de gênero inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número")            
    else:
        print(f"Erro ao buscar opções: {response.status_code}")
        exit()

def get_pergunta_2():
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
                    respostas.append(storytype_choosed)
                    return
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número")            
    else:
        print(f"Erro ao buscar opções: {response.status_code}")
        exit()
    
def get_pergunta_3():
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
                    respostas.append(agemovie_choosed)
                    return
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número")            
    else:
        print(f"Erro ao buscar opções: {response.status_code}")
        exit()       

def get_pergunta_4():
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
                    respostas.append(endmovie_choosed)
                    return
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número")            
    else:
        print(f"Erro ao buscar opções: {response.status_code}")
        exit()   

def get_pergunta_5():
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
                    respostas.append(kindmovie_choosed)
                    return
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número")            
    else:
        print(f"Erro ao buscar opções: {response.status_code}")
        exit()  
        
def quiz():
    print("Bora começar seu Quiz? Ele é importante para podermos melhorar as buscas por sua preferência.")
    get_pergunta_1()
    get_pergunta_2()
    get_pergunta_3()
    get_pergunta_4()
    get_pergunta_5()
    response = requests.get("http://localhost:8000/users/me")
    if response.status_code == 200:
        iduser = response.json()
        respostas.append(iduser)

    respostas_json = json.dumps(respostas)
    print(respostas_json)
    response = requests.post("http://localhost:8000/preferences/", json=respostas_json)
   
    if response.status_code == 201:
        print("Preferências salvas com sucesso!")
    else:
        print(f"Erro ao salvar preferências: {response}")

if __name__ == "__main__":
    quiz()
