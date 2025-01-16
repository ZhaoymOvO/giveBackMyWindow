import win32gui, pandas as pd

def get_all_windows():
    windows = []
    win32gui.EnumWindows(
        lambda hwnd, _: windows.append((hwnd, win32gui.GetWindowText(hwnd))), None
    )
    return windows

def move_window(title, x, y):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        print("window not found")
        return
    win32gui.MoveWindow(hwnd, x, y, 0, 0, True)

if __name__ == "__main__":
    windows = pd.DataFrame(get_all_windows(), columns=["id", "title"])
    windows = windows.replace("", pd.NA).dropna().drop_duplicates(subset="title")
    windows.index = [i for i in range(len(windows))]
    print(windows.to_string())
    while 1:
        windowToMove = input(
            f"""\nEnter the window's index you want to move (0 to {len(windows)-1})
or enter "/name" to find the window
or enter quit/q/exit to exit this script> """
        ).strip()
        if windowToMove.isnumeric():
            windowToMove=int(windowToMove)
            break
        elif windowToMove.startswith('/'):
            listToPrint = windows['title'].str.contains(windowToMove[1:], case=0)
            for i in range(len(listToPrint)):
                if listToPrint.values[i]:
                    print(f"{i}\t\t{windows.loc[i,'title']}")
        elif windowToMove in ['quit', 'q', 'exit']:
            exit()
        else:
            print('!Syntax Error')
    move_window(windows.loc[windowToMove, 'title'], 0, 0)
