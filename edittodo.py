import sys
import tkinter as tk
from tkinter import messagebox as msbox, messagebox
import requests
import json
import os
from dotenv import load_dotenv
import subprocess




load_dotenv()






def setInfo():   #정보 가져오기
    global user_id
    global name
    opInfo = open('info.txt')
    readInfo = opInfo.readlines()[0].split()
    user_id = int(readInfo[0])
    name = readInfo[1]

setInfo()

def editTodo():
    id = user_id
    title = iprTit.get()
    content = iprCo.get("1.0", "end-1c")
    if title == "" or content == "":
        messagebox.showinfo("Error", "제목과 글은 한글자 이상씩 작성하여 주세요.")
    else :
        sendingData = {"author_id": id,"title": title,"content": content,"completed": 0}
        headers = {"Content-Type": "application/json"}
        json_data = json.dumps(sendingData)
        intodo = requests.post(f'{os.environ.get('API_KEY')}/write', data=json_data, headers=headers)
        editPg.quit()




editPg = tk.Tk()
editPg.title("글쓰기")
editPg.geometry("200x150+750+400")
editPg.resizable(width=False, height=False)




seeTit=tk.Label(editPg, text="제목을 입력하세요.", fg="white",relief="solid")    #name 입력 안내 텍스트
seeTit.place(x=0, y=0, relwidth=1, )
iprTit = tk.Entry(editPg)                                                     #name 입력창
iprTit.place(x=0, y=20, relwidth=1,)


seeCo=tk.Label(editPg, text="글 내용을 입력하세요.", fg="white",relief="solid")  #passward 입력 안내 텍스트
seeCo.place(x=0, y=40, relwidth=1,)
iprCo = tk.Text(editPg)           #passward 입력창
iprCo.place(x=0, y=60, relwidth=1,relheight=0.4)


editEnt = tk.Button(editPg, text="확인",command=editTodo)  #로그인 버튼 생성
editEnt.place(x=0, y=120, relwidth=1,)


editPg.mainloop()
