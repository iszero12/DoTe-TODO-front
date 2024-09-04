import sys
import tkinter as tk
import requests
import json
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

def roadInfo():
    global id
    global name
    with open("info.txt") as f:
        info = f.read().split()
        id = info[0]
        name = info[1]

roadInfo()
print(id)

def roadTodo():
    global data
    headers = {"Content-Type": "application/json"}
    getTodoList = requests.get(f'{os.environ.get("API_KEY")}/getTodo/{id}', headers=headers)
    data = getTodoList.json()

roadTodo()




# 버튼 클릭 시 호출되는 함수
def editTodo():
    subprocess.run(args=[sys.executable, 'edittodo.py'])
    roadTodo()
    display_data()

def display_data():
    # 캔버스에 있는 모든 요소 제거
    for widget in frame_container.winfo_children():
        widget.destroy()

    if data == {"detail": "해당 사용자의 할 일이 없습니다"}:
        no_data_label = tk.Label(frame_container, text="투두가 없습니다", font=("Helvetica", 16))
        no_data_label.pack(pady=20)
    else:
        # 모든 프레임들을 캔버스에 추가
        for idx, item in enumerate(data):
            frame = tk.Frame(frame_container, width=480, height=120, highlightbackground="black", highlightthickness=1)
            frame.pack_propagate(False)  # 프레임이 자식 위젯에 맞춰 크기를 변경하지 않도록 설정

            # 체크박스 상태 업데이트 함수
            def update_comp(index):
                id = data[index]['id']
                sendingData = {'id': id}
                headers = {"Content-Type": "application/json"}
                json_data = json.dumps(sendingData)
                changeComp = requests.patch(f'{os.environ.get("API_KEY")}/updateState/{id}', data=json_data, headers=headers)
                roadTodo()
                display_data()

            def delTodo(index):
                id = data[index]['id']
                headers = {"Content-Type": "application/json"}
                delTodoList = requests.delete(f'{os.environ.get("API_KEY")}/deleteTodo/{id}', headers=headers)
                roadTodo()
                display_data()

            # 체크박스 생성
            status_label = tk.Label(frame, text=f"Status: {item['completed']}", font=("Helvetica", 12))

            # 상태변경 버튼
            checkButton = tk.Button(
                frame,
                command=lambda index=idx: update_comp(index),
                text="완료" if item['completed'] else "미완료",
                fg="green" if item['completed'] else "red"
            )

            # 지우기 버튼
            delButton = tk.Button(frame, command=lambda index=idx: delTodo(index), text="삭제")

            # 각 요소에 글 번호, 제목, 내용, 글 상태 라벨 생성
            title_label = tk.Label(frame, text=item["title"], font=("Helvetica", 16, "bold"))
            content_label = tk.Label(frame, text=item["content"], font=("Helvetica", 12))

            # 위젯들을 프레임에 추가
            checkButton.pack(side=tk.LEFT, padx=5)
            delButton.pack(side=tk.LEFT, padx=5)
            title_label.pack(side=tk.TOP, anchor="center")
            content_label.pack(side=tk.TOP, anchor="center")

            # 프레임을 캔버스에 추가
            frame.pack(pady=10)

    # 캔버스의 스크롤 영역 설정
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# tkinter 윈도우 생성
main = tk.Tk()
main.title("DoTe ToDo")
main.geometry("700x800+500+100")  # 창 크기 설정

# 외부 프레임 생성
outer_frame = tk.Frame(main)
outer_frame.pack(fill=tk.BOTH, expand=1)

# 왼쪽 프레임 생성 및 추가 (왼쪽 절반을 차지)
left_frame = tk.Frame(outer_frame, width=500, height=800)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 오른쪽 프레임 생성 및 추가 (오른쪽 절반을 차지)
right_frame = tk.Frame(outer_frame, width=500, height=800,relief="solid",bd="2")
right_frame.pack(side=tk.RIGHT, fill=tk.Y)  # fill=tk.Y로 설정하여 오른쪽 프레임이 완전히 채워지도록 함

# 오른쪽 프레임에 캔버스와 스크롤바 추가
canvas = tk.Canvas(right_frame, width=500, height=800)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 스크롤바 생성
scrollbar = tk.Scrollbar(right_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 스크롤바와 캔버스 연결
canvas.configure(yscrollcommand=scrollbar.set)

# 프레임 컨테이너 생성
frame_container = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_container, anchor="nw")

# 왼쪽 프레임에 버튼 생성
button = tk.Button(left_frame, text="글쓰기", command=editTodo)
button.pack(pady=20)

# 초기 데이터 표시
display_data()

# tkinter 이벤트 루프 시작
main.mainloop()
