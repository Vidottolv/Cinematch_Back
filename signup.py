import requests
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
        12: "Terror\n",
    }
    """ 
    
    """
    boolValid = input("\nBem-Vindo ao Cinematch! "
                        +"\n\nJá tem conta?"
                        +"\n<S>im - - <N>ão\n")
    while boolValid not in ['s','S','n','N']:
        boolValid = input("Insira um valor válido!\n")
    
    if boolValid == 'S' or boolValid == 's':
        email_login = input("Insira seu email: ")
        password_login = input("Insira sua senha: ")

        url = f"http://localhost:8000/users/{email_login}"
        data = {"Email": email_login, "Password": password_login}
        response = requests.get(url, json=data)

        if response.status_code == 200:
            print("Login realizado com sucesso")
            print(response.json())  
        elif response.status_code == 401:
            print("Senha incorreta")
        elif response.status_code == 404:
            print("Usuário não encontrado")
        else:
            print(f"Erro ao realizar login: {response.status_code}")

        return
    
    else:
        print("Vamos criar seu usuário!")
        newEmail = input("Insira um E-mail válido: ")
        newPassword = input("Insira sua senha: ")
        confirmPassword = input("Confirme sua senha: ")
    
        while newPassword != confirmPassword:
            newPassword = input("Insira sua senha: ")
            confirmPassword = input("Confirme sua senha: ")
            
            print("Senhas não coincidem. Vamos tentar novamente!")
        
        url = "http://localhost:8000/users/"  
        data = {"Email": newEmail, "Password": newPassword}
        response = requests.post(url, json=data)
        
        print(data)
        
        if response.status_code == 201:
            
            print(newEmail, newPassword, confirmPassword)
            print("Legal! Você criou seu usuário.")
            
            gen = int(input("Agora, qual o gênero de filme que você quer assistir? Escolha um número: \n" +
                            "\n".join(f"{num} {genero} " for num, genero in generos.items())))
            
            if gen not in generos:
                print("Número de gênero inválido. Tente novamente.")
                exit()
            
            genre = generos[gen]
        
        else:
            print(f"Erro ao criar usuário: {response.text}")

            return
    
    print(genre)
    search_movies(genre)
    
if __name__ == "__main__":
    signup()
