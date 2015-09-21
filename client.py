from Tkinter import *             #GUI
from socket import *              #socket 
from threading import *           #threading
from ScrolledText import*         #Scroll pada text

class Receive():
  def __init__(self, server, gettext):
    self.server = server
    self.gettext = gettext
    while 1:
      try:
        text = self.server.recv(1024)
        if not text: break
        self.gettext.configure(state=NORMAL)
        self.gettext.insert(END,'Server >> %s\n'%text)
        self.gettext.configure(state=DISABLED)
        self.gettext.see(END)
      except:
        break
class App(Thread):
  client = socket()
  print ("CLIENT")
  client.connect((input("IP Server: "), input("Port: ")))
  def __init__(self, master):
    Thread.__init__(self)
    frame = Frame(master)
    frame.pack()
    self.gettext = ScrolledText(frame, height=10,width=100)
    self.gettext.pack()
    self.gettext.insert(END,'Welcome to Chat\n')
    self.gettext.configure(state=DISABLED)
    sframe = Frame(frame)
    sframe.pack(anchor='w')
    self.pro = Label(sframe, text="Client>>");
    self.sendtext = Entry(sframe,width=80)
    self.sendtext.focus_set()
    self.sendtext.bind(sequence="<Return>", func=self.Send)
    self.pro.pack(side=LEFT)
    self.sendtext.pack(side=LEFT)
    
  def Send(self, args):
    self.gettext.configure(state=NORMAL)
    text = self.sendtext.get()
    if text=="": text=" "
    self.gettext.insert(END,'Me >> %s\n'%text)
    self.sendtext.delete(0,END)
    self.client.send(text)
    self.sendtext.focus_set()
    self.gettext.configure(state=DISABLED)
    self.gettext.see(END)

    def sendFile(self,sock,file):
        sock.send(filFlag)
        user = os.environ['USER']
        command = filFlag
        size = os.stat(file)[6]
        f = open(file,'r')
        pos = 0
        while 1:
            if pos == 0:
                buffer = f.read(5000000-282)
                if not buffer: break
                count = sock.send(command + ':' + \
                string.rjust(os.path.basename(file),214) + ':' + \
                string.rjust(str(size).strip(),30) + ':' + \
                string.rjust(str(user).strip(),30) + \
                buffer)
                pos = 1
            else:
                buffer = f.read(5000000)
                if not buffer: break
                count = sock.send(buffer)

    def recvFile(self,sock):
        pjg = 0
        msg1 = sock.recv(283).split(':')
        flag = msg1[0].strip()
        namafile = msg1[1].strip()
        total = msg1[2].strip()
        user = msg1[3].strip()
        file = namafile

        if flag == filFlag:
            try:
                f = open(file,'w')
            except:
                ret = 0
                print 'Tidak dapat menyimpan file'
                sys.exit()
            else:
                try:
                    while 1:
                        leftToRead = int(total) - pjg
                        if not leftToRead: break
                        msg = sock.recv(5000000)
                        pjg = pjg + len(msg)
                        f.write(msg)
                        os.system('echo -n !')
                        f.close()
                except:
                    os.remove(file)
                    ret = 0
                else:
                    ret = 1

  def run(self):
    Receive(self.client, self.gettext)
    
root = Tk()                 #buat form
root.title('Client Chat')   #definisikan title
app = App(root).start()     #Buat class app dengan inisiasi awal, kmudian start(run)
root.mainloop()             #loop untuk root (GUI Aplikasi TKinter)
