import tkinter as tk
import subprocess

back_button = None
games_frame = None

def start_loading():
    login_button.pack_forget()
    password_label.pack(pady=5, side="top", anchor="center")
    password_entry.pack(pady=5, side="top", anchor="center")
    password_entry.focus_set()
    submit_button.pack(pady=5, side="top", anchor="center")

def check_password(event=None):
    password_attempt = password_var.get().strip()
    if password_attempt == "123":
        show_correct_password()
    else:
        message = "Вы ввели неправильный пароль, попробуйте снова."
        error_label.config(text=message)
        error_label.pack(pady=5)

def show_correct_password():
    for widget in [password_label, password_entry, submit_button, error_label]:
        widget.pack_forget()

    correct_password_label.pack(pady=5, side="top", anchor="center")
    window.after(1000, lambda: close_and_show_loading())

def close_and_show_loading():
    correct_password_label.pack_forget()
    loading_window = tk.Toplevel(window)
    loading_window.title("Loading")
    loading_window.configure(bg="black")

    loading_label = tk.Label(loading_window, text="", bg="black", fg="white", font=("Helvetica", 12))
    loading_label.pack(pady=20)

    def loading_animation():
        loading_label.after(200, loading_animation)
        current_text = loading_label.cget("text")
        if current_text.endswith("|"):
            loading_label.config(text="/")
        elif current_text.endswith("/"):
            loading_label.config(text="-")
        elif current_text.endswith("-"):
            loading_label.config(text="\\")
        else:
            loading_label.config(text="|")

    loading_animation()

    loading_window.update_idletasks()
    loading_width = loading_window.winfo_width()
    loading_height = loading_window.winfo_height()
    x_loading = (loading_window.winfo_screenwidth() - loading_width) // 2
    y_loading = (loading_window.winfo_screenheight() - loading_height) // 2
    loading_window.geometry("+{}+{}".format(x_loading, y_loading))

    window.after(3000, lambda: close_and_welcome(loading_window))

def close_and_welcome(loading_window):
    loading_window.destroy()
    welcome_label.pack(pady=20, side="top", anchor="center")
    login_button_after_welcome.pack(pady=5, side="top", anchor="center")

def start_loading_after_welcome():
    login_button_after_welcome.pack_forget()
    loading_window = tk.Toplevel(window)
    loading_window.title("Loading")
    loading_window.configure(bg="black")

    loading_label = tk.Label(loading_window, text="", bg="black", fg="white", font=("Helvetica", 12))
    loading_label.pack(pady=20)

    def loading_animation():
        loading_label.after(200, loading_animation)
        current_text = loading_label.cget("text")
        if current_text.endswith("|"):
            loading_label.config(text="/")
        elif current_text.endswith("/"):
            loading_label.config(text="-")
        elif current_text.endswith("-"):
            loading_label.config(text="\\")
        else:
            loading_label.config(text="|")

    loading_animation()

    loading_window.update_idletasks()
    loading_width = loading_window.winfo_width()
    loading_height = loading_window.winfo_height()
    x_loading = (loading_window.winfo_screenwidth() - loading_width) // 2
    y_loading = (loading_window.winfo_screenheight() - loading_height) // 2
    loading_window.geometry("+{}+{}".format(x_loading, y_loading))

    window.after(3000, lambda: close_after_loading(loading_window))

def close_after_loading(loading_window):
    loading_window.destroy()
    welcome_label.pack_forget()
    gora_label.pack(pady=20, side="top", anchor="center")
    games_button = tk.Button(window, text="Игры", command=close_and_show_games, bg="black", fg="white", relief="solid", width=10)
    teams_button = tk.Button(window, text="Команды", command=do_nothing, bg="black", fg="white", relief="solid", width=10)
    templates_button = tk.Button(window, text="Шаблоны", command=do_nothing, bg="black", fg="white", relief="solid", width=10)

    games_button.pack(pady=5, side="left", anchor="center")
    teams_button.pack(pady=5, side="top", anchor="center")
    templates_button.pack(pady=5, side="right", anchor="center")

def start_tetris_game():
    try:
        subprocess.run(["python3", "путь к тетрису)"]) #ТУТ СКАЧАЙ ФАЙЛ С ТЕТРИСОМ, И ЗАМЕНИ ПУСТЬ НА СВОЙ
    except Exception as e:
        print(f"Ошибка при хуй qwerty.py: {e}")

def close_and_show_games():
    global back_button, games_frame

    # Убираем все виджеты из текущего окна
    for widget in window.winfo_children():
        widget.pack_forget()

    # Создаем фрейм для игр
    games_frame = tk.Frame(window, bg="black")
    
    tetris_button = tk.Button(games_frame, text="Тетрис", command=start_tetris_game, bg="black", fg="white", relief="solid", width=10)
    snake_button = tk.Button(games_frame, text="Змейка", command=do_nothing, bg="black", fg="white", relief="solid", width=10)
    minesweeper_button = tk.Button(games_frame, text="Сапёр", command=do_nothing, bg="black", fg="white", relief="solid", width=10)

    # Пакуем кнопки в фрейм и выводим фрейм
    games_frame.pack(pady=20, side="top", anchor="center")
    tetris_button.pack(side="left")
    snake_button.pack(side="left")
    minesweeper_button.pack(side="left")

    # Создаем кнопку "Назад" и выводим ее
    back_button = tk.Button(window, text="Назад", command=close_and_show_menu, bg="black", fg="white", relief="solid", width=10)
    back_button.pack(pady=5, side="top", anchor="center")

def close_and_show_menu():
    global back_button

    # Убираем фрейм с играми и кнопку "Назад"
    games_frame.pack_forget()
    back_button.pack_forget()

    # Показываем меню снова
    show_menu()

def show_menu():
    global games_frame

    # Восстанавливаем все виджеты меню
    gora_label.config(text="Меню")
    games_button.pack(pady=5, side="left", anchor="center")
    teams_button.pack(pady=5, side="top", anchor="center")
    templates_button.pack(pady=5, side="right", anchor="center")

def do_nothing():
    pass

window = tk.Tk()
window.title("EyeLess")
window.configure(bg="black")

window.geometry("400x300")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coordinate = (screen_width - window.winfo_reqwidth()) // 2
y_coordinate = (screen_height - window.winfo_reqheight()) // 2 - 50
window.geometry("+{}+{}".format(x_coordinate, y_coordinate))

login_button = tk.Button(window, text="Войти", command=start_loading, bg="black", fg="white", relief="solid", width=20)
login_button.pack(pady=20)

password_var = tk.StringVar()
password_label = tk.Label(window, text="Введите пароль:", bg="black", fg="white", font=("Helvetica", 12))
submit_button = tk.Button(window, text="Ввод", command=check_password, bg="black", fg="white", relief="solid", width=10)
submit_button.bind("<Return>", check_password)
error_label = tk.Label(window, text="", bg="black", fg="red", font=("Helvetica", 12))
correct_password_label = tk.Label(window, text="Правильный пароль", bg="black", fg="green", font=("Helvetica", 12))

welcome_label = tk.Label(window, text="Добро пожаловать!", bg="black", fg="white", font=("Helvetica", 12))
welcome_label.pack_forget()

login_button_after_welcome = tk.Button(window, text="Войти", command=start_loading_after_welcome, bg="black", fg="white", relief="solid", width=20)
login_button_after_welcome.pack_forget()

gora_label = tk.Label(window, text="Меню", bg="black", fg="white", font=("Helvetica", 12))
password_entry = tk.Entry(window, show="*", textvariable=password_var, font=("Helvetica", 12), bg="black", fg="white", relief="solid", width=20)

games_button = tk.Button(window, text="Игры", command=close_and_show_games, bg="black", fg="white", relief="solid", width=10)
teams_button = tk.Button(window, text="Команды", command=do_nothing, bg="black", fg="white", relief="solid", width=10)
templates_button = tk.Button(window, text="Шаблоны", command=do_nothing, bg="black", fg="white", relief="solid", width=10)

games_button.pack_forget()
teams_button.pack_forget()
templates_button.pack_forget()

window.mainloop()
