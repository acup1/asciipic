import threading
import time
from PIL import Image,ImageSequence
import numpy as np
from pygamedisplay import PgDisp
import sys
import os
import json


def do_img(size:tuple[int] = ()) -> None:
    global img,char_data, old_size, current_frame, cached_data, symbols
    now=current_frame
    try:
        if cached_data[now].shape[:2]==old_size[now]:
            if abs(size[0]-old_size[now][0])<3 or abs(size[1]-old_size[now][1])<3:
                char_data=cached_data[now]
                return None
            else:pass
                #print(now)
                #print(cached_data[now].shape[:2], size)
        else:pass
            #print(cached_data[now].shape[:2], size)
        
    except Exception as e:pass
        #print(e)
        #print(now)
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
    #symbols='йху'[::-1]

    #17*9
    for y in range(height):
        for x in range(width):
            grey=sum(data[y,x][:3])/3/255*data[y,x][3]/255
            char_data[y,x]=symbols[max(0,round(len(symbols)*grey)-1)]
            #char_data[y,x]='\N{ESC}[38;2;255;0;0m'+symbols[max(0,round(len(symbols)*grey)-1)]+'\u001b[0m'
            #char_data[y,x]='\N{ESC}[38;2;255;0;0m'+'1'+'\u001b[0m'
            #char_data[y,x]='1'
    cached_data[now]=char_data
    old_size[now]=char_data.shape[:2]



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
            app.set_aligned_text(''.join(screen[y,::]),0,y)
            #for x in range(hw()[1]):
            
    

    #threading.Thread(target=drawing_loop, daemon=True, name="drawer", args=()).start()
    while app.running:
        try:
            if not(app.is_minimized):
                draw()
            app.handle_events()
            #time.sleep(.001)
        except Exception as e:pass
            #print(e)

def img_changer():
    global seq, img, current_frame,frame_duration
    current_frame=1
    while threading.main_thread().is_alive():
        if current_frame>=len(seq)-1:
            current_frame=0
        img=seq[current_frame]
        current_frame+=1
        time.sleep(frame_duration)

if __name__=="__main__":
    try:
        try:
            config=json.loads(open("config.json","r").read())
        except:
            config={
                "fname":"g8.gif",
                "font_size":10,
                "speed": 1,
            }
        #img=Image.open(sys.argv[1]).convert("RGBA")
        symbols=' ."`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
        #if len(sys.argv)>1:
        #    fname=sys.argv[1]
        #else:
        #    fname="gif.gif"

        fname=config["fname"]
        seq = Image.open(fname)
        frame_duration = seq.info['duration']/1000*config["speed"]
        seq = list(i.convert("RGBA") for i in ImageSequence.Iterator(seq))
        img=seq[0]
        threading.Thread(target=img_changer,args=(),daemon=True,name="ichange").start()
        char_data=None
        old_size=[0]*len(seq)
        current_frame=1
        cached_data=[0]*len(seq)

        app=PgDisp("screen",config["font_size"])
        main(app)
    except Exception as e:
        with open("err.log","wa") as f:
            f.write(str(e))