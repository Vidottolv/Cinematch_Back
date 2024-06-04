import requests
import getpass
import json
import os
import time
from scrap import search_movies
from quiz import quiz

current_id_user = None

def clear():
    if os.name == 'nt': 
        os.system('cls')
    else:
        os.system('clear')

def signup():
    # quiz()
    # current_id_user = None 
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
            print(current_id_user)    
            time.sleep(0.5)
            # clear()
            search_movies()                      
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
        
        url = "http://localhost:8000/create_user/"  
        data = {
            "Email": newEmail,
            "Username": newUsername,
            "Password": newPassword}
        response = requests.post(url, json=data)
        print('🚀 ~ ', response)
        print(data)
        
        if response.status_code == 201:
            print(newEmail, newPassword, confirmPassword)
            print("Legal! Você criou seu usuário.")
            quiz()        
        else:
            print(f"Erro ao criar usuário: {response.text}")
            return
        
if __name__ == "__main__":
    signup()
