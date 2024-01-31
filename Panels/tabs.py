from customtkinter import (CTkTabview,
                           CTkLabel,
                           CTkButton)

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
                 font,
                 homebutton = None,
                 orientation='h',
                 padx=20,
                 pady=10,
                 **kwargs):
        super().__init__(master, **kwargs)

        horizontal = (orientation=='h')
        vertical = not horizontal

        if homebutton is not None:
            self.add(homebutton['text'])
            self._segmented_button._buttons_dict[homebutton['text']].configure(font=homebutton['font'],
                                                                               bg_color='transparent')

        for i, tabname in enumerate(tabs):
            self.add(tabname)
            self._segmented_button._buttons_dict[tabname].configure(font=font)
            self.label = CTkLabel(master=self.tab(tabname),
                                  text=tabname,
                                  font=font,)
            self.label.grid(row=vertical*i,
                            column=horizontal*i,
                            padx=padx, pady=pady)

