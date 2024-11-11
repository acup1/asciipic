import threading
import time
from PIL import Image,ImageSequence
import numpy as np
from pygamedisplay import PgDisp
import sys
import os

def do_img(size:tuple[int] = ()) -> None:
    global img,char_data
    temp=img.copy()
    w, h = temp.size
    temp=temp.resize((int(w*17/9), h))
    w, h = temp.size
    if len(size)==0:size=(w,h)
    #else: size=(min(size),min(size))
    #size=(17,17)
    temp.thumbnail(size[::-1], Image.LANCZOS)

    data = np.array(temp)
    height,width,_=data.shape
    char_data=np.zeros((height,width),dtype=str)
    symbols='$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`". '[::-1]
    #symbols='йху'[::-1]

    #17*9
    for y in range(height):
        for x in range(width):
            grey=sum(data[y,x][:3])/3/255*data[y,x][3]/255
            char_data[y,x]=symbols[max(0,round(len(symbols)*grey)-1)]
            #char_data[y,x]='\N{ESC}[38;2;255;0;0m'+symbols[max(0,round(len(symbols)*grey)-1)]+'\u001b[0m'
            #char_data[y,x]='\N{ESC}[38;2;255;0;0m'+'1'+'\u001b[0m'
            #char_data[y,x]='1'




def paste(b: np.array,a: np.array,dx: int=0,dy: int=0) -> np.array:
    "paste a in b with dx,dy"
    sy=b.shape[0]//2-a.shape[0]//2+dy
    sx=b.shape[1]//2-a.shape[1]//2+dx
    ey=b.shape[0]//2+a.shape[0]//2+a.shape[0]%2+dy
    ex=b.shape[1]//2+a.shape[1]//2+a.shape[1]%2+dx
    b[sy:ey,sx:ex]=a
    return b

def main(app: PgDisp):
    global char_data, screen

    hw=app.size
    #stdscr.addstr(5,10,f"{tuple(hw())}")
    #stdscr.addstr(6,10,f"{char_data.shape}")
    #frame=screen[hw()[0]//2-char_data.shape[0]//2:hw()[0]//2+char_data.shape[0]//2+1, hw()[1]//2-char_data.shape[1]//2:hw()[1]//2+char_data.shape[1]//2+1]
    #stdscr.addstr(7,10,f"{frame.shape}")
    #screen[hw()[0]//2-char_data.shape[0]//2:hw()[0]//2+char_data.shape[0]//2+1,
    #        hw()[1]//2-char_data.shape[1]//2:hw()[1]//2+char_data.shape[1]//2+1]=char_data
    #screen[hw()[0]-char_data.shape[0]//2:hw()[0]+char_data.shape[0]//2, hw()[1]-char_data.shape[1]//2:hw()[1]+char_data.shape[1]//2]=char_data
    
    def draw():
        screen=np.full(hw()," ",dtype=str)
        do_img(tuple(hw()))
        screen=paste(screen,char_data)
        app.clear()
        for y in range(hw()[0]):
            for x in range(hw()[1]):
                app.set_aligned_text(screen[y,x],x,y)
            
        
    def drawing_loop():
        while 1:
            try:
                draw()
                app.handle_events()
                time.sleep(.001)
            except:pass

    #threading.Thread(target=drawing_loop, daemon=True, name="drawer", args=()).start()
    while app.running:
        try:
            drawing_loop()
        except:
            pass

def img_changer():
    global seq, img
    i=1
    while threading.main_thread().is_alive():
        if i>len(seq)-1:
            i=0
        img=seq[i]
        i+=1
        time.sleep(.1)

if __name__=="__main__":
    #img=Image.open(sys.argv[1]).convert("RGBA")
    seq = Image.open(sys.argv[1])
    seq = list(i.convert("RGBA") for i in ImageSequence.Iterator(seq))
    img=seq[0]
    threading.Thread(target=img_changer,args=(),daemon=True,name="ichange").start()
    char_data=None

    app=PgDisp("screen",10)
    main(app)