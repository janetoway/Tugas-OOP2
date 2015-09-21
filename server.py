from Tkinter import *             #GUI
from socket import *              #socket 
from threading import *           #threading
from ScrolledText import*         #Scroll pada text

class Receive():                                         #class menerima data
  def __init__(self, server, gettext,client):
    self.server = server
    self.gettext = gettext
    self.client = client
    while 1:
      try:
        text = self.server.recv(1024)
        if not text: break
        self.gettext.configure(state=NORMAL)
        self.gettext.insert(END,'client >> %s\n'%text)    #isi teks di akhir textbox
        self.gettext.configure(state=DISABLED)
        self.gettext.see(END)                             #tempatkan di akhir
        data = text
        # echo back the client message
        if data == '1':
           filename='file_a.txt'
           f = open(filename,'rb')
           l = f.read(1024)
           f.close()
           content = "file_a.txt content : \n------------\n"+l+"\n------------"
           self.client.send(content)
        elif data == '2':
           filename='file_b.txt'
           f = open(filename,'rb')
           l = f.read(1024)
           f.close()
           content = "file_b.txt content : \n------------\n"+l+"\n------------"
           self.client.send(content)
        else :
           self.client.send("your mesasage accepted, \n> type '1' to open file_a.txt \n> type '2' to open file_b.txt ")               

      except:
        break
class App(Thread):
  server = socket()
  print ("SERVER")
  server.bind((input("IP Client: "), input("Port: ")))
  server.listen(5)
  client,addr = server.accept()
  def __init__(self, master):
    Thread.__init__(self)
    frame = Frame(master)
    frame.pack()
    self.gettext = ScrolledText(frame, height=10,width=100, state=NORMAL)
    self.gettext.pack()
    sframe = Frame(frame)
    sframe.pack(anchor='w')
    self.pro = Label(sframe, text="Server>>");
    self.sendtext = Entry(sframe,width=80)
    self.sendtext.focus_set()
    self.sendtext.bind(sequence="<Return>", func=self.Send)
    self.pro.pack(side=LEFT)
    self.sendtext.pack(side=LEFT)
    self.gettext.insert(END,'Welcome to Chat\n')
    self.gettext.configure(state=DISABLED)
    
  def Send(self, args):
    self.gettext.configure(state=NORMAL)
    text = self.sendtext.get()
    if text=="": text=" "
    self.gettext.insert(END,'Me >> %s \n'%text)
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
        try:
            f = open(file,'r')
        except:
            ret = 0
        else:
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
                ret = 1
            return ret

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
                else:
                    try:
                        while 1:
                            leftToRead = int(total) - pjg
                            if not leftToRead: break
                            msg = sock.recv(5000000)
                            pjg = pjg + len(msg)
                            f.write(msg)
                        f.close()
                    except:
                        os.remove(file)
                        ret = 0
                    else:
                        ret = 1
                    ret = 1
                return ret

  def run(self):
    Receive(self.client, self.gettext,self.client)  #buat class menerima data
    
root = Tk()                 #buat form
root.title('Server Chat')   #definisikan title
app = App(root).start()     #Buat class app dengan inisiasi awal, kmudian start(run)
root.mainloop()             #loop untuk root (GUI Aplikasi TKinter)
