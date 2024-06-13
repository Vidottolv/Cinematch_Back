import requests
import getpass
import json
import os
import time
from scrap import search_movies, find_by_preference
from quiz import quiz

def clear():
    if os.name == 'nt': 
        os.system('cls')
    else:
        os.system('clear')

def signup():
    global current_id_user, current_name_user

    boolValid = input("\nBem-Vindo ao Cinematch! "
                        +"\n\nJá tem conta?"
                        +"\n<S>im - - <N>ão\n")
    while boolValid not in ['s','S','n','N']:
        boolValid = input("Insira um valor válido!\n")
    
    if boolValid == 'S' or boolValid == 's':
        clear()
        email_login = input("Insira seu email: ")
        password_login = getpass.getpass("Insira sua senha: ")
        url = f"http://localhost:8000/login_user/{email_login}"
        headers = {'Content-type': 'application/json'}
        data = {"Email": email_login, "Password": password_login}
        response = requests.post(url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            print("Login realizado com sucesso")
            response_content = response.content.decode('utf-8')  
            user_data = json.loads(response_content)     
            current_id_user = user_data['IDUser']
            current_name_user = user_data['Username']
            time.sleep(1)
            clear()
            print(f"Bem vindo de volta, {current_name_user}.\n\n"
                  +"Gostaria de pesquisar os filmes de que forma hoje?\n"
                  +"1. Pesquisando através de minhas preferências.\n"
                  +"2. Pesquisa por gênero.")
            kind_search = int(input())
            while kind_search not in [1,2]:
                print("Insira um valor válido.\n")
            
            if kind_search == 1:
                find_by_preference(current_id_user,current_name_user)

            elif kind_search == 2:
                search_movies(current_id_user)        

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
        newPassword = getpass.getpass("Insira sua senha: ")
        confirmPassword = getpass.getpass("Confirme sua senha: ")
    
        while newPassword != confirmPassword:
            newPassword = getpass.getpass("Insira sua senha: ")
            confirmPassword = getpass.getpass("Confirme sua senha: ")
            
            print("Senhas não coincidem. Vamos tentar novamente!")
        
        url = "http://localhost:8000/create_user/"  
        data = {
            "Email": newEmail,
            "Username": newUsername,
            "Password": newPassword}
        response = requests.post(url, json=data)
        
        if response.status_code == 201:
            print(newEmail, newPassword, confirmPassword)
            print("Legal! Você criou seu usuário.")
            response_content = response.content.decode('utf-8')  
            user_data = json.loads(response_content)     
            current_id_user = user_data['IDUser']
            current_name_user = user_data['Username']
            quiz(current_id_user,current_name_user)        
        else:
            print(f"Erro ao criar usuário: {response.text}")
            return
        
if __name__ == "__main__":
    signup()
