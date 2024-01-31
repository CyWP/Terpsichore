from customtkinter import (CTkTabview,
                           CTkLabel)

TABS = ('Play',
        'Record',
        'View',
        'Input',
        'Manage',
        'Train',
        'Help')

class TabGen(CTkTabview):

    def __init__(self,
                 master,
                 tabs,
                 orientation='h',
                 padx=20,
                 pady=10,
                 **kwargs):
        super().__init__(master, **kwargs)

        horizontal = (orientation=='h')
        vertical = not horizontal

        for i, tabname in enumerate(tabs):
            self.add(tabname)
            self.label = CTkLabel(master=self.tab(tabname))
            self.label.grid(row=vertical*i, column=horizontal*i, padx=padx, pady=pady)

