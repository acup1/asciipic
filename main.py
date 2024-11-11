import threading
import time
from PIL import Image,ImageSequence
import numpy as np
import sys
import os
import curses



def do_img(size:tuple[int] = ()) -> None:
    global img,char_data
    temp=img.copy()
    w, h = temp.size
    temp=temp.resize((int(w*20/9), h))
    w, h = temp.size
    if len(size)==0:size=(w,h)
    #else: size=(min(size),min(size))
    #size=(17,17)
    temp.thumbnail(size[::-1], Image.LANCZOS)

    data = np.array(temp)
    height,width,_=data.shape
    char_data=np.zeros((height,width),dtype=str)
    symbols='$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`". '[::-1]
    symbols='йху'[::-1]

    #17*9
    for y in range(height):
        for x in range(width):
            grey=sum(data[y,x][:3])/3/255*data[y,x][3]/255
            char_data[y,x]=symbols[max(0,round(len(symbols)*grey)-1)]
            #char_data[y,x]='\N{ESC}[38;2;255;0;0m'+symbols[max(0,round(len(symbols)*grey)-1)]+'\u001b[0m'
            #char_data[y,x]='\N{ESC}[38;2;255;0;0m'+'1'+'\u001b[0m'
            #char_data[y,x]='1'




def paste(b,a,dx,dy):
    sy=b.shape[0]//2-a.shape[0]//2+dy
    sx=b.shape[1]//2-a.shape[1]//2+dx
    ey=b.shape[0]//2+a.shape[0]//2+a.shape[0]%2+dy
    ex=b.shape[1]//2+a.shape[1]//2+a.shape[1]%2+dx
    b[sy:ey,sx:ex]=a
    return b

def main(stdscr: curses.window):
    global char_data, screen
    curses.start_color()

    curses.mousemask(1)
    curses.curs_set(0)
    hw=stdscr.getmaxyx
    dx,dy=0,0
    #stdscr.addstr(5,10,f"{tuple(hw())}")
    #stdscr.addstr(6,10,f"{char_data.shape}")
    #frame=screen[hw()[0]//2-char_data.shape[0]//2:hw()[0]//2+char_data.shape[0]//2+1, hw()[1]//2-char_data.shape[1]//2:hw()[1]//2+char_data.shape[1]//2+1]
    #stdscr.addstr(7,10,f"{frame.shape}")
    #screen[hw()[0]//2-char_data.shape[0]//2:hw()[0]//2+char_data.shape[0]//2+1,
    #        hw()[1]//2-char_data.shape[1]//2:hw()[1]//2+char_data.shape[1]//2+1]=char_data
    #screen[hw()[0]-char_data.shape[0]//2:hw()[0]+char_data.shape[0]//2, hw()[1]-char_data.shape[1]//2:hw()[1]+char_data.shape[1]//2]=char_data
    
    def draw():
        stdscr=curses.initscr()
        screen=np.full(hw()," ",dtype=str)
        do_img(tuple(hw()))
        screen=paste(screen,char_data,dx,dy)
        stdscr.erase()
        stdscr.addstr(0,0,'')
        for y in range(hw()[0]):
            for x in range(hw()[1]-1):
                try:
                    stdscr.addstr(screen[y,x])
                except:pass
            try:
                stdscr.addstr('\n')
            except:pass
            
        
        stdscr.addstr(0,0,f"{hw()}")
        stdscr.addstr(1,0,f"{char_data.shape}")
        stdscr.refresh()
    def drawing_loop():
        while 1:
            try:
                draw()
            except:pass

    threading.Thread(target=drawing_loop, daemon=True, name="drawer", args=()).start()
    while True:
        try:
            event = stdscr.getch()
            if event == 546:draw()
            #if event==ord('a'):
            #    dx+=-1
            #    dy+=0
            #elif event==ord('w'):
            #    dx+=0
            #    dy+=-1
            #elif event==ord('s'):
            #    dx+=0
            #    dy+=1
            #elif event==ord('d'):
            #    dx+=1
            #    dy+=0
            pass
        except:
            pass

def img_changer():
    global seq, img
    i=1
    while 1:
        if i>len(seq)-1:
            i=0
        img=seq[i]
        i+=1
        time.sleep(.1)

if __name__=="__main__":
    #img=Image.open(sys.argv[1]).convert("RGBA")
    seq = Image.open("g7.gif")
    seq = list(i.convert("RGBA") for i in ImageSequence.Iterator(seq))
    img=seq[0]
    threading.Thread(target=img_changer,args=(),daemon=True,name="ichange").start()
    char_data=None
    curses.wrapper(main)