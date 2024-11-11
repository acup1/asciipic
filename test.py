import curses

def main(stdscr):
    curses.mousemask(1)
    curses.curs_set(0)
    stdscr.addstr("Click inside the terminal window with your mouse...")
    hw=stdscr.getmaxyx

    while True:
        try:
            event = stdscr.getch()
            if event == curses.KEY_MOUSE:
                _, x, y, _, button = curses.getmouse()
                #stdscr.clear()
                stdscr.addstr(0,0,"-"*(hw()[1]-1))
                stdscr.addstr(hw()[0]-1,0,"-"*(hw()[1]-1))
                stdscr.addstr(0,0,f"Mouse clicked at ({x}, {y}), button {button}")
                stdscr.addstr(y,x,"#")
                stdscr.refresh()
            else:
                stdscr.addstr(0,0,"-"*(hw()[1]-1)*2)
                stdscr.addstr(hw()[0]-1,0,"-"*(hw()[1]-1))
                stdscr.addstr(0,0,f"{event}")
        except:pass

# Running the curses wrapper
curses.wrapper(main)