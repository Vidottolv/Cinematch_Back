import requests
import getpass
import json
from scrap import search_movies

def signup():
    boolValid = input("\nBem-Vindo ao Cinematch! "
                        +"\n\nJá tem conta?"
                        +"\n<S>im - - <N>ão\n")
    while boolValid not in ['s','S','n','N']:
        boolValid = input("Insira um valor válido!\n")
    
    if boolValid == 'S' or boolValid == 's':
        email_login = input("Insira seu email: ")
        password_login = getpass.getpass("Insira sua senha: ")
        url = f"http://localhost:8000/users/{email_login}"
        headers = {'Content-type': 'application/json'}
        data = {"Email": email_login, "Password": password_login}
        response = requests.post(url, data=json.dumps(data), headers=headers)

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
        newUsername = input("Insira seu nome: ")
        newPassword = input("Insira sua senha: ")
        confirmPassword = input("Confirme sua senha: ")
    
        while newPassword != confirmPassword:
            newPassword = input("Insira sua senha: ")
            confirmPassword = input("Confirme sua senha: ")
            
            print("Senhas não coincidem. Vamos tentar novamente!")
        
        url = "http://localhost:8000/users/"  
        data = {
            "Email": newEmail,
            "Username": newUsername,
            "Password": newPassword}
        response = requests.post(url, json=data)
        
        print(data)
        
        if response.status_code == 201:
            
            print(newEmail, newPassword, confirmPassword)
            print("Legal! Você criou seu usuário.")
            
            url = "http://localhost:8000/genres/"
            response = requests.get(url)

            if response.status_code == 200:
                generos = response.json()
                gen = int(input("Agora, qual o gênero de filme que você quer assistir? Escolha um número: \n" +
                    "\n".join(f"{num} {genero} " for num, genero in enumerate(generos, start=1))))

            
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
