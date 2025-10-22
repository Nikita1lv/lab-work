import tkinter as tk, random

N=10
COL=dict(bg="#05070d", grid="#1b2233", text="#cfeaff", a="#21e6ff", b="#ff69d4",
         sea="#0b1221", miss="#39455e", hit="#ff5c5c", sunk="#a31230",
         ship="#58f29b", ghost="#7cc6ff", dock="#0d1530", neon="#7c3aed")
FLEET=[4,3,3,2,2,2,1,1,1,1]

def n8(x,y):
    for dx in(-1,0,1):
        for dy in(-1,0,1):
            if dx==dy==0: continue
            u,v=x+dx,y+dy
            if 0<=u<N and 0<=v<N: yield u,v

class Board:
    def __init__(s): s.g=[[0]*N for _ in range(N)]; s.s=[]
    def can_place(s,x,y,l,h):
        cells=[]
        for i in range(l):
            u,v=(x+i,y) if h else (x,y+i)
            if not(0<=u<N and 0<=v<N) or s.g[v][u]!=0: return False
            cells.append((u,v))
        for cx,cy in cells:
            for ax,ay in n8(cx,cy):
                if s.g[ay][ax]==1: return False
        return True
    def place(s,x,y,l,h):
        if not s.can_place(x,y,l,h): return False
        cur=[]
        for i in range(l):
            u,v=(x+i,y) if h else (x,y+i)
            s.g[v][u]=1; cur.append((u,v))
        s.s.append(set(cur)); return True
    def remove_at(s,x,y):
        for ship in list(s.s):
            if (x,y) in ship:
                for u,v in ship: s.g[v][u]=0
                s.s.remove(ship); return len(ship)
        return 0
    def randomize(s):
        s.__init__()
        for k in FLEET:
            ok=False
            for _ in range(1200):
                h=bool(random.getrandbits(1))
                x=random.randint(0,(N-k) if h else N-1)
                y=random.randint(0,(N-1) if h else (N-k))
                if s.place(x,y,k,h): ok=True; break
            if not ok: return False
        return True
    def shoot(s,x,y):
        c=s.g[y][x]
        if c in(-1,2,3): return "repeat",None
        if c==0: s.g[y][x]=-1; return "miss",None
        s.g[y][x]=2
        for ship in s.s:
            if (x,y) in ship:
                if all(s.g[v][u]==2 for u,v in ship):
                    for u,v in ship: s.g[v][u]=3
                    for u,v in ship:
                        for a,b in n8(u,v):
                            if s.g[b][a]==0: s.g[b][a]=-1
                    return "sunk",ship
                return "hit",ship
        return "miss",None
    def all_sunk(s): return all(all(s.g[v][u]==3 for u,v in ship) for ship in s.s)

class App:
    def __init__(s,root):
        s.r=root; root.title("Космо-морской бой"); root.configure(bg=COL["bg"])
        s.full=True; root.attributes("-fullscreen",True)
        sw,sh=root.winfo_screenwidth(),root.winfo_screenheight()
        s.c=tk.Canvas(root,width=sw,height=sh,bg=COL["bg"],highlightthickness=0); s.c.pack(fill="both",expand=True)
        s.pad=80; s.cell=min((sh-2*s.pad-120)//N, (sw-2*s.pad-240)//(2*N))
        s.left=(s.pad, s.pad+60); s.right=(sw-s.pad - N*s.cell, s.pad+60)
        s.dock_x=(sw//2)-40; s.dock_y=s.pad+60
        s.p, s.e = Board(), Board()
        s.phase="prep"; s.horiz=True; s.drag=None; s.to_place={1:4,2:3,3:2,4:1}
        s.msg=tk.StringVar(value="Перетаскивай корабли из дока. R — поворот, клик по своему кораблю — убрать. F11/ESC — полноэкран.")
        tk.Label(root,textvariable=s.msg,bg=COL["bg"],fg=COL["text"],font=("Segoe UI",12)).place(relx=.5,y=28,anchor="n")
        tb=tk.Frame(root,bg=COL["bg"]); tb.place(relx=.5,rely=1.0,x=0,y=-50,anchor="s")
        tk.Button(tb,text="Случайно",command=s.rand_player).grid(row=0,column=0,padx=6)
        tk.Button(tb,text="Очистить",command=s.clear_player).grid(row=0,column=1,padx=6)
        tk.Button(tb,text="Старт",command=s.start).grid(row=0,column=2,padx=6)
        root.bind("<Button-1>",s.on_down); root.bind("<ButtonRelease-1>",s.on_up)
        root.bind("<Motion>",s.on_move); root.bind("<Key-r>",s.rotate)
        root.bind("<F11>",s.toggle_fs); root.bind("<Escape>",s.exit_fs)
        s.draw()
    def bbox(s,ox,oy,x,y):
        a=ox+x*s.cell; b=oy+y*s.cell; return a,b,a+s.cell,b+s.cell
    def cell_from(s,ox,oy,px,py):
        x=(px-ox)//s.cell; y=(py-oy)//s.cell
        return (x,y) if 0<=x<N and 0<=y<N else None
    def bg(s):
        w=int(s.c["width"]); h=int(s.c["height"])
        for i in range(6):
            x=random.randint(0,w); y=random.randint(0,h)
            r=random.randint(140,240)
            s.c.create_oval(x-r,y-r,x+r,y+r,fill="#0b0f2a",outline="")
        random.seed(2)
        for _ in range(260):
            x=random.randint(0,w); y=random.randint(0,h); r=random.randint(1,2)
            s.c.create_oval(x-r,y-r,x+r,y+r,fill="#9ad7ff",outline="")
        s.c.create_text(w/2,20,fill=COL["b"],text="✦ Stellar Fleet ✦",font=("Segoe UI",18,"bold"))
    def grid(s,ox,oy,cap,accent):
        s.c.create_rectangle(ox-10,oy-10,ox+N*s.cell+10,oy+N*s.cell+10,outline=accent,width=2)
        s.c.create_text(ox+N*s.cell/2,oy-26,fill=accent,font=("Segoe UI",14,"bold"),text=cap)
        for i in range(N):
            s.c.create_text(ox+i*s.cell+s.cell/2,oy-10,fill=COL["text"],text=chr(65+i))
            s.c.create_text(ox-14,oy+i*s.cell+s.cell/2,fill=COL["text"],text=str(i+1))
        for y in range(N):
            for x in range(N):
                x0,y0,x1,y1=s.bbox(ox,oy,x,y)
                s.c.create_rectangle(x0,y0,x1,y1,fill=COL["sea"],outline=COL["grid"])
    def cells(s,b,ox,oy,show):
        for y in range(N):
            for x in range(N):
                v=b.g[y][x]; x0,y0,x1,y1=s.bbox(ox,oy,x,y)
                if show and v==1: s.c.create_rectangle(x0+4,y0+4,x1-4,y1-4,fill=COL["ship"],outline="")
                if v==-1: s.c.create_oval(x0+10,y0+10,x1-10,y1-10,fill=COL["miss"],outline="")
                if v==2:  s.c.create_oval(x0+10,y0+10,x1-10,y1-10,fill=COL["hit"],outline="")
                if v==3:  s.c.create_rectangle(x0+6,y0+6,x1-6,y1-6,fill=COL["sunk"],outline="")
    def dock(s):
        x=s.dock_x; y=s.dock_y; h=N*s.cell
        s.c.create_rectangle(x-60,y-20,x+120,y+h+20,fill=COL["dock"],outline=COL["neon"],width=2)
        s.c.create_text(x+30,y-28,fill=COL["text"],text="Док",font=("Segoe UI",12,"bold"))
        s.pal=[]
        yy=y+10
        for size in (4,3,2,1):
            s.c.create_rectangle(x-40,yy,x+100,yy+28,fill="",outline=COL["grid"])
            for i in range(size):
                s.c.create_rectangle(x-36+i*24,yy+5,x-36+i*24+20,yy+23,fill=COL["ship"],outline="")
            s.c.create_text(x+74,yy+14,fill=COL["text"],text=f"×{s.to_place.get(size,0)}")
            s.pal.append((size,(x-40,yy,x+100,yy+28))); yy+=36
        s.c.create_text(x+30,y+h+28,fill=COL["text"],text="Перетащи →",font=("Segoe UI",10))
    def drag_preview(s):
        if not s.drag: return
        ex,ey=s.last; lx,ly=s.left; cell=s.cell_from(lx,ly,ex,ey)
        if not cell: return
        k=s.drag["size"]; h=s.drag["h"]; ok=s.p.can_place(*cell,k,h)
        for i in range(k):
            u,v=((cell[0]+i,cell[1]) if h else (cell[0],cell[1]+i))
            if 0<=u<N and 0<=v<N:
                x0,y0,x1,y1=s.bbox(lx,ly,u,v)
                s.c.create_rectangle(x0+3,y0+3,x1-3,y1-3,outline=COL["ghost" if ok else "hit"],width=2)
        s.c.create_text(lx+N*s.cell/2,ly-42,fill=COL["text"],
                        text=f"{'Гориз' if h else 'Вертик'} {k}-палубный — {'OK' if ok else 'нельзя'}")
    def draw(s):
        s.c.delete("all"); s.bg()
        lx,ly=s.left; rx,ry=s.right
        s.grid(lx,ly,"Твой сектор",COL["a"]); s.cells(s.p,lx,ly,True)
        s.grid(rx,ry,"Сектор бота",COL["b"]); s.cells(s.e,rx,ry,s.phase!="battle")
        if s.phase=="prep": s.dock(); s.drag_preview()
    def hit_pal(s,x,y):
        for size,(x0,y0,x1,y1) in s.pal:
            if x0<=x<=x1 and y0<=y<=y1: return size
        return None
    def rotate(s,_=None):
        if s.phase!="prep": return
        if s.drag: s.drag["h"]=not s.drag["h"]
        else: s.horiz=not s.horiz
        s.draw()
    def on_down(s,e):
        s.last=(e.x,e.y); lx,ly=s.left
        if s.phase=="prep":
            t=s.cell_from(lx,ly,e.x,e.y)
            if t and s.p.g[t[1]][t[0]]==1:
                got=s.p.remove_at(*t)
                if got: s.to_place[got]=s.to_place.get(got,0)+1; s.draw(); return
            sz=s.hit_pal(e.x,e.y)
            if sz and s.to_place.get(sz,0)>0: s.drag=dict(size=sz,h=s.horiz)
        elif s.phase=="battle":
            t=s.cell_from(s.right[0],s.right[1],e.x,e.y)
            if t: s.player_shoot(*t)
    def on_move(s,e):
        s.last=(e.x,e.y)
        if s.phase=="prep" and s.drag:
            s.draw()
    def on_up(s,e):
        s.last=(e.x,e.y)
        if s.phase!="prep" or not s.drag: return
        t=s.cell_from(s.left[0],s.left[1],e.x,e.y); k=s.drag["size"]; h=s.drag["h"]
        if t and s.p.place(t[0],t[1],k,h): s.to_place[k]-=1
        s.drag=None; s.draw()
    def rand_player(s):
        if s.phase!="prep": return
        while not s.p.randomize(): pass
        s.to_place={1:0,2:0,3:0,4:0}; s.draw()
    def clear_player(s):
        if s.phase!="prep": return
        s.p=Board(); s.to_place={1:4,2:3,3:2,4:1}; s.drag=None; s.draw()
    def start(s):
        if s.phase!="prep": return
        if any(s.to_place.values()): s.msg.set("Расставь все корабли или жми «Случайно»."); return
        while not s.e.randomize(): pass
        s.phase="battle"; s.msg.set("Бой! Кликайте по правому полю.")
        s.ai_targets={(x,y) for y in range(N) for x in range(N)}; s.ai_q=[]; s.draw()
    def player_shoot(s,x,y):
        r,_=s.e.shoot(x,y)
        if r=="repeat": return
        s.draw()
        if s.e.all_sunk(): s.msg.set("Победа!"); s.phase="end"; return
        s.r.after(350, s.ai_turn if r=="miss" else lambda: s.msg.set("Попал! Ходи ещё."))
    def ai_pick(s):
        while s.ai_q:
            t=s.ai_q.pop(0)
            if t in s.ai_targets: return t
        pool=[t for t in s.ai_targets if sum(t)%2==0] or list(s.ai_targets)
        return random.choice(pool)
    def ai_enqueue_cross(s,x,y):
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            u,v=x+dx,y+dy
            if 0<=u<N and 0<=v<N: s.ai_q.append((u,v))
    def ai_turn(s):
        if s.p.all_sunk(): s.msg.set("Бот победил."); s.phase="end"; return
        x,y=s.ai_pick(); s.ai_targets.discard((x,y))
        r,_=s.p.shoot(x,y)
        if r=="hit": s.ai_enqueue_cross(x,y); s.msg.set(f"Бот попал в {chr(65+x)}{y+1} и добивает…"); s.draw(); s.r.after(350,s.ai_turn); return
        if r=="sunk": s.msg.set("Бот потопил корабль!"); s.ai_q.clear(); s.draw(); s.r.after(350,s.ai_turn); return
        s.msg.set("Бот промахнулся. Твой ход."); s.draw()
    def toggle_fs(s,_=None):
        s.full=not s.full; s.r.attributes("-fullscreen",s.full)
    def exit_fs(s,_=None):
        s.full=False; s.r.attributes("-fullscreen",False)

if __name__=="__main__":
    random.seed(); tk.Tk.report_callback_exception=lambda *a,**k: None
    r=tk.Tk(); r.configure(bg=COL["bg"]); App(r); r.mainloop()
