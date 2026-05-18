import tkinter as tk
from tkinter import filedialog, messagebox



current_file = None
def save_file_as():
  """다른이름으로 저장"""

  global current_file
  file_path = filedialog.asksaveasfilename(
        defaultextension='.txt',
        filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")]
    )
  if file_path:
        current_file = file_path
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text_area.get('1.0', tk.END))
        messagebox.showinfo('저장 완료', f"'{current_file}'에 저장했습니다.")
        app.title(f'메모장 - {current_file}')

def new_file():
    """새파일생성"""
    global current_file
    text_area.delete('1.0', tk.END) #텍스트 위젯 전체삭제
    current_file = None
    app.title("메모장 - 새파일")

def open_file():
    """기존 txt 파일 열기"""
    global current_file
    file_path = filedialog.askopenfilename(
        filetypes=[("텍스트 파일","*.txt"), ("모든파일","*.*")]
    )
    if file_path:
        current_file = file_path
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        text_area.delete('1.0', tk.END)
        text_area.insert('1.0', content)
        app.title(f'메모장 -{file_path}')

def save_file():
    global current_file
    if current_file is None:
        save_file_as()
    else:
        with open(current_file , 'w', encoding='utf-8') as f:
            f.write(text_area.get('1.0', tk.END))
        messagebox.showinfo('저장 완료!',f"'{current_file}'에 ㅈ저장!.")

app = tk.Tk()

def exit_app():
   '''프로그램종료'''
   app.destroy()


app.title('메모장')
#현재 열려있는 파일정보저장
text_area = tk.Text(app)
text_area.pack(expand=True, fill='both')
# 메뉴
menubar = tk.Menu(app)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label='새로 만들기', command=new_file)
file_menu.add_command(label='열기', command=open_file)
file_menu.add_command(label='저장', command=save_file)
file_menu.add_command(label='다른 이름으로 저장',command=save_file_as)
file_menu.add_separator()
file_menu.add_command(label='종료',command=exit_app)
menubar.add_cascade(label='파일',menu=file_menu)
app.config(menu=menubar)
app.mainloop()