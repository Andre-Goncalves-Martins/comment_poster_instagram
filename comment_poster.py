from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep
from tqdm import tqdm
from random import randint
from flask import Flask, request
import smtplib
import ssl

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    # Receber o arquivo CSV
    csv_file = request.files['csv_file']
    # Receber o email
    email = request.form['email']
    # Receber a senha
    senha = request.form['senha']
    # Receber o comentário
    comentario = request.form['comentario']
    if '@' not in email:
        return 'Invalid Email'
    if len(senha) < 8:
        return 'Invalid password'
    if len(comentario) == 0:
        return 'Invalid comment'
    if 'USER' not in csv_file.columns:
        return 'CSV file need have a column named "USER"'
    else:
        return "Infos recieved!"
    
def instagram(navegador, email, senha):
    navegador.get('https://www.instagram.com/')
    sleep(0.5)
    navegador.find_element(By.NAME,'username').send_keys(email)
    navegador.find_element(By.NAME,'password').send_keys(senha)
    navegador.find_element(By.NAME,'password').send_keys(Keys.ENTER)
    sleep(1)
   
def bot_commenter(users, email, senha, comment):
    # setting up to run in the background
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    navegador = webdriver.Chrome(options=options)
    instagram(navegador, email, senha)
    sleep(10)
    try:
        navegador.find_element(by=By.CLASS_NAME, value="_a9--._a9_1").click()
    except:
        print('Não retirou a opção de não ativar as notificações')
        pass
    sleep(1)

    all_rigth = False
    for user in tqdm(users.USER):
        print(user)
        search = navegador.find_elements(by=By.CLASS_NAME, value='_ab6-')[1] # element of search
        search.click()
        sleep(1)
        # search user
        navegador.find_element(by=By.CLASS_NAME, value='_aauy').send_keys(user) 
        sleep(1)
        
        # accessing the profile of the found user
        work = True
        count = 0 
        while work and count < 10:
            try:
                navegador.find_element(by=By.CLASS_NAME, value="x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x6s0dn4 xozqiw3 x1q0g3np".replace(' ','.')).click()
                work=False
            except:
                count +=1
                sleep(0.5)
                print('erro primeiro loop')
        sleep(5)
        
        # click on last post
        navegador.find_element(by=By.CLASS_NAME, value="_aagw").click() 
        sleep(5)
        
        # make the comment
        work = True
        count = 0 
        while work and count < 10:
            try: 
                navegador.find_element(by=By.CLASS_NAME, value="x1i0vuye xvbhtw8 x76ihet xwmqs3e x112ta8 xxxdfa6 x5n08af x78zum5 x1iyjqo2 x1qlqyl8 x1d6elog xlk1fp6 x1a2a7pz xexx8yu x4uap5 x18d9i69 xkhd6sd xtt52l0 xnalus7 x1bq4at4 xaqnwrm xs3hnx8".replace(' ','.')).send_keys(f'@{user} '+comment)
                work = False
            except:
                count += 1
                sleep(0.5)
                print(count, end=', ')
        if work:
            print(f'Erro in user {user}!')
            break
        sleep(1)
        
        # Sending the comment        
        navegador.find_element(by=By.CLASS_NAME, value="x1i0vuye xvbhtw8 x76ihet xwmqs3e x112ta8 xxxdfa6 x5n08af x78zum5 x1iyjqo2 x1qlqyl8 x1d6elog xlk1fp6 x1a2a7pz xexx8yu x4uap5 x18d9i69 xkhd6sd xtt52l0 xnalus7 x1bq4at4 xaqnwrm xs3hnx8".replace(' ','.')).send_keys(Keys.ENTER)
        sleep(2)
        
        # exit post
        navegador.find_element(by=By.CLASS_NAME, value='x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 x78zum5 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha'.replace(' ','.')).click()
        sleep(.5)
        
        # go back to home
        navegador.find_elements(by=By.CLASS_NAME, value='_ab6-')[0].click()
        
        # Wait at least 5 minutes to continue
        sleep(60*randint(5, 15))
        print(f'end {user}')
    all_rigth = True
    return all_rigth


def send_email(email):
    # Atividade do Email
    assunto = 'Automation of comments on Instagram'
    corpo = 'Hello! \nAll the users requests receive a comment as you defined!'

    smtp_server = "smtp.gmail.com" ## Usando o gmail
    port = 587  # Porta para TLS
    sender_email = ""  # Email do remetente ####################### coloque o seu
    receiver_email = email # Email do destinatário
    password = "" # Senha de aplicativo gerada pelo Gmail ######### sua senha de app
    message = f"""\
    Subject: {assunto}

    {corpo}."""

    # Cria uma conexão segura com o servidor SMTP do Gmail usando TLS
    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    print("E-mail enviado com sucesso!")
    

if __name__ == '__main__':
    
    users = pd.read_csv('usernames.csv')
    comment = 'Amazing!'
    email = '' # email para logar na conta do instagram
    senha = '' # senha da conta da instagram
    
    # upload() A ideia é receber as entradas necessárias de um frontend
    certo = bot_commenter(users, email, senha, comment)
    if certo:
        send_email(email)