from requests import post  
from scrap import search_movies

def signup():
    generos = {
        1: "Ação",
        2: "Aventura",
        3: "Comédia",
        4: "Comédia Romântica",
        5: "Documentário",
        6: "Faroeste",
        7: "Ficção Científica",
        8: "Guerra",
        9: "Musical",
        10: "Romance",
        11: "Suspense",
        12: "Terror",
        "":""
    }
    """ 
    
    """
    print("Vamos criar seu usuário!")
    newEmail = input("Insira um E-mail válido: ")
    newPassword = input("Insira sua senha: ")
    confirmPassword = input("Confirme sua senha: ")
   
    while newPassword != confirmPassword:
        newPassword = input("Insira sua senha: ")
        confirmPassword = input("Confirme sua senha: ")
        print("Senhas não coincidem. Vamos tentar novamente!")
    # url = "http://localhost:8000/users/"  
    # data = {"email": newEmail, "password": newPassword}
    # response = post(url, json=data)
    # if response.status_code == 201:
    print(newEmail, newPassword, confirmPassword)
    print("Legal! Você criou seu usuário.")
    gen = int(input("Agora, qual o gênero de filme que você quer assistir? Escolha um número: \n" +
                    "\n".join(f"{num} {genero} " for num, genero in generos.items())))
    if gen not in generos:
        print("Número de gênero inválido. Tente novamente.")
        exit()
    genre = generos[gen]

    print(genre)
    search_movies(genre)
    # else:
    #     print(f"Erro ao criar usuário: {response.text}")
if __name__ == "__main__":
    signup()
