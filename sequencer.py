#python 3.5.1
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

#flashing lights = transcription factors
#sigma is one example of a transcription factor

class Application(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.frames = {}
        
        container = tk.Frame(self)

        self.title("DNA Tool")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        frame = StartPage(container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames[StartPage] = frame

        frame = SequencePage(container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames[SequencePage] = frame

        self.show_frame(StartPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        logoPhoto = tk.PhotoImage(file="./dna-helix.gif")
        logoLabel = tk.Label(self, image=logoPhoto)
        logoLabel.image = logoPhoto
        logoLabel.pack(side="top")
        
        sequenceButton = tk.Button(self, text="Find Sequence Motifs",
                                   command=self.goToSequencePage)
        sequenceButton.pack()

    def goToSequencePage(self):
        self.controller.show_frame(SequencePage)
        

class SequencePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)
        self.columnconfigure(4, pad=3)
        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)

        self.homeButton = tk.Button(self, text="Back to Home", command=self.goHome)
        self.homeButton.grid(row=0, column=0, sticky="nsew")

        self.analyzeButton = tk.Button(self, text="Analyze",command=self.analyze)
        self.analyzeButton.grid(row=1, column=0, sticky="nsew")


        self.getFileButton = tk.Button(self, text="Add File", command=self.addFile)
        self.getFileButton.grid(row=2, column=0, sticky="nsew")

        self.files = {}
        self.currentFile = ""
        self.fileListbox = tk.Listbox(self, relief="ridge", height=10, width=60)
        self.fileListbox.grid(rowspan=3, row=0, column=1, sticky="nsew")
        self.fileListbox.bind('<<ListboxSelect>>', self.getFileSelection)

        self.sortFilesAZButton = tk.Button(self, text="⬆", command=self.sortFilesAZ)
        self.sortFilesAZButton.grid(row=0, column=4, sticky="nsew")
        
        self.sortFilesZAButton = tk.Button(self, text="⬇", command=self.sortFilesZA)
        self.sortFilesZAButton.grid(row=1, column=4, sticky="nsew")

        self.enteredText = ""
        self.dnaText = tk.Text(self, relief="ridge", height=10, width=40, borderwidth=1)
        self.dnaText.grid(row=3, column=0, columnspan=4, sticky="nsew")
        #scrollb = tk.Scrollbar(self, command=self.dnaText.yview)
        #scrollb.grid(row=0, column=1, sticky='nsew')
        #self.dnaText.yscrollcommand = scrollb.set

        self.letterCount = tk.Label(self, text="Count:")
        self.letterCount.grid(row=4, column=1, sticky="nsew")

    def goHome(self):
        self.controller.show_frame(StartPage)

    def analyze(self):
        print("analyzing..." + self.getDNAText())

    def setDNAText(self, text):
        self.dnaText.delete(1.0, "end")
        self.dnaText.insert("end", text)
        self.enteredText = text
        
    def getDNAText(self):
        self.enteredText = self.dnaText.get('1.0', 'end-1c')
        return self.enteredText

    def selectFile(self, fullPath):
        if self.currentFile != fullPath:
            self.currentFile = fullPath
            try:
                text = open(fullPath).read().strip()
                self.letterCount['text'] = 'Count: ' + str(len(text))
                if len(text) <= 500:
                    self.setDNAText(text)
                else:
                    self.setDNAText(text[:500])
            except:
                messagebox.showerror("File Error", "Could not read file: \n%s" % fullPath)

    def getFileSelection(self, event):
        w = event.widget
        if w.curselection() != ():
            index = int(w.curselection()[0])
            value = w.get(index)
            fullPath = value.split("~>")[-1]
            self.selectFile(fullPath)

    def addFile(self):
        fullPath = filedialog.askopenfilename(filetypes=[("Text files","*.txt")])
        if fullPath:
            shortName = fullPath.split("/")[-1]
            self.files[fullPath] = {"FullPath" : fullPath, "ShortName" : shortName}

            descriptor = shortName+ " ~>" + fullPath
            self.fileListbox.insert("end", descriptor)               
            self.selectFile(fullPath)
        else:
            print("no file selected")

    def sortFilesAZ(self):
        self.fileListbox.delete(0, "end")
        l = []
        for key in self.files.keys():
            fileInfo = self.files[key]
            l.append( (fileInfo["ShortName"], fileInfo["FullPath"]) )
        l.sort()
        for tup in l:
            descriptor = tup[0] + " ~>" + tup[1]
            self.fileListbox.insert("end", descriptor)
        

    def sortFilesZA(self):
        self.fileListbox.delete(0, "end")
        l = []
        for key in self.files.keys():
            fileInfo = self.files[key]
            l.append( (fileInfo["ShortName"], fileInfo["FullPath"]) )
        l.sort()
        for tup in reversed(l):
            descriptor = tup[0] + " ~>" + tup[1]
            self.fileListbox.insert("end", descriptor)

class FileReader():
    def __init__(self, text, docType):
        self.text = text
    

def main():
    app = Application()
    app.geometry("650x400+600+100")
    app.mainloop()

main()
