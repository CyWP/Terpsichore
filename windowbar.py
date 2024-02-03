from customtkinter import(CTkFrame,
                          CTkLabel)
from button import Button

class TitleBar(CTkFrame):
    def __init__(self, parent, bg):
        self.root = parent
        #self.root.overrideredirect(True) # For Remove Default Title Bar
        super().__init__(parent)

        self.root.configure(background=bg)
        
        '''Button(self, text='✕', type='TAB', cursor="hand2", command=self.close_window).pack(side="right")
        self.bind("<ButtonPress-1>", self.oldxyset)
        self.bind("<B1-Motion>", self.move)

        Button(self, text='—', type='TAB', cursor="hand2", command=self.minimize).pack(side="right")
        self.bind("<ButtonPress-1>", self.oldxyset)
        self.bind("<B1-Motion>", self.move)'''

        Button(self, text='File', type='TAB', cursor="hand2", command=self.close_window).pack(side="left", fill='both', expand=True)
        #self.bind("<ButtonPress-1>", self.oldxyset)
        #self.bind("<B1-Motion>", self.move)

        Button(self, text='Settings', type='TAB', cursor="hand2", command=self.close_window).pack(side="left", fill='both', expand=True)
        #self.bind("<ButtonPress-1>", self.oldxyset)
        #self.bind("<B1-Motion>", self.move)
        Button(self, text='Help', type='TAB', cursor="hand2", command=self.close_window).pack(side="left", fill='both', expand=True)

        Button(self, text='Documentation', type='TAB', cursor="hand2", command=self.close_window).pack(side="right", fill='both', expand=True)
        #self.bind("<ButtonPress-1>", self.oldxyset)
        #self.bind("<B1-Motion>", self.move)

    def oldxyset(self, event):
        self.oldx = event.x 
        self.oldy = event.y

    def oldxyset_label(self, event):
        self.oldx = event.x + self.nav_title.winfo_x()
        self.oldy = event.y + self.nav_title.winfo_y()
        
    def move(self, event):
        self.y = event.y_root - self.oldy
        self.x = event.x_root - self.oldx
        self.root.geometry(f"+{self.x}+{self.y}")
    
    def close_window(self):
        self.root.destroy()

    def minimize(self):
        self.root.update_idletasks()
        self.root.overrideredirect(False)
        self.root.withdraw()
        self.root.state('iconic')

    