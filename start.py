import sys
import tkinter as tk
from tkinter import messagebox as msbox
import requests
import json
import os
from dotenv import load_dotenv
import subprocess


load_dotenv()


opInfo = open('info.txt')






dummy = {'name':'abcd1234','pw':'abcd1232'}
name = ""
pw = ""



def goSignup() :
    subprocess.run(args=[sys.executable, 'signup.py'])



def saveInfo(id,name):   #정보 저장
    f = open('info.txt', 'w')
    f.write(str(id))
    f = open('info.txt', 'a')
    f.write(f" {name}")
    f.close()



def loginst():
    name = str(iprName.get())
    pw = str(iprPw.get())
    sendingData = {'name': name, 'password': pw}
    headers = {"Content-Type": "application/json"}
    json_data = json.dumps(sendingData)
    authorizeUser = requests.post(f'{os.environ.get('API_KEY')}/login/', data=json_data, headers=headers)
    chData = str(authorizeUser)
    userInfo = authorizeUser.json()
    print(userInfo)
    if (chData.split('[')[1].split(']')[0] == '401'):
        msbox.showerror('Error','아이디 또는 비밀번호를 확인하여 주세요')
    if (chData.split('[')[1].split(']')[0] == '200'):
        id = userInfo['user_id']
        saveInfo(id,name)
        login.destroy()
        import main


def beforelog() :
    if opInfo.readline() != "":
        response = msbox.askyesno("Login", "로그인한 기록이 있습니다. 이어서 로그인 하시겠습니까?")
        if response == 1:
            login.destroy()
            import main
        else :
            pass




login = tk.Tk()            #로그인 화면 생성
login.title("Login")
login.geometry("500x300+600+100")



seeName=tk.Label(login, text="아이디를 입력하세요.", fg="white",relief="solid")    #name 입력 안내 텍스트
seeName.place(x=0, y=0, relwidth=1,)
iprName = tk.Entry(login)                                                     #name 입력창
iprName.place(x=0, y=20, relwidth=1,)


seePw=tk.Label(login, text="비밀번호를 입력하세요.", fg="white",relief="solid")  #passward 입력 안내 텍스트
seePw.place(x=0, y=40, relwidth=1,)
iprPw = tk.Entry(login,show="*")                                           #passward 입력창
iprPw.place(x=0, y=60, relwidth=1,)


loginEnt = tk.Button(login, text="로그인", command=loginst)  #로그인 버튼 생성
loginEnt.place(x=0, y=80, relwidth=1,)


signupBtn = tk.Button(login, text="회원가입", command=goSignup)  #회원가입 버튼 생성
signupBtn.place(x=0, y=120, relwidth=1,)

beforelog()


login.mainloop()     #창 유지













