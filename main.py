import curses
import typing
import sqlite3

from utils import to_str, isvalidEmail, SPACE
from typing import List, Dict, Tuple, Optional, Union
from curses import wrapper
from curses.textpad import rectangle

from quotes_site import main as quotes_site
from notes_site import main as notes_site
from todos_site import main as todos_site

from menu import CursesMenu


def check_font_site(stdscr):
    CENTER = (curses.LINES // 2, curses.COLS // 2)
    stdscr.addstr(
        CENTER[0] - 2,
        CENTER[1] - (len((msg := "FIRST CHECK IF YOU ARE HAVE RIGHT FONT")) // 2),
        msg,
    )
    stdscr.addstr(
        CENTER[0] - 1,
        CENTER[1]
        - (len((msg := "if you have right font than type 'done'")) // 2),
        msg,
    )
    stdscr.addstr(
        CENTER[0],
        CENTER[1]
        - (
            len(
                (
                    msg := "you can dowloand one of my favoutites on 'https://bit.ly/JetBrainsMonoRegularNerdFontCompleteMono'"
                )
            )
            // 2
        ),
        msg,
    )
    stdscr.addstr(
        CENTER[0]+1,
        CENTER[1]
        - (
            len(
                (
                    msg := "if font doesn't work try dowloand newest terminal on 'https://bit.ly/microsoft-WindowsTerminal'"
                )
            )
            // 2
        ),
        msg,
    )
    cols = curses.COLS // 4-2 #* i have only 3 special chars in my program
    stdscr.addstr( CENTER[0] + 3, cols+4, f"\u2193{SPACE*cols}\u2193{SPACE*cols}\u2193")
    stdscr.addstr( CENTER[0] + 4, cols+4, f"\u2713{SPACE*(cols+1)}{SPACE*(cols)}\u2717")
    rectangle(stdscr, CENTER[0] + 4 , cols*2+4 , CENTER[0] + 4+2 , cols*2+2+4 )
    curses.echo()
    while True:
        rectangle(stdscr, CENTER[0] + 9 , CENTER[1]-3 , CENTER[0] + 11 , CENTER[1]+3 )
        done = to_str(stdscr.getstr(CENTER[0] + 10, CENTER[1]-2, 5))
        if "done" in done:
            break

        
            
    
def login_menu() -> str:
    menu: dict = {
        "title": "Menu",
        "type": "menu",
        "subtitle": "Chosse login or signup ",
    }

    option_1: dict = {"title": "LOG-IN", "type": "login", "command": "echo login"}

    option_2: dict = {"title": "SIGN-UP", "type": "signup", "command": "echo signup"}

    menu["options"] = [option_1, option_2]

    m = CursesMenu(menu)
    selected_action: Dict[str, str] = m.display()
    return selected_action["type"]


def signup(stdscr, msg: str = "") -> Tuple[str, str, str]:
    curses.echo()
    stdscr.clear()

    stdscr.addstr(0, curses.COLS - len(msg) - 1, msg)
    stdscr.addstr(1, 1, "Name        : ")
    stdscr.addstr(4, 1, "Email       : ")
    stdscr.addstr(7, 1, "Password    : ")
    stdscr.addstr(10, 1, "re-Password : ")

    rectangle(stdscr, 0, 14, 2, 30)
    rectangle(stdscr, 3, 14, 5, 45)
    rectangle(stdscr, 6, 14, 8, 30)
    rectangle(stdscr, 9, 14, 11, 30)

    name: str = to_str(stdscr.getstr(1, 15, 15))
    rectangle(stdscr, 0, 14, 2, 30)

    email: str = to_str(stdscr.getstr(4, 15, 30)).replace("\\x16", "@")
    rectangle(stdscr, 3, 14, 5, 45)

    password: str = to_str(stdscr.getstr(7, 15, 15))
    rectangle(stdscr, 6, 14, 8, 30)

    password2: str = to_str(stdscr.getstr(10, 15, 15))
    rectangle(stdscr, 9, 14, 11, 30)

    stdscr.addstr(15, 5, "if you want to continue then press | Any")
    stdscr.addstr(16, 5, "if you want to correct then press  | r")
    stdscr.addstr(17, 5, "if you want to quit then press     | q")
    key: str = stdscr.getkey()

    if key == "r":
        name, email, password = signup(stdscr)
    elif key == "q":
        curses.endwin()
        quit()
    else:
        if not isvalidEmail(email):
            name, email, password = signup(stdscr, "Invalid email syntax")
        if password != password2:
            name, email, password = signup(stdscr, "Password mismatch")
        names = cursor.execute("SELECT name FROM users").fetchall()
        if name in names:
            name, email, password = signup(stdscr, "Name already used")
        usr = find_user(name, email, password)
        if not usr:
            add_user(name, email, password)
        else:
            name, email, password = signup(stdscr, "User already exsist")
    stdscr.refresh()

    return name, email, password


def add_user(name: str, email: str, password: str):
    params = (name, email, password)
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?,?,?)", params)
    connection.commit()


def find_user(name: str, email: str, password: str) -> Tuple[bool, str]:
    try:
        params: tuple = (name, email, password)
        user = cursor.execute(
            "SELECT * FROM users WHERE name = ? AND email = ? AND password = ?", params
        ).fetchone()
        if user:
            return True
    except:
        return False


def login(stdscr, msg: str = "") -> Tuple[str, str, str]:
    curses.echo()
    stdscr.clear()

    stdscr.addstr(0, curses.COLS - len(msg) - 1, msg)
    stdscr.addstr(1, 1, "Name     : ")
    stdscr.addstr(4, 1, "Email    : ")
    stdscr.addstr(7, 1, "Password : ")

    rectangle(stdscr, 0, 11, 2, 27)
    rectangle(stdscr, 3, 11, 5, 42)
    rectangle(stdscr, 6, 11, 8, 27)

    name: str = to_str(stdscr.getstr(1, 12, 15))
    rectangle(stdscr, 0, 11, 2, 27)

    email: str = to_str(stdscr.getstr(4, 12, 30)).replace("\\x16", "@")
    rectangle(stdscr, 3, 11, 5, 42)

    password: str = to_str(stdscr.getstr(7, 12, 15))
    rectangle(stdscr, 6, 11, 8, 27)

    stdscr.addstr(15, 5, "if you want to continue then press | Any")
    stdscr.addstr(16, 5, "if you want to correct then press  | r")
    stdscr.addstr(17, 5, "if you want to quit then press     | q")
    key: str = stdscr.getkey()

    if key == "r":
        name, email, password = login(stdscr)
    elif key == "q":
        curses.endwin()
        quit()
    else:
        if not isvalidEmail(email):
            name, email, password = login(stdscr, "Invalid email syntax")
        user_exsists = find_user(name, email, password)
        if not user_exsists:
            name, email, password = login(stdscr, "Wrong username or password")

    stdscr.refresh()
    return name, email, password


def main_menu() -> str:
    menu: dict = {
        "title": "Menu",
        "type": "menu",
        "subtitle": "Chosse main funcionality ",
    }

    option_1: dict = {
        "title": "QUOTES - bug fixing (in 1 week)",
        "type": "quote",
        "command": "echo quote",
    }
    option_2: dict = {
        "title": "NOTES",
        "type": "notes",
        "command": "echo notes",
    }
    option_3: dict = {
        "title": "TODOS",
        "type": "todos",
        "command": "echo todos",
    }
    option_4: dict = {
        "title": "STATS - comming soon (in 1 week)",
        "type": "stats",
        "command": "echo stats",
    }
    # add here when more funcionalities

    menu["options"] = [
        option_1,
        option_2,
        option_3,
        option_4,
    ]  # add to this list when more funcionalities

    m = CursesMenu(menu)
    selected_action: Dict[str, str] = m.display()
    return selected_action["type"]


def main(stdscr):
    check_font_site(stdscr)
    global cursor, connection
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, password TEXT)"
    )
    connection.commit()

    stdscr.clear()
    stdscr.refresh()

    curses.curs_set(1)

    name: str
    email: str
    password: str
    while True:
        # stdscr.clear()
        # stdscr.refresh()
        # action: str = login_menu()
        # if action == "signup":
        #     name, email, password = signup(stdscr)
        # elif action == "login":
        #     name, email, password = login(stdscr)
        # elif action == "exitmenu":
        #     connection.close()
        #     quit()

        name, email, password = "anonymous", "anonymous@gmail.com", "anonymous1"
        stdscr.clear()
        stdscr.refresh()

        while True:
            stdscr.clear()
            stdscr.refresh()
            action: str = main_menu()
            if action == "quote":
                pass  # quotes_site(stdscr, name) #TODO FIXME
            elif action == "notes":
                notes_site(stdscr, name)
            elif action == "todos":
                todos_site(stdscr, name)
            elif action == "stats":
                pass  # TODO: create stats menu
            elif action == "exitmenu":
                quit()
                break


wrapper(main)


# TODO more autentification for email (send autentification email)
# TODO use typing module to simplyfi code to read by other person(module typing)
