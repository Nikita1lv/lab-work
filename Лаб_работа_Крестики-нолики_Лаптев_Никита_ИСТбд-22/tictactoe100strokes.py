import tkinter as tk
b=[' ']*9; human,ai='X','O'
wins=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def win(s):
    for a,c,d in wins:
        if s[a]==s[c]==s[d]!=' ': return s[a]
    return None
def full(s): return all(x!=' ' for x in s)

def line_sc(s,pl):
    op=human if pl==ai else ai; r=0
    for a,c,d in wins:
        ln=[s[a],s[c],s[d]]
        if op not in ln: r+={0:1,1:3,2:9}.get(ln.count(pl),0)
        if pl not in ln: r-={0:1,1:3,2:9}.get(ln.count(op),0)
    return r

def evalb(s,d):
    w=win(s)
    if w==ai: return 10-d
    if w==human: return d-10
    if full(s): return 0
    return line_sc(s,ai)

def mm(s,d,a,b,maxi):
    if win(s) or full(s): return evalb(s,d),-1
    best=-1
    if maxi:
        v=-999; mv=[i for i,x in enumerate(s) if x==' ']
        mv.sort(key=lambda i:line_sc(s[:i]+[ai]+s[i+1:],ai),reverse=True)
        for i in mv:
            s[i]=ai; sc,_=mm(s,d+1,a,b,False); s[i]=' '
            if sc>v: v,best=sc,i
            a=max(a,sc)
            if b<=a: break
        return v,best
    else:
        v=999
        for i in [i for i,x in enumerate(s) if x==' ']:
            s[i]=human; sc,_=mm(s,d+1,a,b,True); s[i]=' '
            if sc<v: v,best=sc,i
            b=min(b,sc)
            if b<=a: break
        return v,best

def ai_move():
    _,i=mm(b[:],0,-999,999,True)
    if i!=-1:
        b[i]=ai; btns[i]['text']=ai; btns[i]['state']='disabled'; btns[i]['bg']='#ffd7d7'
    check_end()

def click(i):
    if b[i]!=' ' or win(b): return
    b[i]=human; btns[i]['text']=human; btns[i]['state']='disabled'; btns[i]['bg']='#d7f7ff'
    if not check_end(): ai_move()

def check_end():
    w=win(b)
    if w:
        lab['text']=f'Победа: {w}'
        for a,c,d in wins:
            if b[a]==b[c]==b[d]==w:
                for j in (a,c,d): btns[j]['bg']='#a0ff9e'
        dis(); return True
    if full(b):
        lab['text']='Ничья'; dis(); return True
    lab['text']=f'Ход: {("человека" if sum(x!=" " for x in b)%2==0 else "бота")}'; return False

def dis():
    for t in btns: t['state']='disabled'

def new_game():
    for i in range(9):
        b[i]=' '; t=btns[i]; t['text']=''; t['state']='normal'; t['bg']='#f0f0f0'
    lab['text']='Ход: ' + ('человека' if human=='X' else 'бота')
    if human=='O': ai_move()

def set_side(side):
    global human,ai; human,ai=side,('O' if side=='X' else 'X'); new_game()

root=tk.Tk(); root.title('(Крестики-нолики)'); root.geometry('520x640'); root.configure(bg='#1f2530')
root.bind('r',lambda e:new_game()); root.bind('R',lambda e:new_game())
frm=tk.Frame(root,bg='#1f2530'); frm.pack(padx=16,pady=10)
btns=[]
for r in range(3):
    for c in range(3):
        i=r*3+c
        t=tk.Button(frm,text='',font=('Segoe UI',36,'bold'),width=3,height=1,
                    command=lambda i=i:click(i),bg='#f0f0f0',activebackground='#e8e8e8',fg='#222')
        t.grid(row=r,column=c,padx=12,pady=12,ipadx=20,ipady=20); btns.append(t)
lab=tk.Label(root,text='Выберите сторону и начните',font=('Segoe UI',16),bg='#1f2530',fg='#e6eef7'); lab.pack(fill='x',padx=16,pady=6)
ctrl=tk.Frame(root,bg='#1f2530'); ctrl.pack(pady=4)
tk.Button(ctrl,text='Играть за X',font=('Segoe UI',12),command=lambda:set_side('X')).grid(row=0,column=0,padx=6)
tk.Button(ctrl,text='Играть за O',font=('Segoe UI',12),command=lambda:set_side('O')).grid(row=0,column=1,padx=6)
tk.Button(root,text='Новая игра (R)',font=('Segoe UI',14),command=new_game,bg='#e6eef7',activebackground='#dbe7f5').pack(pady=8,ipadx=12,ipady=6)
root.mainloop()
