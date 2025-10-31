import tkinter as tk, random
from collections import deque

CELLS=8
TILE=32
NEI=[(-1,0),(0,1),(1,0),(0,-1)]
STEP=6
FRAME=12

def build(c):
    n=2*c+1
    g=[[1]*n for _ in range(n)]
    R=C=c
    seen=[[False]*C for _ in range(R)]
    r=c//2; k=c//2
    st=[(r,k)]; seen[r][k]=True; g[2*r+1][2*k+1]=0
    while st:
        r,k=st[-1]
        q=[]
        for dr,dc in NEI:
            nr,nc=r+dr,k+dc
            if 0<=nr<R and 0<=nc<C and not seen[nr][nc]:
                q.append((dr,dc,nr,nc))
        if q:
            dr,dc,nr,nc=random.choice(q)
            g[2*r+1+dr][2*k+1+dc]=0
            g[2*nr+1][2*nc+1]=0
            seen[nr][nc]=True
            st.append((nr,nc))
        else:
            st.pop()
    for _ in range(200):
        s=random.choice("NSWE")
        if s=="N":
            x=2*random.randrange(C)+1
            if g[1][x]==0: g[0][x]=0; break
        if s=="S":
            x=2*random.randrange(C)+1
            if g[2*R-1][x]==0: g[2*R][x]=0; break
        if s=="W":
            y=2*random.randrange(R)+1
            if g[y][1]==0: g[y][0]=0; break
        if s=="E":
            y=2*random.randrange(R)+1
            if g[y][2*C-1]==0: g[y][2*C]=0; break
    return g

class Stellar(tk.Tk):
    def __init__(s):
        super().__init__()
        s.N=2*CELLS+1
        s.configure(bg="#050816")
        s.title("Stellar Maze • DFS")
        tk.Label(s,text="Stellar Maze",font=("Arial",18,"bold"),bg="#050816",fg="#d5e8ff").pack(pady=(8,0))
        bar=tk.Frame(s,bg="#050816"); bar.pack(fill="x",pady=(2,8))
        mk=lambda t,cmd: tk.Button(bar,text=t,command=cmd,bg="#0d1222",fg="#cfe2ff",activebackground="#16213a",bd=0,padx=12,pady=6)
        mk("Новый",s.new).pack(side="left",padx=4)
        mk("Старт",s.start).pack(side="left",padx=4)
        mk("Сброс",s.reset).pack(side="left",padx=4)
        s.info=tk.StringVar(value="Готово.")
        tk.Label(bar,textvariable=s.info,bg="#050816",fg="#8fb6ff").pack(side="right",padx=8)
        s.cv=tk.Canvas(s,width=s.N*TILE,height=s.N*TILE,highlightthickness=0,bg="#050816"); s.cv.pack()
        s.g=[[1]*s.N for _ in range(s.N)]
        s.rect=[[None]*s.N for _ in range(s.N)]
        s.start_cell=(s.N//2,s.N//2)
        s.exits=[]
        s.robot=None
        s.robot_dir=(0,-1)
        s.vis=set()
        s.path=[]
        s.probe={}
        s.run=False
        s.fin=False
        s.new()
        s.bind("<space>",lambda e:s.start())
        s.bind("r",lambda e:s.new())

    def starfield(s,count=300):
        for _ in range(count):
            x=random.randint(0,s.N*TILE-2); y=random.randint(0,s.N*TILE-2)
            r=random.choice((1,1,1,2))
            col=random.choice(("#ffffff","#dfe6ff","#bcd7ff","#b0f0ff"))
            s.cv.create_oval(x,y,x+r,y+r,fill=col,outline="")

    def new(s):
        if s.run: return
        s.fin=False; s.vis.clear(); s.path.clear(); s.probe.clear()
        s.g=build(CELLS)
        s.exits=[(r,c) for r in range(s.N) for c in range(s.N) if s.g[r][c]==0 and (r in (0,s.N-1) or c in (0,s.N-1))]
        s.cv.delete("all"); s.robot=None
        s.starfield(300)
        for r in range(s.N):
            for c in range(s.N):
                x0,y0=c*TILE,r*TILE; x1,y1=x0+TILE,y0+TILE
                if s.g[r][c]==1:
                    s.rect[r][c]=s.cv.create_rectangle(x0,y0,x1,y1,fill="#1a1740",outline="#5132ff")
                else:
                    s.rect[r][c]=s.cv.create_rectangle(x0,y0,x1,y1,fill="",outline="")
        if s.g[s.start_cell[0]][s.start_cell[1]]==1:
            t=s.nearest(s.start_cell)
            if t: s.start_cell=t
        s.path=[s.start_cell]
        s.place(s.start_cell,True)
        s.info.set(f"Старт: {s.start_cell}; выходов: {len(s.exits)}. SPACE=старт, R=новый.")

    def nearest(s,orig):
        sr,sc=orig; seen={(sr,sc)}; q=deque([(sr,sc)])
        while q:
            r,c=q.popleft()
            if s.g[r][c]==0: return (r,c)
            for dr,dc in NEI:
                nr,nc=r+dr,c+dc
                if 0<=nr<s.N and 0<=nc<s.N and (nr,nc) not in seen:
                    seen.add((nr,nc)); q.append((nr,nc))

    def center(s,rc):
        r,c=rc; return (c*TILE+TILE/2,r*TILE+TILE/2)

    def ship_points(s,center,vec,size):
        cx,cy=center; dx,dy=vec
        if (dx,dy)==(0,-1):
            return (cx,cy-size,cx-size*0.75,cy+size*0.8,cx+size*0.75,cy+size*0.8)
        if (dx,dy)==(1,0):
            return (cx+size,cy,cx-size*0.8,cy-size*0.7,cx-size*0.8,cy+size*0.7)
        if (dx,dy)==(0,1):
            return (cx,cy+size,cx-size*0.75,cy-size*0.8,cx+size*0.75,cy-size*0.8)
        return (cx-size,cy,cx+size*0.8,cy-size*0.7,cx+size*0.8,cy+size*0.7)

    def place(s,cell,new=False):
        cx,cy=s.center(cell); size=TILE*0.35
        if s.robot is None or new:
            aura=s.cv.create_oval(cx-size*1.1,cy-size*1.1,cx+size*1.1,cy+size*1.1,fill="#0b1f3f",outline="")
            ship=s.cv.create_polygon(s.ship_points((cx,cy),s.robot_dir,size*0.9),fill="#7de2ff",outline="")
            s.robot=(ship,aura,(cx,cy)); return
        ship,aura,_=s.robot
        s.cv.coords(aura,cx-size*1.1,cy-size*1.1,cx+size*1.1,cy+size*1.1)
        s.cv.coords(ship,*s.ship_points((cx,cy),s.robot_dir,size*0.9))
        s.robot=(ship,aura,(cx,cy))

    def reset(s):
        if s.run: return
        s.vis.clear(); s.path=[s.start_cell]; s.probe.clear(); s.fin=False
        for r in range(s.N):
            for c in range(s.N):
                if s.g[r][c]==1:
                    s.cv.itemconfig(s.rect[r][c],fill="#1a1740",outline="#5132ff")
                else:
                    s.cv.itemconfig(s.rect[r][c],fill="",outline="")
        s.place(s.start_cell)
        s.info.set("Сброшено.")

    def start(s):
        if s.run or s.fin: return
        if s.g[s.start_cell[0]][s.start_cell[1]]==1:
            s.info.set("Старт в стене. Нажмите «Новый»."); return
        s.run=True; s.info.set("DFS...")
        s.tick()

    def tick(s):
        if not s.run: return
        cur=s.path[-1]
        if cur not in s.vis:
            s.vis.add(cur)
            if cur!=s.start_cell and s.g[cur[0]][cur[1]]==0:
                s.cv.itemconfig(s.rect[cur[0]][cur[1]],fill="#0c142b")
        if cur in s.exits and cur!=s.start_cell:
            s.run=False; s.fin=True; s.draw_path(s.path); s.info.set(f"Выход: {cur}"); return
        idx=s.probe.get(cur,0)
        for j in range(idx,len(NEI)):
            s.probe[cur]=j+1
            dr,dc=NEI[j]; nr,nc=cur[0]+dr,cur[1]+dc
            if 0<=nr<s.N and 0<=nc<s.N and s.g[nr][nc]==0 and (nr,nc) not in s.vis:
                nxt=(nr,nc); s.path.append(nxt); s.robot_dir=(dc,dr) if (dc,dr)!=(0,0) else s.robot_dir
                s.move_to(nxt,lambda:s.after(FRAME,s.tick)); return
        if len(s.path)>1:
            prev=s.path[-2]; s.robot_dir=(prev[1]-cur[1],prev[0]-cur[0]); s.path.pop()
            s.move_to(prev,lambda:s.after(FRAME,s.tick)); return
        s.run=False; s.fin=True; s.info.set("Путь не найден.")

    def move_to(s,target,cb):
        if s.robot is None: s.place(target,True); cb(); return
        ship,aura,(cx,cy)=s.robot
        tx,ty=s.center(target)
        dx=1 if tx>cx else -1 if tx<cx else 0
        dy=1 if ty>cy else -1 if ty<cy else 0
        if (dx,dy)==(0,0): cb(); return
        m=min(STEP,abs(tx-cx) if dx!=0 else abs(ty-cy))
        nx=cx+m*dx; ny=cy+m*dy
        size=TILE*0.35
        s.cv.coords(aura,nx-size*1.1,ny-size*1.1,nx+size*1.1,ny+size*1.1)
        s.cv.coords(ship,*s.ship_points((nx,ny),s.robot_dir,size*0.9))
        s.robot=(ship,aura,(nx,ny))
        s.after(FRAME,lambda:s.move_to(target,cb))

    def draw_path(s,path):
        for i in range(1,len(path)):
            x0,y0=s.center(path[i-1]); x1,y1=s.center(path[i])
            s.cv.create_line(x0,y0,x1,y1,fill="#ffd860",width=6,capstyle=tk.ROUND)
        s.place(path[-1])

if __name__=="__main__":
    Stellar().mainloop()
