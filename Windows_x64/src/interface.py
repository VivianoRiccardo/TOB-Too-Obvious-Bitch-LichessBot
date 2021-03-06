import tkinter
import webapp
import session
import os
from threading import Thread
import time
from subprocess import Popen, PIPE
import stockfish10
import mouse
import os
import signal
from tkinter import ttk
from tkinter import Scrollbar
from tkinter import Text
from tkinter import Entry


# Collect events until released

there_is_session = False
path = ""
xy = None
go_thread = True
pid = None
cs = False
cs2 = False
text = ''
user_move = ''

def btn6u():
    global cs2
    cs2 = True
    
def btn4u():
    global cs
    cs = True
    
def btn3u():
    global xy
    mouse.screenshot()
    xy = mouse.get_area()
    
def center_window(root,w=300, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)    
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

def threaded_function2(lista):
    combo = lista[0]
    combo2 = lista[1]
    combo3 = lista[2]
    combo4 = lista[3]
    global pid
    pid = os.getpid()
    global there_is_session
    while(not there_is_session):
        global cs
        cs = False
        global cs2
        cs2 = False
        global there_is_session
    global path
    sessions = session.IdSession(path)
    r = sessions.getAccountInformation()
    if(sessions.getStatusCode(r) == 200):
        window = tkinter.Tk()
        window.title("Success")
        center_window(window,200,200)
        label = tkinter.Label(window, text = "You Profile has been loaded").pack()
        label = tkinter.Label(window, text = "Close This window!").pack()
        window.mainloop()
    else:
        window = tkinter.Tk()
        window.title("Failed")
        center_window(window,200,200)
        label = tkinter.Label(window, text = "An Error Occurred").pack()
        label = tkinter.Label(window, text = "loading your profile").pack()
        label = tkinter.Label(window, text = "Close This Window!").pack()
        window.mainloop()
    
    l = 'position startpos'
    s = combo.get()
    waiting = (float)(combo4.get())
    engine = 'stockfish_6_x64_modern'
    if(s == '5'):
        engine = 'stockfish_5_x64_modern'
    elif(s == '6'):
        engine = 'stockfish_6_x64_modern'
    elif(s == '7'):
        engine = 'stockfish_7_x64'
    elif(s == '8'):
        engine = 'stockfish_8_x64_modern'
    elif(s == '9'):
        engine = 'stockfish_9_x64'
    elif(s == '10'):
        engine = 'stockfish_10_x64_modern'
    
    depth = (int)(combo2.get())
    sec = (float)(combo3.get())
    
    p = Popen("../bin/"+engine, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    stockfish10.get(p, verbose=True)
    stockfish10.putget(p, 'uci')
    stockfish10.putget(p, l)
    move = '-10'
    move_counter = 0
    l+=' moves'
    g = 0
    gameId = ''
    u = False
    uu = False
    new_move = False
    reminder = ''
    opponent_castle = 0
    global user_move
    last_user_move = user_move
    while(sessions.getStatusCode(r)== 200 and move_counter < 20):
        
        global cs
        u = cs
        global cs2
        uu = cs2
        if((u == True or uu == True) and g == 0):
            window = tkinter.Tk()
            window.title("Success")
            center_window(window,200,200)
            label = tkinter.Label(window, text = "The bot is ready to play or think!").pack()
            label = tkinter.Label(window, text = "Close this window to let him play").pack()
            window.mainloop()
            g = 1
            
        r = sessions.getOngoingGames("1")
        
        if(sessions.getStatusCode(r) == 200 and (u == True or uu == True)):
            try:
                cont = sessions.getContent(r)
                color = cont['nowPlaying'][0]['color']
                isMyTurn = cont['nowPlaying'][0]['isMyTurn']
                lastMove = cont['nowPlaying'][0]['lastMove']
                if(cont['nowPlaying'][0]['gameId'] != gameId):
                    gameId = cont['nowPlaying'][0]['gameId']
                    l = 'position startpos moves'
                    move = '-10'
                    move_counter = 0
                    new_move = False
                    reminder = ''
                    opponent_castle = 0
                else:
                    
                    if(move != lastMove):
                        move_counter = 0
                        move = lastMove
                        move2 = move
                        if(move!=''):
                            if(color == 'white'):
                                if(move[0] == 'e' and move[1] == '8'):
                                    if(opponent_castle == 0):
                                        opponent_castle = 1
                                        if(move[2] == 'h' and move[3] == '8'):
                                            move2=move2[:2]+'g'+move2[3:]
                                        elif(move[2] == 'a' and move[3] == '8'):
                                            move2=move2[:2]+'c'+move2[3:]
                            else:
                                if(move[0] == 'e' and move[1] == '1'):
                                    if(opponent_castle == 0):
                                        opponent_castle = 1
                                        if(move[2] == 'h' and move[3] == '1'):
                                            move2=move2[:2]+'g'+move2[3:]
                                        elif(move[2] == 'a' and move[3] == '1'):
                                            move2=move2[:2]+'c'+move2[3:]
                        new_move = True
                        if(isMyTurn == True):
                            l+=' '+reminder+' '+move2
                            move2 = move
                            
                    else:
                        if(isMyTurn == True):
                            move_counter+=1
                            
                    if(isMyTurn == True):
                        print("eccomi")
                        stockfish10.put(p,l)
                        pos = stockfish10.go(p, depth=depth, t=sec)
                        if pos[13:14] == ' ':
                            new_pos = pos[9:13]
                        else:
                            new_pos = pos[9:14]
                           
                        if(u == True and uu == False):
                            mouse.click_somewhere(xy,new_pos,color,waiting)
                        if(new_move or l == 'position startpos moves'):
                            if(u == True and uu == False):
                                reminder = new_pos
                                new_move = False
                            elif uu == True:
                                txt.insert("end-1c",str(new_pos)+"\n")
                                txt.see("end")
                            
                            
                        if(uu == True and new_move):
                            global user_move
                            while(last_user_move == user_move):
                                global user_move
                                last_user_move = last_user_move
                            reminder = user_move
                            new_move = False
                            last_user_move = user_move
                                

                            
                        
            except:
                print("No Ongoing matches")
                l = 'position startpos moves'
                move = '-10'
                move_counter = 0
                gameId = ''
                new_move = True
                reminder = ''
                opponent_castle = 0
             
    
def btn5u(s1,s2):
    f = open("../text/client_inf.txt","w")
    f.write(s1+"\n")
    f.write(s2)
    f.close()

def bt2(s):
    try:
        f = open("../bin/"+s+".bin", 'rb')
        f.close()
        global path
        path = "../bin/"+s+".bin"
        global there_is_session
        there_is_session = True
    except :
        window = tkinter.Tk()
        center_window(window,200,200)
        window.geometry("200x200")
        label = tkinter.Label(window, text = "This profile has not been saved").pack()
        label = tkinter.Label(window, text = "try to create a session!").pack()

def bt7(s,action):
    global user_move
    user_move = s
    print(s)

       
if __name__ == "__main__":

    
    window = tkinter.Tk()
    window.title("TOB")
    center_window(window,600,500)
    window.resizable(True, True)
    
    #top_frame = tkinter.Frame(window).pack()
    #bottom_frame = tkinter.Frame(window).pack(side = "bottom")
    tkinter.Label(window, text = "Client Id").grid(row = 0) # this is placed in 0 0
    # 'Entry' is used to display the input-field
    entry1 = tkinter.Entry(window) # this is placed in 0 1
    entry1.grid(row = 0, column = 1) # this is placed in 0 1

    tkinter.Label(window, text = "Client Secret").grid(row = 1) # this is placed in 1 0
    entry2 = tkinter.Entry(window) # this is placed in 1 1
    entry2.grid(row = 1, column = 1) # this is placed in 1 1
    tkinter.Label(window, text = "Lichess profile").grid(row = 22,column = 1) # this is placed in 1 0
    tkinter.Label(window, text = "Best Moves").grid(row = 10,column = 2) # this is placed in 1 0
    entry3 = tkinter.Entry(window) # this is placed in 1 1
    entry3.grid(row = 25, column = 1) # this is placed in 1 1
    tkinter.Label(window, text = "Your move").grid(row = 30,column = 2)
    entry4 = tkinter.Entry(window) # this is placed in 1 1
    entry4.grid(row = 35, column = 2)
    # now, create some widgets in the top_frame and bottom_frame
    btn0 = tkinter.Button(window, text = "Create Web Application", fg = "black", height = 5, width = 20)
    btn1 = tkinter.Button(window, text = "Create Session", fg = "red", height = 5, width = 20)
    btn2 = tkinter.Button(window, text = "Load Lichess Profile", fg = "green", command=lambda :  bt2(entry3.get()))
    btn3 = tkinter.Button(window, text = "Take a Screenshot of Lichess Board", fg = "purple", command=lambda :  btn3u()).grid(row = 40, column = 1)
    btn4 = tkinter.Button(window, text = "Let The bot Play", fg = "orange",command=lambda :  btn4u()).grid(row = 50, column = 1)
    btn5 = tkinter.Button(window, text = "Save Client Inf", fg = "yellow", command=lambda :  btn5u(entry1.get(),entry2.get()))
    btn6 = tkinter.Button(window, text = "Let The bot Think", fg = "black", command=lambda :  btn6u()).grid(row = 55, column = 1)
    btn7 = tkinter.Button(window, text = "Move!", fg = "black", command=lambda :  bt7(entry4.get(),entry4.delete(0, 'end')))
    
    btn0.bind("<Button-1>", webapp.bt0)
    btn0.grid(row = 2, column = 1)
    btn1.bind("<Button-1>", webapp.bt1)
    btn1.grid(row = 20, column = 1)
    btn5.grid(row = 0, column = 2)
    btn2.grid(row = 30, column = 1)
    btn7.grid(row = 40, column = 2)
    
    txt = Text(window, width = 25, height = 2)
    txt.grid(row = 20,column = 2, columnspan = 2)
    scrollb = Scrollbar(window, command=txt.yview)
    txt['yscrollcommand'] = scrollb.set
    
    combo = ttk.Combobox(window)
    combo['values']= (5,6,7,8,9,10)
    combo.current(5)
    combo.grid(column=1, row=60)
    tkinter.Label(window, text = "Stockfish Level").grid(row = 60,column = 2)
    combo2 = ttk.Combobox(window)
    combo2['values']= (1,2,3,5,10,15,20)
    combo2.current(3)
    combo2.grid(column=1, row=70)
    tkinter.Label(window, text = "Depth").grid(row = 70,column = 2)
    combo3 = ttk.Combobox(window)
    combo3['values']= (0.01,0.03,0.05,0.1,1,5,10,30,60,120,300,600)
    combo3.current(4)
    combo3.grid(column=1, row=80)
    tkinter.Label(window, text = "Seconds").grid(row = 80,column = 2)
    combo4 = ttk.Combobox(window)
    combo4['values']= (0.02,0.03,0.05,0.1,1,3,5,10,30,60,120,300,600)
    combo4.current(1)
    combo4.grid(column=1, row=90)
    tkinter.Label(window, text = "Max random waiting time").grid(row = 90,column = 2)
    lista = [combo,combo2,combo3,combo4]
    thread = Thread(target = threaded_function2,args = (lista, ))
    thread.start()
    window.mainloop()
    if(pid != None):
        os.kill(pid, signal.SIGTERM)
     
    
    
    

