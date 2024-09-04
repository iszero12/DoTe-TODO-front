import tkinter as tk
from tkinter import messagebox as msbox
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def signup() :
    name = iprName1.get()
    pw = iprPw1.get()
    sendingData = {'name': name, 'password': pw}
    headers = {"Content-Type": "application/json"}
    json_data = json.dumps(sendingData)

    createUser = requests.post(f'{os.environ.get('API_KEY')}/signup/', data=json_data, headers=headers)
    userinfo = str(createUser)
    if (userinfo.split('[')[1].split(']')[0] == '422'):
        print('error')
    if (userinfo.split('[')[1].split(']')[0] == '200'):
        msbox.showinfo('Success', '회원가입 성공!')
        signupScrn.destroy()


signupScrn = tk.Tk()            #로그인 화면 생성
signupScrn.title("SignUp")
signupScrn.geometry("500x300+600+100")


seeName=tk.Label(signupScrn, text="아이디를 입력하세요.", fg="white",relief="solid")    #name 입력 안내 텍스트
seeName.place(x=0, y=0, relwidth=1,)
iprName1 = tk.Entry(signupScrn)                                                     #name 입력창
iprName1.place(x=0, y=20, relwidth=1,)


seePw=tk.Label(signupScrn, text="비밀번호를 입력하세요.", fg="white",relief="solid")  #passward 입력 안내 텍스트
seePw.place(x=0, y=40, relwidth=1,)
iprPw1 = tk.Entry(signupScrn,show="*")                                           #passward 입력창
iprPw1.place(x=0, y=60, relwidth=1,)


entSignup = tk.Button(signupScrn, text="회원가입", command=signup)  #회원가입 버튼 생성
entSignup.place(x=0, y=120, relwidth=1,)


signupScrn.mainloop()