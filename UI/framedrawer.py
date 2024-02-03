from customtkinter import (CTkFrame,
                           CTkLabel)
from .customclasses import (Button,
                           ConsciousFrame)
from CTkTable import *


def clearFrame(master, state):
    if master is ConsciousFrame:
        if master.state==state:
            return False
        master.state = state
    for widget in master.winfo_children():
          widget.destroy() 
    return True  


def drawHomeFrame(master):

    if(clearFrame(master, 'Home')):
    
        Button(master, type='BIG', text='NEW').pack(anchor='sw', side='bottom')
        Button(master, type='BIG', text='LOAD').pack(anchor='sw', side='bottom')
        Button(master, type='BIG', text='LAST').pack(anchor='sw', side='bottom')

def drawMoveFrame(master:CTkFrame):
    
    if(clearFrame(master, 'Move')):
    
        Button(master, type='BIG', text='NEW').pack(anchor='sw', side='bottom')
        Button(master, type='BIG', text='LOAD').pack(anchor='sw', side='bottom')
        Button(master, type='BIG', text='LAST').pack(anchor='sw', side='bottom')

def drawTraceFrame(master:CTkFrame):
    
    if(clearFrame(master, 'Trace')):
    
        Button(master, type='BIG', text='NEW').pack(anchor='sw', side='bottom')
        Button(master, type='BIG', text='LOAD').pack(anchor='sw', side='bottom')
        Button(master, type='BIG', text='LAST').pack(anchor='sw', side='bottom')

def drawViewFrame(master:CTkFrame):
    
    if(clearFrame(master, 'View')):
    
        Button(master, type='BIG', text='NEW').pack(anchor='sw', side='bottom')
        Button(master, type='BIG', text='LOAD').pack(anchor='sw', side='bottom')
        Button(master, type='BIG', text='LAST').pack(anchor='sw', side='bottom')

def drawInputFrame(master:CTkFrame):
    
    if(clearFrame(master, 'Input')):
    
        Button(master, type='BIG', text='NEW').pack(anchor='sw', side='bottom')
        Button(master, type='BIG', text='LOAD').pack(anchor='sw', side='bottom')
        Button(master, type='BIG', text='LAST').pack(anchor='sw', side='bottom')

def drawDataFrame(master:CTkFrame):
    
    if(clearFrame(master, 'Data')):
    
        Button(master, type='BIG', text='NEW').pack(anchor='sw', side='bottom')
        Button(master, type='BIG', text='LOAD').pack(anchor='sw', side='bottom')
        Button(master, type='BIG', text='LAST').pack(anchor='sw', side='bottom')

def drawTrainFrame(master:CTkFrame):
    
    if(clearFrame(master, 'Train')):
    
        Button(master, type='BIG', text='NEW').pack(anchor='sw', side='bottom')
        Button(master, type='BIG', text='LOAD').pack(anchor='sw', side='bottom')
        Button(master, type='BIG', text='LAST').pack(anchor='sw', side='bottom')