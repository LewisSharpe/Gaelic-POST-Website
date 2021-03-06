#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import csv
import itertools
import glob
import codecs
import nltk
from nltk.tag.brill   import BrillTagger
import numpy
from nltk.tokenize import word_tokenize
import sys
from nltk.util import ngrams
from nltk.corpus import brown
from nltk.tag import UnigramTagger
from nltk.tag.brill import *
import random
from decimal import *
from collections import OrderedDict
import ast
from tkinter import *
from tkinter.ttk import *
import time
import pickle 

myGui = Tk()
myGui.inputFile = ''
myGui.tokenisedFile =''
myGui.taggerFile =''
myGui.directory =''
myGui.directory1 =''
myGui.time2 = time.strftime("%d%m%Y")
myGui.tracker = StringVar()
w, h = myGui.winfo_screenwidth(), myGui.winfo_screenheight()
myGui.text = Text(myGui, width=int(w/5), height=int(h/20), wrap=WORD)
myGui.currentdir = os.getcwd()
myGui.defaultModel =''
myGui.simplifiedModel =''
myGui.filename1 = ''
myGui.filename2 = ''
#myGui.englishLexicon  = list(csv.reader(codecs.open(r'C:\ScottishGaelicProject\TestSystem\data\EnglishLexiconFinal06082014.csv','r')))
myGui.englishLexicon  = list(csv.reader(codecs.open(os.path.join(os.getcwd(), 'data', 'EnglishLexiconFinal06082014.csv'),'r')))

def about():
   # messagebox.showwarning(title="About", message="This PoS Tagger is under development and ready to be used for research purposes")
    abtFile = codecs.open(os.path.join(os.getcwd(), 'data', 'AboutFile14112014.txt') ,'r', 'utf-8-sig').readlines()
    #abtFile = codecs.open('C:\ScottishGaelicProject\TestSystem\data\AboutFile14112014.txt' ,'r', 'utf-8-sig').readlines()
    myGui.text.delete(1.0, END)
    for abtline in abtFile:
         myGui.text.insert(INSERT, abtline)
    
    return

def helpfile():
   # messagebox.showwarning(title="About", message="This PoS Tagger is under development and ready to be used for research purposes")
    helpFile = codecs.open(os.path.join(os.getcwd(), 'data', 'HelpFile14112014.txt') ,'r', 'utf-8-sig').readlines()
    #helpFile = codecs.open('C:\ScottishGaelicProject\TestSystem\data\HelpFile14112014.txt' ,'r', 'utf-8-sig').readlines()
    myGui.text.delete(1.0, END)
    for helpline in helpFile:
         myGui.text.insert(INSERT, helpline)
    
    return

def mquit():
    mclose = messagebox.askyesno(title="Close", message="Do you want to close program")
    if mclose>0:
        myGui.destroy()
    return

def mopenfiles():
    gPoS = GaelicSentenceSplitter()
    myGui.filename= filedialog.askopenfilename(filetypes= (('Text Files','*.txt'),('','')))
    if myGui.filename:
         myGui.inputFile = gPoS.readinputfile(codecs.open(myGui.filename, 'r', 'utf-8-sig'))
         myGui.tracker.set('File: ' +  myGui.filename + ' is open')
        
    else:
         messagebox.showerror(title="Error", message="No input file supplied..please supply an input file")
    return myGui.inputFile


def tokenisefile():
        tk = GaelicTokeniser()
        if myGui.inputFile:
            refresh()
            myGui.tracker.set('Status: please wait..tokeniser in progress')
            myGui.myprogressbar.update_idletasks()
            myGui.tokenisedFile = tk.tokenise(myGui.inputFile)
            myGui.tracker.set('Status: tokeniser complete..')   
            myGui.text.insert(INSERT, myGui.tokenisedFile)
            savefile(myGui.tokenisedFile)
            myGui.tracker.set('')   
           
        else:
             messagebox.showerror(title="Error", message="No input file supplied..please supply an input file")
  
        return


def LoadDefaultModel():
   dModel = open(os.path.join(os.getcwd(), 'model', 'DefualtModel.pkl'),"rb")
   #dModel = open('C:\ScottishGaelicProject\TestSystem\model\DefualtModel.pkl',"rb")
   model = pickle.load(dModel)
   dModel.close()
   return model

def LoadSimplifiedModel():
   sModel = open(os.path.join(os.getcwd(), 'model', 'SimplifiedModel.pkl'),"rb")
   #sModel = open('C:\ScottishGaelicProject\TestSystem\model\SimplifiedModel.pkl',"rb")
   model = pickle.load(sModel)
   sModel.close()
   return model




def tagfile_Default():
        tk = GaelicTokeniser()
        algT=[]
        algV=[]
        myGui.tokenisedFile =''
        if myGui.inputFile :
                      refresh()
                      myGui.tracker.set('Status: please wait..default tagging in progress')
                      myGui.myprogressbar.update_idletasks() ## to hold status infor on screen till end of process
                    # myGui.taggerFile = tagger.tagDefault(tk.tokenise(myGui.inputFile))
                      defmodel = LoadDefaultModel()
                      BrillTag = defmodel.tag(tk.tokenise(myGui.inputFile))

                      for (c, d) in BrillTag: # algorithm output
                                algT.append(c)
                                algV.append(d)

                      Sp= ["Spv", "Spp3sm", "Spp3sf", "Spp3p", "Spp1s", "Spa-s", "Spa-p", "Spa", "Sp"]

 
                      for x, b in enumerate(algV):
                                   
                                                
                                    Nouncasesd = re.findall(r"(\bN+.*d\b)", str(b))
                                    Nouncasesn = re.findall(r"(\bN+.*n\b)", str(b))
                                    Nouncasesg = re.findall(r"(\bN+.*g\b)", str(b))

                                    temp = []
                                    temp2 = []
                                    temp.append(''.join(algV[x-1])) 
                                    temp.append(''.join(algV[x-2]))
                                    temp.append(''.join(algV[x-3]))

                                         
                                    tp = (set(temp) & set(Sp))
                                    tp2 = (set(temp2) & set(Sp))
                                       
                                    if (Nouncasesd and not tp) :
                                                nc = ''.join(Nouncasesd)
                                                cc = re.findall(r"\S",str(nc))
                                                cca =cc[:len(cc)-1]
                                                cca.extend('n')
                                                algV[x]= ''.join(cca)
                                         

                                    if (Nouncasesg and not tp) :
                                                ng = ''.join(Nouncasesg)
                                                cc = re.findall(r"\S",str(ng))
                                                cca =cc[:len(cc)-1]
                                                cca.extend('d')
                                                algV[x]= ''.join(cca)
                                             
           
                                    if ''.join(b)=='Sp' and 'Ug' in algV[x+3]:
                                         algV[x]= 'Sa'
                                                                           
                                        

                      for y, c in enumerate(algT):
                            for x, b in enumerate(algV):
                                if x==y:
                                     for d in myGui.englishLexicon :
                                            if str(''.join(d)).lower() == c and c not in ['air','shine', 'gun','sin', 'far', 'fear', 'a', 'can'] and b!='Xfe':
                                                    algV[x]='Xfe'

                                     Verbcases = ''.join(re.findall(r"(\bV+.*\b)", str(b)))
                                     Wcases = ''.join(re.findall(r"(\bW+.*\b)", str(b)))


                                     if str(''.join(c)) in ['Sann','sann',"'sann"]:
                                         algV[x]='Wp-i-x'

                                     if ''.join(b) =='Sap3sf' and ''.join(algT[y+1][:2]) in ['ph','bh','ch','th','dh','mh','sh','fh']:
                                        algV[x]='Sap3sm'

                                     if ''.join(b)=='Sap3sm' and ''.join(algT[y+1][:2]) in ['pa','pe', 'pi', 'po', 'pu', 'pl', 'pm', 'pn','ba','be', 'bi', 'bo', 'bu', 'bl', 'bm', 'bn', 'ca','ce', 'ci', 'co', 'cu', 'cl', 'cm', 'cn','ga','ge', 'gi', 'go', 'gu', 'gl', 'gm', 'gn','ta','te', 'ti', 'to', 'tu', 'tl', 'tm', 'tn','da','de', 'di', 'do', 'du', 'dl', 'dm', 'dn','ma','me', 'mi', 'mo', 'mu', 'ml', 'mm', 'mn','sa','se', 'si', 'so', 'su', 'sl', 'sm', 'sn','fa','fe', 'fi', 'fo', 'fu', 'fl', 'fm', 'fn']:
                                        algV[x]='Sap3sf'
            
                                     if ''.join(b)=='Sap3sm' and ''.join(algT[y+1][:1])=='h-':
                                        algV[x]='Sap3sf'

                                     if ''.join(algT[y])=="an" and ''.join(algT[y+1])=='sàs':
                                        algV[x]='Sp'
                                        algV[x+1]='Ncsmd'


                                     if ''.join(algT[y]) in ["nam", "nan"] and ''.join(algV[x+1])== Verbcases:
                                        algV[x]='Q-s'

                                     if ''.join(algT[y])=='a' and ''.join(algV[x+1])== Verbcases:
                                        algV[x]='Q-r'


                                     if ''.join(algT[y])=='na' and ''.join(algV[x-1])== "Sp":
                                        algV[x]='Tdpm'


                                     if ''.join(algT[y])=='am' and ''.join(algV[x])!= "Tdsm":

                                        algV[x]='Tdsm'

                                     if ''.join(algT[y]) in ["gum", "gun", "gu"] and ''.join(algV[x+1]) in [Verbcases, Wcases]:
                                        algV[x]='Qa'
                                  
                                     if ''.join(b) =='Dp3sf' and ''.join(algT[y+1][:2]) in ['ph','bh','ch','th','dh','mh','sh','fh']:
                                        algV[x]='Dp3sm'
                                   
                                     if ''.join(b)=='Dp3sm' and ''.join(algT[y+1][:2]) in ['pa','pe', 'pi', 'po', 'pu', 'pl', 'pm', 'pn','ba','be', 'bi', 'bo', 'bu', 'bl', 'bm', 'bn', 'ca','ce', 'ci', 'co', 'cu', 'cl', 'cm', 'cn','ga','ge', 'gi', 'go', 'gu', 'gl', 'gm', 'gn','ta','te', 'ti', 'to', 'tu', 'tl', 'tm', 'tn','da','de', 'di', 'do', 'du', 'dl', 'dm', 'dn','ma','me', 'mi', 'mo', 'mu', 'ml', 'mm', 'mn','sa','se', 'si', 'so', 'su', 'sl', 'sm', 'sn','fa','fe', 'fi', 'fo', 'fu', 'fl', 'fm', 'fn']:
                                        algV[x]='Dp3sf'
                                 
                                  
                                     if ''.join(b)=='Dp3sm' and ''.join(algT[y+1][:1])=='h-':
                                        algV[x]='Dp3sf'
                                  
                                     if ''.join(b) =='Spp3sf' and ''.join(algT[y+1][:2]) in ['ph','bh','ch','th','dh','mh','sh','fh']:
                                        algV[x]='Spp3sm'
                                 
                                     if ''.join(b)=='Spp3sm' and ''.join(algT[y+1][:2]) in ['pa','pe', 'pi', 'po', 'pu', 'pl', 'pm', 'pn','ba','be', 'bi', 'bo', 'bu', 'bl', 'bm', 'bn', 'ca','ce', 'ci', 'co', 'cu', 'cl', 'cm', 'cn','ga','ge', 'gi', 'go', 'gu', 'gl', 'gm', 'gn','ta','te', 'ti', 'to', 'tu', 'tl', 'tm', 'tn','da','de', 'di', 'do', 'du', 'dl', 'dm', 'dn','ma','me', 'mi', 'mo', 'mu', 'ml', 'mm', 'mn','sa','se', 'si', 'so', 'su', 'sl', 'sm', 'sn','fa','fe', 'fi', 'fo', 'fu', 'fl', 'fm', 'fn']:
                                        algV[x]='Spp3sf'
                                

                                     if ''.join(b)=='Spp3sm' and ''.join(algT[y+1][:1])=='h-':
                                        algV[x]='Spp3sf'


                                     if ''.join(b)!='Mn' and ''.join(algT[y][:1])in ['0','1','2','3','4','5','6','7','8','9'] and ''.join(algT[y][len(algT[y])-1:])in ['0','1','2','3','4','5','6','7','8','9']: 
                                        algV[x]='Mn'

                                     if ''.join(b)!='Mn' and ''.join(algT[y][:1])in ['0','1','2','3','4','5','6','7','8','9'] and ''.join(algT[y][len(algT[y])-2:])in ['an']: 
                                        algV[x]='Mn'

                                     if ''.join(b)!='Mo' and ''.join(algT[y][:1])in ['0','1','2','3','4','5','6','7','8','9'] and ''.join(algT[y][len(algT[y])-2:])in ['mh']: 
                                        algV[x]='Mo'

                                     if ''.join(b)!='Fb' and ''.join(algT[y])=='—':
                                        algV[x]='Fb'
                                    
                                   

                      myGui.taggerFile = list(zip(algT,algV))
                      myGui.tracker.set('Status: default tagging complete..')
                      myGui.text.insert(INSERT, myGui.taggerFile)
                      savefile(myGui.taggerFile)
                      myGui.tracker.set('Status: ready')   
            
        else:
             messagebox.showerror(title="Error", message="No input file supplied..please supply an input file")

        return 


def tagfile_Simplified():
        tk = GaelicTokeniser()
        algT=[]
        algV=[]
        myGui.tokenisedFile =''
        if myGui.inputFile :
            refresh()
            myGui.tracker.set('Status: please wait..simplified tagging in progress')
            myGui.myprogressbar.update_idletasks() ## to hold status infor on screen till end of process
            simmodel = LoadSimplifiedModel()
            BrillTag  = simmodel.tag(tk.tokenise(myGui.inputFile))
            
            for (c, d) in BrillTag: # algorithm output
                                algT.append(c)
                                algV.append(d)


            for y, c in enumerate(algT):
                            for x, b in enumerate(algV):
                                if x==y:
                                     for d in myGui.englishLexicon :
                                            if str(''.join(d)).lower() == c and c not in ['air','shine', 'gun','sin', 'far', 'fear', 'a', 'can'] and b!='Xfe':
                                                    algV[x]='Xfe'
                                     if ''.join(b)!='Mn' and ''.join(algT[y][:1])in ['0','1','2','3','4','5','6','7','8','9'] and ''.join(algT[y][len(algT[y])-1:])in ['0','1','2','3','4','5','6','7','8','9']: 
                                        algV[x]='Mn'

                                     if ''.join(b)!='Mn' and ''.join(algT[y][:1])in ['0','1','2','3','4','5','6','7','8','9'] and ''.join(algT[y][len(algT[y])-2:])in ['an']: 
                                        algV[x]='Mn'

                                     if ''.join(b)!='Mo' and ''.join(algT[y][:1])in ['0','1','2','3','4','5','6','7','8','9'] and ''.join(algT[y][len(algT[y])-2:])in ['mh']: 
                                        algV[x]='Mo'

                                     if ''.join(b)!='Fb' and ''.join(algT[y])=='—':
                                        algV[x]='Fb'

            myGui.taggerFile = list(zip(algT,algV))
            myGui.tracker.set('Status: simplified tagging complete..')
            myGui.text.insert(INSERT, myGui.taggerFile)
            savefile(myGui.taggerFile)
            myGui.tracker.set('Status: ready')   
            
        else:
             messagebox.showerror(title="Error", message="No input file supplied..please supply an input file")

        return 
        
def refresh():
    myGui.text.delete(1.0, END)
    myGui.tracker.set('Status: ready')   

  
def savefile(myfile):
        msavefile = myfile
        tagger1 = Tagger()
        msave = messagebox.askyesno(title="Processing complete", message="Do you want to save output file")
        if msave>0:
             msavetype = messagebox.askyesnocancel(title="Confirm File Save", message="Yes to save file with default-txt?, NO to save as csv or Cancel")
             if msavetype==1 and len(myGui.tokenisedFile)>1:
                         myGui.taggerFile =''
                         print('Yes is chosen - txt')
                         #myGui.directory = filedialog.askdirectory()+ '/' + "TokenisedOutput" + myGui.time2
                         myGui.filename = filedialog.asksaveasfilename()
                         print (myGui.directory)
                         #tagger1.writeouputfile(msavefile, myGui.directory, 'txt', 'tk')
                         tagger1.writeouputfile(msavefile, myGui.filename, 'txt', 'tk')
                         messageinfo ='File is saved..please check your output: ' + myGui.filename
                         messagebox.showinfo(title="File Saved", message=messageinfo)
                         return
                        
             if msavetype==0 and  len(myGui.tokenisedFile)>1:
                     myGui.taggerFile =''
                     #print('No is chosen - csv')
                     #myGui.directory = filedialog.askdirectory()+ '/' + "TokenisedOutput" + myGui.time2
                     myGui.filename = filedialog.asksaveasfilename()
                     tagger1.writeouputfile(msavefile, myGui.filename, 'csv', 'tk')
                     messageinfo ='File is saved..please check your output: ' + myGui.filename
                     messagebox.showinfo(title="File Saved", message=messageinfo)
                     return
                    
             if msavetype==1 and myGui.taggerFile and len(myGui.tokenisedFile)<1 :
                     
                    # print('Yes is chosen - txt')
                    # myGui.directory1 = filedialog.askdirectory()+ '/' + "TaggerOutput" + myGui.time2
                     myGui.filename1 = filedialog.asksaveasfilename()
                     tagger1.writeouputfile(msavefile, myGui.filename1, 'txt', 'tg')
                     messageinfo ='File is saved..please check your output: ' + myGui.filename1
                     messagebox.showinfo(title="File Saved", message=messageinfo)
                     return


                    
             if msavetype==0 and myGui.taggerFile and len(myGui.tokenisedFile)<1:
                   
                    # print('No is chosen - csv')
                    # myGui.directory1 = filedialog.askdirectory()+ '/' + "TaggerOutput" + myGui.time2
                     myGui.filename1 = filedialog.asksaveasfilename()
                     #print (myGui.directory1)
                     #print (list(myGui.taggerFile))
                     tagger1.writeouputfile(msavefile, myGui.filename1, 'csv', 'tg')
                     messageinfo ='File is saved..please check your output: ' + myGui.filename1
                     messagebox.showinfo(title="File Saved", message=messageinfo)
                     return
             else:
                 if msavetype==None:
                      print('Cancel is chosen')
                      return
        else:
            return
                        

def buildGUI():
       
        myGui.geometry("%dx%d+0+0" % (w, h))
        myGui.title('Scottish Gaelic Part-of-Speech Tagger Beta Version 1.0')
        lblheader1 = Label(myGui, font=("serif",14), justify= CENTER, foreground="black",  text='Scottish Gaelic Tokeniser and Part-of-Speech Tagger - BETA vervsion 1.0 ').pack()
       # lblheader2 = Label(myGui, font=("serif",14), justify= CENTER, foreground="blue", text='Please feel free to use and do not hesitate to report any issues you may have to Dr Will Lamb. Email: w.lamb@ed.ac.uk').pack()
        myGui.myprogressbar = Label(myGui, textvariable = myGui.tracker, borderwidth=1, relief=SUNKEN, anchor=W)
             
        myGui.myprogressbar.pack(expand=True, fill=X, side=TOP)
        myGui.text.pack()
        myGui.tracker.set('Status: ready')
       
  

        menubar = Menu(myGui)
        filemenu = Menu(menubar,tearoff=0)
        filemenu.add_command(label='New', command = refresh)
        filemenu.add_command(label='Open', command= mopenfiles)
        filemenu.add_command(label='Close', command=mquit)
        menubar.add_cascade(label='File', menu=filemenu)
                  
        runmenu = Menu(menubar,tearoff=0)
        runmenu.add_command(label='Tokeniser', command=tokenisefile)
        runmenu.add_command(label='Default Tagger', command = tagfile_Default)
        runmenu.add_command(label='Simplified Tagger', command = tagfile_Simplified)
        menubar.add_cascade(label='Run', menu=runmenu)

        helpmenu = Menu(menubar,tearoff=0)
        helpmenu.add_command(label='Read me file', command=helpfile)
        helpmenu.add_command(label='About', command=about)
        menubar.add_cascade(label='Help', menu=helpmenu)

        
        myGui.config(menu=menubar)

       
      
        myGui.mainloop()
       
       
       

class GaelicPartOfSpeechTagger:
                                        
            def  __init__(self, inputfile, outputfile):
                self.inputfile = inputfile
                self.outputfile=outputfile
                
            def readinputfile(self, inputfile):
                        self.inputfile = inputfile
                       # self.item = ''
                        self.item = self.inputfile.read()
                       # print ('this is the inputfile', self.inputfile)
                        
                        return self.item
                    
            def writeouputfile(self, inputfile, output, outputformat, process):
                 self.inputfile= inputfile # for API
                 self.output= output
                 self.outputformat = outputformat
                 self.process = process
                
               

                 #print(list(self.inputfile))
                

                 if self.outputformat =='csv' and self.process=='tg':
                        self.output2  = codecs.open(self.output+'.csv' ,'w')
                        print ('this is the output', self.outputformat)
                        wr = csv.writer(self.output2,  delimiter=',',  lineterminator='\n')
                        for  (v, y) in self.inputfile:
                                  wr.writerow((v, y))
                        return
                      
                                         
                 if self.outputformat == 'txt'and self.process=='tg':
                      self.output1  = codecs.open(self.output+'.txt' ,'w')
                      print ('this is the output', self.outputformat)
                      for  (v, y) in self.inputfile:
                           self.output1.write(''.join(v) + '/' + ''.join(y)+ ' ')
                      self.output1.close()
                      return


                 if self.outputformat =='csv' and self.process=='tk':
                        self.output2  = codecs.open(self.output+'.csv' ,'w')
                        print ('this is the output', self.outputformat)
                        wr = csv.writer(self.output2,  delimiter=',',  lineterminator='\n')
                        for   v in self.inputfile:
                                wr.writerow([v])
                        return

                                               
                 if self.outputformat == 'txt'and self.process=='tk':
                      self.output1  = codecs.open(self.output+'.txt' ,'w')
                      print ('this is the output', self.outputformat)
                      for  v in self.inputfile:
                           self.output1.write(''.join(v)+'\n')
                      self.output1.close()
                      return
                 

                
      
            def __str__(self):
                return self.inputfile


class GaelicSentenceSplitter(GaelicPartOfSpeechTagger):
                    def  __init__(self):
                        GaelicPartOfSpeechTagger. __init__(self, 'inputfile', 'outputfile')

                    def splitsentence(self, text):
                        self.text = text
                        self.sentences = re.split(r'\\.', self.text)

                        return self.sentences
                      

class GaelicTokeniser(GaelicPartOfSpeechTagger):
                def  __init__(self):
                    GaelicPartOfSpeechTagger. __init__(self, 'inputfile', 'outputfile')
                    
                def  tokenise(self, text):
                      self.text=text
                      self.Pnamedict = {}
                      self.PnameValues = []
                      self.tokensetF = []
                      self.tokensetF1 = []
                      self.tokensetF2 = []
                      self.tokensetF3 = []
                      self.tokensetF4 = []
                      self.tokensetF5 = []
                      self.Junk =[]
                      self.abbr = re.findall(r"\w+\S+",  str(codecs.open(os.path.join(os.getcwd(), 'data', 'Abbrv070214.csv') ,'r')))
                      #self.abbr = re.findall(r"\w+\S+",  str(codecs.open(r'C:\ScottishGaelicProject\TestSystem\data\Abbrv070214.csv' ,'r')))
                      self.exceptions = ["'ac", '`ac', "'gam",  "`gam", "'gad",  "`gad", "'ga",  "`ga", "'gar",  "`gar", "'gur",  "`gur", "'gan",  "`gan", "'m",  "`m", "'n",  "`n", "'nam",  "`nam", "'nad",  "`nad", "'na",  "`na", "'nar",  "`nar", "‘nar", "'nur",  "`nur", "'nan",  "`nan", "'san", "'San", "‘San", "`san", "‘sa",  "`sa", "‘S", "'S", "`S", "‘ac", "‘ga", "`ga", "‘gan","`gan" ]

                        
                      self.alltokens = re.findall(r"\w+[“'-’]+\w+|\w+[-.!?,'"":’`/“”]+\s+|[-'’`“]+\w+|[(]\W+|[(]+[0-9]+[)]|[(]+\S+[)]|\S+[)]|\w+[)]+[,.]+\s+|\w\+[-]+\w+[)]+[.]+\s|\S+[)]+[;.]+\s+|\s+[',.!?:’`/=]+\s+|(?<!=[‘',.!?:’/`])+\w+|\S[^]+\S+|\w+[',.!?:""’/`‘]+|(?<=['"":’`‘])+\S+|[£$]+[0-9]+|\w+[""''’”/]+|[aA-zZ]*[.:,’`”)]+[,;.]+\s+|[aA-zZ]*[.:,’`”]+|[aA-zZ]*[?]+[”]+\s|[‘]+\w+[’]+[,]|[‘]+\w+[’]+\s+|\w+[@]+\w+[.]+\w+|\w+[?]+[:]+[//]+[^\s<>']+|\W\w+\s|[^\W\s]+", self.text) ## in the process of modifying for different text type - formal
                      for n in self.alltokens:
                                 self.tokensetF.append(n.strip())
                      for nx in self.tokensetF:
                          if nx == self.abbr :
                                      self.tokensetF1.append(nx)

                          if nx in self.exceptions:
                                        self.tokensetF1.append(nx)
       
                          else:
                             
                            hyphenT = re.findall(r"(\bt-)", str(nx)) ## takes all  t-hyphenated
                            hyphenT1 = re.findall('(?<=t-)\w+', str(nx))
                            hyphenN = re.findall(r"(\bn-)", str(nx)) ## takes all  n-hyphenated
                            hyphenN1 = re.findall('(?<=n-)\w+', str(nx))
                            hyphenH = re.findall(r"(\bh-)", str(nx)) ## takes all  h-hyphenated
                            hyphenH1 = re.findall('(?<=h-)\w+', str(nx))
                            hyphenSa = re.findall(r"(\b-sa\b)", str(nx)) ## takes all  -sa hyhpenated 
                            XhyphenSa = re.findall('(?<!=-sa)\w+', str(nx)) ## takes all   word befor hyhpenated -sa
                            hyphenSe = re.findall(r"(\b-se\b)", str(nx)) ## takes all  -se hyhpenated 
                            XhyphenSe = re.findall('(?<!=-se)\w+', str(nx)) ## takes all   word befor hyhpenated -se
                            hyphenSan = re.findall(r"(\b-san\b)", str(nx)) ## takes all  -san hyhpenated 
                            XhyphenSan = re.findall(r'(?<!=-san)\w+', str(nx)) ## takes all   word befor hyhpenated -san
                            doublQpnt = re.findall(r'(\A[" / \ ( [ ])\w+', str(nx)) ## determines whether there is an initial quotes from a string 
                            doublQSub = re.findall(r'(?<!=["])\S', str(nx)) ## find the strings that starts with quotes and end with non-white space
                            qMark = re.findall(r"(?<=(\b[?.!,:' " "]))", str(nx)) ## determines whether there is a puntuation mark at end of string
                            BeforeqMark = re.findall(r"(?<!=[?.!,:'])\w+", str(nx)) ## find the strings that ends with puntuation mark and non-white space
                            singleQpnt = re.findall(r"(\A[']+)", str(nx)) ## determines whether there is an initial single quotes from a string 
                            singleQSub = re.findall(r"(?<!=['])\S", str(nx)) ## find the strings that starts with single quotes and end with non-white space
                            #comprativeParticles = re.findall(r"(?<!=['])\S", str(nx))
                            currency = re.findall(r"(\A[$£]+)", str(nx)) ## determines whether there is an initial currency sign from a string 
                            currencySub = re.findall(r"(?<!=[$£])\S", str(nx)) ##
                            comprativeParticles = re.findall(r"(\w+['])", str(nx)) ## approstohe 
               
                            comprativeParticles1 = re.findall(r"(?<!=[']\w)\w+", str(nx))

                            doubleAfter = re.findall(r'(\w+["]+)', str(nx)) ## determines whether there is an initial quotes from a string


                            beforestroke = re.findall(r"(\b/\b)", str(nx)) ## takes all  -strock words
                            afterstroke = re.findall('(?<!=/)\w+', str(nx)) ## takes all   word -strock words


               
                            beforeEqual = re.findall(r"(\A[=]+)", str(nx)) ## takes all  -strock words
                            afterEqual = re.findall("(?<!=\A[='])\S", str(nx)) ## takes all   word -strock words


                            beforeAccent = re.findall(r"(\b’\b)", str(nx)) ## takes all  -accen words
                            afterAccent = re.findall('(?<!= ’ )\S', str(nx)) ## takes all   -accented words


                            beginAccent = re.findall(r"(\A[‘]+)", str(nx)) ## takes all  -accented words
                            beginAccentT = re.findall('(?<!= ‘ )\S', str(nx)) ## takes all   -accented words

                            beforePeriod = re.findall(r"(\B[.]\B)", str(nx)) ## takes all  - words with periods at end
                            afterPeriod = re.findall('(?<!= [.] )\S', str(nx)) ## takes all   - peroid

                            beforeComer = re.findall(r"(\B[,]\B)", str(nx)) ## takes all  - words with comer at end
                            afterComer  = re.findall('(?<!= [,] )\S', str(nx)) ## takes all   - comer

                            beforeQmark = re.findall(r"(\B[?]+\B)", str(nx)) ## takes all  - words with question marks at end
                            afterQmark  = re.findall('(?<!= [?] )\S', str(nx)) ## takes all   - comer


                            beforePeriod1 = re.findall(r"(\b[.])", str(nx)) ## takes all  - words with periods at end
                            afterPeriod1 = re.findall('(?<!= [.] )\S', str(nx)) ## takes all   - peroid

                            beforeComer1 = re.findall(r"(\b[,])", str(nx)) ## takes all  - words with comer at end
                            afterComer1  = re.findall('(?<!= [,] )\S', str(nx)) ## takes all   - comer


                            beginAccent2 = re.findall(r"(\b[’]+)", str(nx)) ## takes all  -accented words
                            beginAccentT2 = re.findall('(?<!= ’ )\S', str(nx)) ## takes all   -accented words


                            beforeOpenBra = re.findall(r"(\A[(]+[(‘])", str(nx)) ## takes all  - words with comer at end
                            afterOpenBra  = re.findall("(?<!= [(])\S", str(nx)) ## takes all   - comer

                            beforeDuoubleQ = re.findall(r"(\A[“])", str(nx)) ## takes all  - words with double quote at end
                            afterDuoubleQ  = re.findall("(?<!= [“])\S", str(nx)) ## takes all   - comer

                            qColon = re.findall(r"(?<=(\b[:]))", str(nx)) ## determines whether there is a puntuation mark at end of string

                            if qColon:
                                 x = re.findall(r"\S", str(nx))
                                 self.tokensetF1.append(''.join(x[:len(x)-1]))
                                 xx = x[len(x)-1:]
                                 self.tokensetF1.append(''.join(xx))
                                 nx = ''


                            if beforeDuoubleQ  :
                                self.tokensetF1.append(''.join(beforeDuoubleQ))
                                self.tokensetF1.append(''.join(afterDuoubleQ[1:]))
                                nx = ''
                
                            if beforeOpenBra :
                                self.tokensetF1.append(''.join(afterOpenBra[:1]))
                                self.tokensetF1.append(''.join(afterOpenBra[1:2]))
                                self.tokensetF1.append(''.join(afterOpenBra[2:]))
                                nx = ''
                   

                            if beginAccent2:
                                if ''.join(beginAccentT2[:2])=='a’':
                                       self.tokensetF1.append(''.join(beginAccentT2[:2]))
                                       self.tokensetF1.append(''.join(beginAccentT2[2:]))
                                       nx = ""
                     

                            if beforeComer1:
                      
                                 if ''.join(beforeComer1) == ''.join(afterComer1[len(afterComer1)-1:]):
                                      self.tokensetF1.append(''.join(afterComer1[:len(afterComer1)-1]))
                                      self.tokensetF1.append(''.join(beforeComer1))
                                      nx=''
                     
                

                            if beforePeriod1:
                                 if ''.join(beforePeriod1) == ''.join(afterPeriod1[len(afterPeriod1)-1:]):
                                      self.tokensetF1.append(''.join(afterPeriod1[:len(afterPeriod1)-1]))
                                      self.tokensetF1.append(''.join(beforePeriod1))
                                      nx=''
                                    


                            if beforeQmark and nx not in ["[?]", "[1]", "[2]", "[3]", "[4]", "[5]", "[6]", "[7]", "[8]", "[9]"]:
                                if ''.join(beforeQmark) == ''.join(afterQmark[:1]):
                                    ''
                                else:
                                    x = afterQmark[len(afterQmark)-1:]
                                    self.tokensetF1.append(''.join(afterQmark[:len(afterQmark)-1]))
                                    self.tokensetF1.append(''.join(beforeQmark))
                                    nx=''
                            

                
                            if beforeComer :

                                  x =  afterComer[len(afterComer)-2:] ## filtering for (eg: ],) type of tokens normally used in accademic text
                                  y  = afterComer[:1]## filtering for (eg: [ ,) type of tokens normally used in accademic text
                                  if ''.join(x[:len(x)-1]) in [']', ')'] and ''.join(y) in ['[', '('] :
                                       self.tokensetF1.append(''.join(y))
                                       self.tokensetF1.append(''.join(afterComer[1:len(afterComer)-2]))
                                       self.tokensetF1.append(''.join(x[:len(x)-1]))
                                       self.tokensetF1.append(''.join(beforeComer))
                                       nx=''
                                       
                                  if ''.join(x[:len(x)-1]) in [']', ')'] and ''.join(y) not in ['[', '(']:
                                       self.tokensetF1.append(''.join(afterComer[:len(afterComer)-2]))
                                       self.tokensetF1.append(''.join(x[:len(x)-1]))
                                       self.tokensetF1.append(''.join(beforeComer))
                                       nx=''

                                  if  ''.join(x[:len(x)-1]) not in [']', ')'] and ''.join(y) not in  ['[', '(']:
                                      xx =x[:len(x)-1]
                                      if xx:
                                            if ''.join(afterComer[:1])== '‘':
                                                    xxx = afterComer[len(afterComer)-2:]
                                                    xxxx = afterComer[:]
                                                    self.tokensetF1.append(''.join(afterComer[:1]))
                                                    self.tokensetF1.append(''.join(afterComer[1: len(afterComer)-2]))
                                                    self.tokensetF1.append(''.join( xxx[:1]))
                                                    self.tokensetF1.append(''.join( afterComer[len(afterComer)-1:]))
                                                    nx=''
                                            else:

                                                 if len(afterComer)==3 :
                                                    self.tokensetF1.append(''.join(afterComer[1:2]))
                                                    self.tokensetF1.append(''.join(afterComer[len(afterComer)-1:]))
                                                    nx=''

                                                 else:
                                                        if len(afterComer)==2:
                                                                 self.tokensetF1.append(''.join(afterComer[:1]))
                                                                 self.tokensetF1.append(''.join(afterComer[len(afterComer)-1:]))
                                                                 nx=''

                            if beginAccent and ''.join(beginAccentT[len(beginAccentT)-1:])=='’'  and not xx:
                                  x= beginAccentT[1:]
                                  self.tokensetF1.append(''.join(beginAccent))
                                  self.tokensetF1.append(''.join(x[:len(x)-1]))
                                  self.tokensetF1.append(''.join(beginAccentT[len(beginAccentT)-1:]))
                                  self.Junk.append(''.join(beginAccentT[1:]))
                                  nx=''


                            if beginAccent and ''.join(beginAccentT[len(beginAccentT)-1:])==',' and not xx:
                                  self.tokensetF1.append(''.join(beginAccent))
                                  self.tokensetF1.append(''.join(beginAccentT[1:len(beginAccentT)-1]))
                                  self.tokensetF1.append(''.join(beginAccentT[len(beginAccentT)-1:]))
                                  self.Junk.append(''.join(beginAccent + beginAccentT[1:len(beginAccentT)-1]))
                                  nx=''

                            if beginAccent and ''.join(beginAccentT[len(beginAccentT)-1:])=='?' and not xx:
                                  x = beginAccentT[len(beginAccentT)-2:]
                                  if  ''.join(x[:len(x)-1])== '’':
                                        self.tokensetF1.append(''.join(beginAccent)) 
                                        self.tokensetF1.append(''.join(beginAccentT[1:len(beginAccentT)-2]))
                                        self.tokensetF1.append(''.join(x[:len(x)-1]))
                                        self.tokensetF1.append(''.join(beginAccentT[len(beginAccentT)-1:]))
                                        self.Junk.append(''.join(beginAccent) + beginAccentT[1:len(beginAccentT)-1])
                                        self.Junk.append(''.join(beginAccentT[1:len(beginAccentT)-1] + beginAccentT[len(beginAccentT)-1:])) 
                                        nx=""

                            if beginAccent and not beforeComer1 and not xx:
                                       nx=''
                            
                            if beforeAccent and ''.join(afterAccent[len(afterAccent)-1:]) not in ['s'] :
                                x = afterAccent[:3]
                                if  ''.join(x[1:2])== "’":
                                  self.tokensetF1.append(''.join(afterAccent[:2]))
                                  self.tokensetF1.append(''.join(afterAccent[2:]))
                                  nx=''
                                if ''.join(x[2:3])== "’":
                                  self.tokensetF1.append(''.join(afterAccent[:3]))
                                  self.tokensetF1.append(''.join(afterAccent[3:]))
                                  nx=''

                              
                            if beforeEqual:
                                self.tokensetF1.append(''.join(beforeEqual))
                                self.tokensetF1.append(''.join(afterEqual[1:2]))
                                nx=''
                                
                                

                            if beforestroke:
                                 self.tokensetF1.append(''.join(afterstroke[:1]))
                                 self.tokensetF1.append(''.join(beforestroke))
                                 self.tokensetF1.append(''.join(afterstroke[1:]))
                                 nx=''
                                 

                            if currency:
                                    x = len(currencySub)
                                    self.tokensetF1.append(''.join(currency[:1]))
                                    self.tokensetF1.append(''.join(currencySub[1: x]))
                                    #self.tokensetF1.append(''.join(currencySub[x-1:]))
                                    nx=''
                                 

                            if doublQpnt and nx not in ["[?]","[Name]","[Placename]", "[1]", "[2]", "[3]", "[4]", "[5]", "[6]", "[7]", "[8]", "[9]"]:
                                    x = doublQSub[1:len(doublQSub)-1]
                                    y = ''.join(doublQSub[len(doublQSub)-1:])
                                    m = ''.join(doublQpnt)
                                    if  y != '"' or y != '' and y== ')' and  m != '('  :
                                             
                                        xy = (x+ doublQSub[len(doublQSub)-1:])
                                        if ''.join(xy[len(xy)-1:]) not in [')', ':', '?', ']'] :
                                       
                                            self.tokensetF1.append(''.join(m))
                                            self.tokensetF1.append(''.join(xy))
                                          
                                            nx = ' '
                                        
                                        else:
                                            self.tokensetF1.append(m)
                                            self.tokensetF1.append(''.join(xy[:len(xy)-1]))
                                            self.tokensetF1.append(y)
                                            nx = ''

                                    if  y == '"':
                                        self.tokensetF1.append(''.join(doublQpnt))
                                        self.tokensetF1.append(''.join(doublQSub[1:len(doublQSub)-1]))
                                        self.tokensetF1.append(''.join(y))
                                        nx=' '

                            if comprativeParticles and len(comprativeParticles1)>0 :
                                         if   len(''.join(comprativeParticles1[1:]))>1 :
                                                self.tokensetF1.append(''.join(comprativeParticles[:1]))
                                                self.tokensetF1.append(''.join(comprativeParticles1[1:]))
                                                nx = ""
                              
                                         if len(''.join(comprativeParticles1[1:]))==1:
                                                self.tokensetF1.append(''.join(comprativeParticles[:1]+ comprativeParticles1[1:]))
                                                nx=''
    
                              
                            if  hyphenT:
                                 
                                     self.tokensetF1.append(''.join(hyphenT))
                                     self.tokensetF1.append(''.join(hyphenT1))
                                     nx=''
                                                      
                                               
                            if  hyphenN:
                                    self.tokensetF1.append(''.join(hyphenN)) ## then appen the tripped token into the list container 
                                    self.tokensetF1.append(''.join(hyphenN1))## then appen the tripped token into the list container
                                    nx=''
                          
                            if  hyphenH and nx not in ["h-uile", "h-ana-miannaibh"]:
                                    self.tokensetF1.append(''.join(hyphenH)) ## then appen the tripped token into the list container
                                    self.tokensetF1.append(''.join(hyphenH1))## then appen the tripped token into the list container
                                    nx=''
                                            
                            if  hyphenSe:
                                   self.tokensetF1.append(''.join(hyphenSa[:1]))
                                   self.tokensetF1.append(''.join(XhyphenSe[:1]))
                                   nx=''

                            if  hyphenSan:
                                      self.tokensetF1.append(''.join(XhyphenSan[:1]))
                                      self.tokensetF1.append(''.join(XhyphenSan[:1]))
                                      nx=''
                       
                            else:
                                    self.tokensetF1.append(nx)


                      for   i, DA in enumerate(self.tokensetF1):
##                         
##                                if DA == '1':
##                                        self.tokensetF2.append('[1]')
##                                        DA=''
##
##                                if DA == '2':
##                                        self.tokensetF2.append('[2]')
##                                        DA=''
##
##                                if DA == '3':
##                                        self.tokensetF2.append('[3]')
##                                        DA=''
##
##                                if DA == '4':
##                                        self.tokensetF2.append('[4]')
##                                        DA=''
##
##                                if DA == '5':
##                                        self.tokensetF2.append('[5]')
##                                        DA=''
##
##                                if DA == '6':
##                                        self.tokensetF2.append('[6]')
##                                        DA=''
##                                if DA == '7':
##                                        self.tokensetF2.append('[7]')
##                                        DA=''
##
##                                if DA == '8':
##                                        self.tokensetF2.append('[8]')
##                                        DA=''
##
##                                if DA == '9':
##                                        self.tokensetF2.append('[9]')
##                                        DA=''

                                if DA == ']':
                                          self.tokensetF2.append('')
                                          DA=''

                                if DA == 'Placename':
                                        self.tokensetF2.append('[Placename]')
                                        DA=''
                                              
                                
                                              
                                if DA =='a-réir':
                                      self.tokensetF2.append('a')
                                      self.tokensetF2.append('-')
                                      self.tokensetF2.append('réir')
                                      DA=''

                   
                                if DA =="mi '":
                                        self.tokensetF2.append('mi')
                                        self.tokensetF2.extend("'")
                                        DA=''

                                if DA =="!)":
                                        self.tokensetF2.append('!')
                                        self.tokensetF2.extend(")")
                                        DA=''

                                if DA =="le'r":
                                        self.tokensetF2.append('le')
                                        self.tokensetF2.extend("'r")
                                        DA=''

                                                                
                                if DA== "mi.”"  :
                                        self.tokensetF2.append("mi")
                                        self.tokensetF2.extend(".")
                                        self.tokensetF2.extend("”")
                                        #self.tokensetF1.remove("mi.”")
                                        DA = ''

                                if DA== "mi,”"  :
                                        self.tokensetF2.append("mi")
                                        self.tokensetF2.extend(",")
                                        self.tokensetF2.extend("”")
                                        DA = ''

                                if DA =="].":
                                        self.tokensetF2.append(']')
                                        self.tokensetF2.extend(".")
                                        DA=''
                                        
                                if DA =="?)":
                                        self.tokensetF2.append('?')
                                        self.tokensetF2.extend(")")
                                        DA=''


                                if DA ==".)":
                                        self.tokensetF2.append('.')
                                        self.tokensetF2.extend(")")
                                        DA=''

                                if DA =="”)":
                                        self.tokensetF2.append('”')
                                        self.tokensetF2.extend(")")
                                        DA=''

                                if DA =='); ':
                                        self.tokensetF2.append(')')
                                        self.tokensetF2.extend(";")
                                        DA=''

                                if DA ==") ":
                                        self.tokensetF2.append(')')
                                        DA=''

                                if DA =="?”":
                                        self.tokensetF2.append('?')
                                        self.tokensetF2.extend("”")
                                        DA='' 
                                        
                                if DA =="i.”":
                                        self.tokensetF2.append('i')
                                        self.tokensetF2.extend(".")
                                        self.tokensetF2.extend("”")
                                        DA=''  
                                        
                                if DA ==".’”":
                                        self.tokensetF2.append('.')
                                        self.tokensetF2.extend("”")
                                        DA=''

                                if DA ==",”":
                                        self.tokensetF2.append(',')
                                        self.tokensetF2.extend("”")
                                        DA='' 

                                if DA =="tu,”":
                                        self.tokensetF2.append('tu')
                                        self.tokensetF2.extend(",")
                                        self.tokensetF2.extend("”")
                                        DA='' 
                                
                                        
                                if DA =="”.":
                                        self.tokensetF2.append('”')
                                        self.tokensetF2.extend(".")
                                        DA=''
                                        
                                if DA =="às.”":
                                        self.tokensetF2.append('às')
                                        self.tokensetF2.extend(".")
                                        self.tokensetF2.extend("”")
                                        DA=''
                                        
                                if DA =="sa,”":
                                        self.tokensetF2.append('sa')
                                        self.tokensetF2.extend(",")
                                        self.tokensetF2.extend("”")
                                        DA='' 
                                        
                                if DA =="’, ":
                                        self.tokensetF2.append('’')
                                        self.tokensetF2.extend(",")
                                        DA='' 
                                        
                                if DA ==").":
                                        self.tokensetF2.append(')')
                                        self.tokensetF2.extend(".")
                                        DA=''
                                        
                                if DA =="),":
                                        self.tokensetF2.append(')')
                                        self.tokensetF2.extend(",")
                                        DA=''
                                        
                                if DA =="), ":
                                        self.tokensetF2.append(')')
                                        self.tokensetF2.extend(",")
                                        DA=''

                                if DA ==".”":
                                        self.tokensetF2.append('.')
                                        self.tokensetF2.extend("”")
                                        DA=''

                                if DA =="’.”":
                                        self.tokensetF2.append('’')
                                        self.tokensetF2.extend(".")
                                        self.tokensetF2.extend("”")
                                        DA='' 

                                if DA ==",”":
                                        self.tokensetF2.append(',')
                                        self.tokensetF2.extend("”")
                                        DA=''
                                        
                                if DA =="’,":
                                        self.tokensetF2.append('’')
                                        self.tokensetF2.extend(",")
                                        DA=""
                                
                                if DA =="’ ":
                                        self.tokensetF2.append('’')
                                        DA='' 

                                if DA ==");":
                                        self.tokensetF2.append(')')
                                        self.tokensetF2.extend(";")
                                        DA=''
                                        
                                if DA =="s’.”":
                                        self.tokensetF2.append('s’')
                                        self.tokensetF2.extend(".")
                                        self.tokensetF2.extend("”")
                                        DA=''

                                        
                                       
                                if DA =="tus":
                                        self.tokensetF2.append("tus'")
                                        DA=''

                                if DA =="aic":
                                        self.tokensetF2.append("aic'")
                                        DA=''
                        

                                if DA =='mi-fhìn':
                                        self.tokensetF2.append('mi')
                                        self.tokensetF2.append('-')
                                        self.tokensetF2.append('fhìn')
                                        DA=''

                                if DA =='dh’èireas':
                                        self.tokensetF2.append('dh’')
                                        self.tokensetF2.append('èireas')
                                        DA=''
                                        
                                if DA =='mi-fhèin':
                                        self.tokensetF2.append('mi')
                                        self.tokensetF2.append('-')
                                        self.tokensetF2.append('fhèin')
                                        DA=''

                                if DA =='thu-fhèin':
                                        self.tokensetF2.append('thu')
                                        self.tokensetF2.append('-')
                                        self.tokensetF2.append('fhèin')
                                        DA=''
                                        
                                if DA =='e-fhèin':
                                        self.tokensetF2.append('e')
                                        self.tokensetF2.append('-')
                                        self.tokensetF2.append('fhèin')
                                        DA=''

                                if DA =='i-fhèin':
                                        self.tokensetF2.append('i')
                                        self.tokensetF2.append('-')
                                        self.tokensetF2.append('fhèin')
                                        DA=''
                        
                  
                                if DA =='sinn-fhìn':
                                        self.tokensetF2.append('sinn')
                                        self.tokensetF2.append('-')
                                        self.tokensetF2.append('fhìn')
                                        DA=''
                                        
                                if DA =='sibh-fhèin':
                                        self.tokensetF2.append('sibh')
                                        self.tokensetF2.append('-')
                                        self.tokensetF2.append('fhèin')
                                        DA=''
                                 
                                        
                                if DA =='iad-fhèin':
                                        self.tokensetF2.append('iad')
                                        self.tokensetF2.append('-')
                                        self.tokensetF2.append('fhèin')
                                        DA=''

                ##
                                if DA =='h-ana-miannaibh':
                                        self.tokensetF2.append('h-')
                                        self.tokensetF2.append('ana-miannaibh')
                                        DA=''

                                        
                                if DA =="a b'":
                                        self.tokensetF2.append('a')
                                        self.tokensetF2.append("b'")
                                        DA=''
                                
                                        
                                if DA =='dh’obair-riaghaltais':
                                        self.tokensetF2.append('dh’')
                                        self.tokensetF2.append('obair-riaghaltais')
                                        DA=''

                                if DA =="dh’fheumas":
                                        self.tokensetF2.append("dh'")
                                        self.tokensetF2.append('fheumas')
                                        DA=''
                                        
                                if DA =="dh'fheumas":
                                        self.tokensetF2.append("dh'")
                                        self.tokensetF2.append('fheumas')
                                        DA=''

                                if DA =="dh'fhaodas":
                                        self.tokensetF2.append("dh'")
                                        self.tokensetF2.append('fhaodas')
                                        DA=''

                                if DA =="dh’fhaodas":
                                        self.tokensetF2.append("dh'")
                                        self.tokensetF2.append('fhaodas')
                                        DA=''

            
                                if DA =="dh’fhàs":
                                        self.tokensetF2.append("dh’")
                                        self.tokensetF2.append('fhàs')
                                        DA=''
                                           
                                if DA =="dh'fhàs":
                                        self.tokensetF2.append("dh'")
                                        self.tokensetF2.append('fhàs')
                                        DA='' 
                                    
                                if DA =='Ban-righ' and "'nn" in self.tokensetF1[i:i+2]:
                                      #  print (' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("'nn")
                                        DA=''

                                if DA =='Dh' and "’fhaodainn" in self.tokensetF1[i:i+2]:
                                      #  print (' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF2.append('Dh’')
                                        self.tokensetF2.append('fhaodainn')
                                        self.tokensetF1.remove("’fhaodainn")
                                        DA=''


                                if DA =='Ban-righ' and "'nn" in self.tokensetF1[i:i+2]:
                                      #  print (' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("'nn")
                                        DA='' 


                                if DA =='bhrist' and "’" in self.tokensetF1[i:i+2]:
                                      #  print (' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("’")
                                        DA='' 

                                if DA =='oidhch' and "’" in self.tokensetF1[i:i+2]:
                                      #  print (' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("’")
                                        DA=''


                                if DA =='[' and "Placename]." in self.tokensetF1[i:i+2]:
                                      #  print (' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF2.append("[Placename]")
                                        self.tokensetF2.append(".")
                                        self.tokensetF1.remove("Placename].")
                                        DA='' 

                                if DA =='[' and "Placename]" in self.tokensetF1[i:i+2]:
                                      #  print (' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF2.append("[Placename]")
                                        self.tokensetF1.remove("Placename].")
                                        DA='' 


                                if DA =="A" and  "n" in self.tokensetF1[i:i+3]: # it is important to consider the next 3 tokens instead of 2 because there is some blank token created in between
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF1.remove("n")
                                        DA=''

                                if DA =="do’" and  "n" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("n")
                                        DA=''

                                if DA =="oirr" and  "’" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("’")
                                        DA=''

                                if DA =="aig" and  "’" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("’")
                                        DA=''

                                if DA =="chalp" and  "’" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("’")
                                        DA=''

                                if DA =="chual" and  "’" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("’")
                                        DA=''

                                if DA =="chual" and  "'" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("'")
                                        DA='' 

                                if DA =="tein" and  "’" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("’")
                                        DA=''

                                if DA =="creids" and  "’" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("’")
                                        DA=''

                                if DA =="creids" and  "'" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("'")
                                        DA=''

                                if DA =="dhòmhs" and  "’" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("’")
                                        DA=''

                                if DA =="toilicht" and  "’" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("’")
                                        DA=''

                                if DA =="toilicht" and  "'" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("'")
                                        DA=''

                                if DA =="dhòmhs" and  "'" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("'")
                                        DA=''

                                if DA =="innt" and  "'" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("'")
                                        DA=''
                                        
                               
                                if DA =="innt" and  "’" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("’")
                                        DA=''
                                        
                                if DA =="chreach-s" and  "’" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("’")
                                        DA=''

                                if DA =="chreach-s" and  "'" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("'")
                                        DA=''


                                if DA =="Do’" and  "n" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("n")
                                        DA=''

                                if DA =="prionns" and  "'" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("'")
                                        DA=''
                                        
                                if DA =="prionns" and  "’" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("’")
                                        DA=''

                                        
                                if DA =="De’" and  "n" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("n")
                                        DA=''

                                if DA =="comhairl" and  "’" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("’")
                                        DA=''

                                if DA =="òrain-“pop" and  "”" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("”")
                                        DA=''

                                if DA =="f’" and  "a" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("a")
                                        DA=''


                                if DA =="F’" and  "a" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("a")
                                        DA=''
                                        
                                if DA =="de’" and  "n" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("n")
                                        DA=''

                                if DA =="Gu" and  "dé" in self.tokensetF1[i:i+2]: 
                                       # print (''.join(self.tokensetF1[i:i+3]))
                                        self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("dé")
                                        DA=''
                                        
                                if DA =="mu" and  "thràth" in self.tokensetF1[i:i+2]: 
                                        self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("thràth")
                                        DA=''

                                if DA =="Mu’" and  "n" in self.tokensetF1[i:i+2]: 
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("n")
                                        DA=''

                                if DA =="mu’" and  "n" in self.tokensetF1[i:i+2]: 
                                        self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("n")
                                        DA=''

                                if DA =="An" and  "dràsda" in self.tokensetF1[i:i+2]: 
                                        self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("dràsda")
                                        DA=''
                                        
                                if DA =="an" and  "dràsda" in self.tokensetF1[i:i+2]: 
                                        self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("dràsda")
                                        DA=''
                                         
                                       
                                if DA =="Srath" and  "Chluaidh" in self.tokensetF1[i:i+2]: 
                                        self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("Chluaidh")
                                        DA=''


                                if DA =="ma" and  "tha" in self.tokensetF1[i:i+2]: 
                                        self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("tha")
                                        DA=''

                                if DA =='Roinn' and  "Eòrpa" in self.tokensetF1[i:i+2]:
                                        self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                        self.tokensetF1.remove("Eòrpa")
                                        DA=''

                                if DA =='Phort' and  "Rìgh" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("Rìgh")
                                                DA=''

                                if DA =='dhen' and  "an" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("an")
                                                DA=''
                                     
                                if DA =='bhon' and  "'n" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                               # self.tokensetF1.remove("bhon")
                                                self.tokensetF1.remove("'n")
                                                DA=''

                                if DA =='làn' and  "-Ghàidhealtachd" in self.tokensetF1[i:i+3]: #it is important to consider the next 3 tokens instead of 2 because there is some blank token created in between
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+3]))
                                               # self.tokensetF1.remove("bhon")
                                                self.tokensetF1.remove("-Ghàidhealtachd")
                                                DA=''

                                if DA =='leth' and  "-Ghàidhealtachd" in self.tokensetF1[i:i+3]: # it is important to consider the next 3 tokens instead of 2 because there is some blank token created in between
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+3]))
                                               # self.tokensetF1.remove("bhon")
                                                self.tokensetF1.remove("-Ghàidhealtachd")
                                                DA=''


                                if DA =='bhon' and  "an" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("an")
                                                DA=''
                                                
                                if DA =="o’" and  "n" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("n")
                                                DA=''

                                if DA =='bhon' and "a'" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                               
                                                self.tokensetF1.remove("a'")
                                                DA=''

                                if DA =='Loch' and "Aillse" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("Aillse")
                                                DA=''

                                if DA =='a' and "b'" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("b'")
                                                DA=''
                                                
                                if DA =='a' and "b’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("b’")
                                                DA=''

                                if DA =="a'" and "shineach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                #self.tokensetF1.remove("a'")
                                                self.tokensetF1.remove("shineach")
                                                DA=''


                                if DA =="a’" and "s" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                #self.tokensetF1.remove("a'")
                                                self.tokensetF1.remove("s")
                                                DA=''
                                                
                                if DA =="a" and "shineach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("shineach")
                                                DA=''

                              
                                if DA== "Caledonian"  and "Mac" in self.tokensetF1[i:i+2] and "a’ " in self.tokensetF1[i:i+3] and "Bhruthainn" in self.tokensetF1[i:i+4]:
                                                #print (' '.join(self.tokensetF1[i:i+4]))
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+4]))
                                                DA = ''

                                if DA== "Caledonian"  and "Mac" in self.tokensetF1[i:i+2] and "a' " in self.tokensetF1[i:i+3] and "Bhruthainn" in self.tokensetF1[i:i+4]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+4]))
                                                self.tokensetF1.remove("Mac")
                                                self.tokensetF1.remove("a'")
                                                self.tokensetF1.remove("Bhruthainn")
                                                DA = ''
                                
                                                
                                if DA =='dhan' and "an" in self.tokensetF1[i:i+2] and "sin" in self.tokensetF1[i:i+3] :
                                                self.tokensetF2.append('dhan')
                                                self.tokensetF2.append('an sin')
                                                self.tokensetF1.remove("an")
                                                self.tokensetF1.remove("sin")
                                                DA=''
                                                         
                          
                                if DA =='fon' and  "a'" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("a'")
                                                DA=''

                                if DA =='s' and  "a" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("a")
                                                DA=''

                                if DA =='prionns' and  "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA='' 

                                if DA =='leams' and  "'" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("'")
                                                DA='' 
                                                
                                if DA =='leams' and  "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA=''
                                                
                                if DA =='fon' and "an" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("an")
                                                DA=''

                                if DA =='fon' and "an" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("an")
                                                DA=''

                                if DA =='ionnsaicht' and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA=''

                                if DA =='ionnsaicht' and "'" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("'")
                                                DA=''

                                if DA =='Dùn' and "Èideann" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("Èideann")
                                                DA=''
                                                
                                if DA =='an' and "toiseach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("toiseach")
                                                DA=''

                                if DA =="‘n" and "toiseach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("toiseach")
                                                DA=''

                                if DA =="'n" and "toiseach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("toiseach")
                                                DA=''

                                if DA =="a" and "tuath" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("tuath")
                                                DA=''

                                if DA =="air" and "choireigin-ach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("choireigin-ach")
                                                DA=''
                                                
                                if DA =="an" and "raoir" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("raoir")
                                                DA=''
                                                
                                if DA =="a" and "chaoidh" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("chaoidh")
                                                DA=''

                                if DA =='mun' and  "a'" in self.tokensetF1[i:i+2]:
                                               # print (' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("a'")
                                                DA=''

                                if DA =='mun' and "an" in self.tokensetF1[i:i+2]:
                                               # print (' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("an")
                                                DA=''


                                if DA =='on' and  "a'" in self.tokensetF1[i:i+2]:
                                               # print (' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("a'")
                                                DA=''

                                if DA =='on' and "an" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("an")
                                                DA=''

                                if DA =='ron' and  "a'" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("a'")
                                                DA=''

                                if DA =='oidhch' and  "’." in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append("oidhch’")
                                                self.tokensetF2.append(".")
                                                self.tokensetF1.remove("’.")
                                                DA=''

                                if DA =='ron' and  "an" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("an")
                                                DA=''

                                if DA =='tron' and  "a'" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("a'")
                                                DA=''

                                if DA =='Coille' and  "Chaoil" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("Chaoil")
                                                DA=''

                                if DA =='Gleann' and  "Dail" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("Dail")
                                                DA=''

                                if DA =='Ruaidh' and  "Mhònaidh" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("Mhònaidh")
                                                DA=''

                                if DA =='tron' and "an" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("an")
                                                DA=''

                                if DA =="de'" and "n" in self.tokensetF1[i:i+2]:
                                               self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                               self.tokensetF1.remove("n")
                                               DA=''
                               
                                                
                                if DA =="mu'" and "n" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("n")
                                                DA=''
                                                
                                if DA =="do'" and "n" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("n")
                                                DA=''

                                if DA =="doesn'" and "t" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("t")
                                                DA=''
                                                
                                if DA =="a" and "staigh" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("staigh")
                                                DA=''
                                                
                                if DA =="a" and "steach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("steach")
                                                DA=''
                                                
                                if DA =="a" and "mach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("mach")
                                                DA=''
                                                
                                if DA =="sam" and "bith" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("bith")
                                                DA=''
                                                
                                if DA =="Roinn" and "Eorpa" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("Eorpa")
                                                DA=''
                                                
                                if DA =="air" and "choireigin" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("choireigin")
                                                DA=''
                                                
                                if DA =="a" and "sin" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("sin")
                                                DA=''
                                                
                                if DA =="an" and "sin" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("sin")
                                                DA=''


                                if DA =="Eilean" and "Sgitheanach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("Sgitheanach")
                                                DA=''

                                if DA =="Fairy" and "Bridge" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("Bridge")
                                                DA=''


                                if DA =="Eilean" and "Tiridhe" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("Tiridhe")
                                                DA=''

                                if DA =="a" and "chèile" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("chèile")
                                                DA=''

                                if DA =="Dùn" and "Bheagain" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("Bheagain")
                                                DA=''

                                if DA =="Gleann" and "Ois" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("Ois")
                                                DA=''

                                if DA =="ana" and "nàdarra" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("nàdarra")
                                                DA=''

                                if DA== "An" and "Aodann" in self.tokensetF1[i:i+2] and "Bàn" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("Aodann")
                                                self.tokensetF1.remove("Bàn")
                                                DA=''
                                 
                                
                                               
                                if DA== "a" and "bhòn-dè" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("bhòn-dè")
                                                DA=''
                                                
                                if DA== "a'" and "bhòn-dè" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("bhòn-dè")
                                                DA=''
                                                
                                if DA== "Pholl" and "a'" in self.tokensetF1[i:i+2] and "Ghrùthain" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("Ghrùthain")
                                                self.tokensetF1.remove("a'")
                                                DA=''
                               

                                                
                                if DA== "ann" and "a" in self.tokensetF1[i:i+2] and "shiud" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("a")
                                                self.tokensetF1.remove("shiud")
                                                DA=''
                                                
                                if DA== "ann" and "an" in self.tokensetF1[i:i+2] and "shiud" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("an")
                                                self.tokensetF1.remove("shiud")
                                                DA=''

                                if DA== "ann" and "an" in self.tokensetF1[i:i+2] and "seo" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("an")
                                                self.tokensetF1.remove("ann")
                                                DA='' 

                                if DA== "ann" and "an" in self.tokensetF1[i:i+2] and "siud" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("an")
                                                self.tokensetF1.remove("siud")
                                                DA=''

                                if DA== "ann" and "an" in self.tokensetF1[i:i+2] and "sin" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("an")
                                                self.tokensetF1.remove("sin")
                                                DA='' 
                                
                                if DA== "a'" and "bhòn-raoir" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("a'")
                                                self.tokensetF1.remove("bhòn-raoir")
                                                DA=''

                                if DA== "a'" and "s" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("s")
                                                DA=''

                                if DA== "a" and "bhòn-raoir" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("a")
                                                self.tokensetF1.remove("bhòn-raoir")
                                                DA=''

                                                      
                                if DA== "a" and "bhòn" in self.tokensetF1[i:i+2] and "raoir" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("a")
                                                self.tokensetF1.remove("bhòn")
                                                self.tokensetF1.remove("raoir")
                                                DA=''

                                if DA== "a'" and "bhòn-uiridh" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("a'")
                                                self.tokensetF1.remove("bhòn-uiridh")
                                                DA=""

                                if DA== "a" and "bhòn-uiridh" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("a")
                                                self.tokensetF1.remove("bhòn-uiridh")
                                                DA=""

                                if DA== "a" and "bhòn" in self.tokensetF1[i:i+2] and "uiridh" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("a")
                                                self.tokensetF1.remove("bhòn")
                                                self.tokensetF1.remove("uiridh")
                                                DA=""

                                if DA== "a'" and "bhòn-uiridh" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("bhòn-uiridh")
                                                DA=""

                                if DA== "a" and "bhos" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("bhos")
                                                DA=""
                                                
                                if DA== "a" and "bhàn" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("bhàn")
                                                DA=""

                                if DA== "a" and "mach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("mach")
                                                DA=""

                                if DA== "a" and "màireach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("màireach")
                                                DA=""

                                if DA== "am" and "màireach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("bliadhna")

                                if DA== "a" and "muigh" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove('a')
                                                self.tokensetF1.remove("muigh")
                                                DA=""
                                                
                                if DA== "a" and "nall" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("a")
                                                self.tokensetF1.remove("nall")
                                                DA=""

                                if DA== "an" and "ath-bhliadhna" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("an")
                                                self.tokensetF1.remove("ath-bhliadhna")
                                                DA=""

                                if DA== "an" and "ath" in self.tokensetF1[i:i+2] and "bhliadhna" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("ath")
                                                self.tokensetF1.remove("bhliadhna")
                                                DA=""
                                                
                                if DA== "an" and "ath-oidhche" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("ath-oidhche")
                                                DA=""
                                               

                                if DA== "an" and "ath" in self.tokensetF1[i:i+2] and "oidhche" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("ath")
                                                self.tokensetF1.remove("oidhche")
                                                DA=""
                                                
                                if DA== "an" and "ath" in self.tokensetF1[i:i+2] and "oidhch'" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("ath")
                                                self.tokensetF1.remove("oidhch'")
                                                DA=""
                                                
                                if DA== "an" and "ath-oidhche" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("ath-oidhche")
                                                DA=""

                                if DA== "an" and "ath-sheachdainn" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("ath-sheachdainn")
                                                DA=""

                                if DA== "an" and "ath" in self.tokensetF1[i:i+2] and "sheachdainn" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("an")
                                                self.tokensetF1.remove("sheachdainn")
                                                DA=""
                                
                                if DA== "an" and "ath-sheachdain" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("ath-sheachdain")
                                                DA=""
                                                
                                
                                                
                                if DA== "an" and "ath" in self.tokensetF1[i:i+2] and "sheachdain" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("an")
                                                DA=""

                                if DA== "an" and "còmhnaidh" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("an")
                                                DA=""
                                                
                                if DA== "an" and "de" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("de")
                                                DA=""
                                                
                                if DA== "an" and "diugh" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("diugh")
                                                DA=""
                                                
                                if DA== "an" and "dràsta" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("dràsta")
                                                DA=""
                                                
                                if DA== "an" and "earar" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("earar")
                                                DA=''

                                if DA== "an" and "earair" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("earair")
                                                DA=""

                                if DA== "a" and "nis" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("nis")
                                                DA=''

                                if DA== "a" and "nisd" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("nisd")
                                                DA=""


                                if DA== "a" and "nochd" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("nochd")
                                                DA=''

                                if DA== "a" and "nuas" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("nuas")
                                                DA=""

                                if DA== "a" and "uiridh" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("uiridh")
                                                DA=''

                                if DA== "a" and "null" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("null")
                                                DA=""

                                if DA== "a" and "raoir" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("raoir")
                                                DA=""

                                if DA== "a" and "rithist" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("rithist")
                                                DA=""

                                if DA== "a" and "staidh" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("staidh")
                                                DA=""
                                                
                                if DA== "a" and "steach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("steach")
                                                DA=""
                                                
                                if DA== "b" and "e" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append("b'")
                                                self.tokensetF2.append("e")         
                                                self.tokensetF1.remove("b")
                                                DA=""
                                if DA== "mi'" :
                                                self.tokensetF2.append("mi")
                                                self.tokensetF2.append("'")         
                                                self.tokensetF1.remove("mi'")
                                                DA=""
                                                
                                if DA== "na"  and "s" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append("na's")
                                                self.tokensetF1.remove('s')
                                                DA=""

                                if DA== "na"  and "bu" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove('bu')
                                                DA=""

                                if DA== "a"  and "bu'" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("bu'")
                                                DA=""

                                                
                                if DA== "Inbhir"  and "Nis" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("Nis")
                                                DA=""

                                if DA== "ann"  and "am" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("am")
                                                DA=""
                                        
                                if DA== "ann"  and "an" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("an")
                                                DA=""


                                if DA== "an"  and "siud" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("siud")
                                                DA=""

                                if DA== "ann"  and "an" in self.tokensetF1[i:i+2] and "siud" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("an")
                                                self.tokensetF1.remove("siud")
                                                DA=""
                                                
                                if DA== "an"  and "am" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("am")
                                                DA=""
                                                
                                if DA== "pòs"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove('’')
                                                DA = '' 

                                if DA== "gàir"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove('’')
                                                DA = '' 
                                                 
                                if DA== "an"  and "ceart-uair" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove('ceart-uair')
                                                DA = ''
                                                


                                if DA== "an"  and "sineach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove('sineach')
                                                DA = ''

                                
                                if DA== "an"  and "dràsda" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove('dràsda')
                                                DA = ''


                                if DA== "ma"  and "tha" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove('tha')
                                                DA = ''
                                                
                                if DA== "a"  and "sineach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove('sineach')
                                                DA = ''

                                
                                if DA== "an"  and "ceartuair" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove('ceartuair')
                                                DA = ''
                                                
                                if DA== "fhad"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA = ''

                                               
                                if DA== "ge"  and "brì" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove('brì')
                                                DA = ''

                                if DA== "ge"  and "brith" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove('brith')
                                                DA = ''
                                
                                if DA== "ge"  and "be" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("be")
                                                DA = ''

                                if DA== "ge"  and "'s" in self.tokensetF1[i:i+2] and "bith" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("'s")
                                                self.tokensetF1.remove("bith")
                                                DA = ''

                                if DA== "gar"  and "bith" in self.tokensetF1[i:i+2] :
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("bith")
                                                DA = ''

                                                      
                                if DA== "air"  and "falbh" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("falbh")
                                                DA = '' 

                                if DA== "an"  and "làrna-mhàireach" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("làrna-mhàireach")
                                                DA = '' 

                                if DA== "ma"  and "dh'" in self.tokensetF1[i:i+2] and "fhaoidhte" in self.tokensetF1[i:i+3] :
                                                x = self.tokensetF1[i:i+3]
                                                xx = ' '.join(x[:2])
                                                y = ''.join(x[2:])
                                               # print (xx + y)
                                                self.tokensetF2.append(xx + y)
                                                self.tokensetF1.remove("dh'")
                                                self.tokensetF1.remove("fhaoidhte")
                                                DA = ''
                                                
                                if DA== "ma"  and "dh'" in self.tokensetF1[i:i+2] and "fhaoite" in self.tokensetF1[i:i+3] :
                                                x = self.tokensetF1[i:i+3]
                                                xx = ' '.join(x[:2])
                                                y = ''.join(x[2:])
                                                self.tokensetF2.append(xx + y)
                                                self.tokensetF1.remove("dh'")
                                                self.tokensetF1.remove("fhaoite")
                                                DA = ''


                                      
                                if DA== "math"  and "dh'" in self.tokensetF1[i:i+2] and "fhaoite" in self.tokensetF1[i:i+3] :
                                                x = self.tokensetF1[i:i+3]
                                                xx = ' '.join(x[:2])
                                                y = ''.join(x[2:])
                                                self.tokensetF2.append(xx + y)
                                                self.tokensetF1.remove("dh'")
                                                self.tokensetF1.remove("fhaoite")
                                                DA = ''
                                                
                                if DA== "math"  and "dh'" in self.tokensetF1[i:i+2] and "fhaoidte" in self.tokensetF1[i:i+3] :
                                                x = self.tokensetF1[i:i+3]
                                               # print (x)
                                                xx = ' '.join(x[:2])
                                                y = ''.join(x[2:])
                                                #print (xx + y)
                                                self.tokensetF2.append(xx + y)
                                                self.tokensetF1.remove("dh'")
                                                self.tokensetF1.remove("fhaoidte")
                                                DA = ''
                                                


                                if DA== "nach"  and "maireann" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("maireann")
                                                DA = ''

                                if DA== "gu"  and "dè" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("gu")
                                                DA = ''

                                if DA== "a"  and "chèil" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("chèil")
                                                DA = ''

                                if DA== "mu"  and "dheireadh" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("dheireadh")
                                                DA = ''

                                if DA== "a"  and "h-uile" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("h-uile")
                                                DA = ''

                               
                                if DA== "a"  and "seo" in self.tokensetF1[i:i+2]:
                                                #print (' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("seo")
                                                DA = ''

                                if DA== "an"  and "seo" in self.tokensetF1[i:i+2]:
                                                #print (' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("seo")
                                                DA = ''

                                if DA== "ann"  and "an" in self.tokensetF1[i:i+2] and "seo" in self.tokensetF1[i:i+3]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("an")
                                                self.tokensetF1.remove("seo")
                                                DA = ''

                                if DA== "a"  and "niste" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("niste")
                                                DA = ''

                                if DA== "a"  and "niste" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("niste")
                                                DA = ''
                               
                                if DA== "ge"  and "b'" in self.tokensetF1[i:i+2] and "e" in self.tokensetF1[i:i+3] and "air" in self.tokensetF1[i:i+4] and "bith" in self.tokensetF1[i:i+5]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+5]))
                                                self.tokensetF1.remove("b'")
                                                self.tokensetF1.remove("e")
                                                self.tokensetF1.remove("air")
                                                self.tokensetF1.remove("bith")
                                                DA = ''

                                if DA== "tuilleadh"  and "'s" in self.tokensetF1[i:i+2] and "a" in self.tokensetF1[i:i+3] and "chòir" in self.tokensetF1[i:i+4]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+4]))
                                                self.tokensetF1.remove("'s")
                                                self.tokensetF1.remove("a")
                                                self.tokensetF1.remove("chòir")
                                                DA = ''
                                                
                                if DA== "tuilleadh"  and "'s" in self.tokensetF1[i:i+2] and "a" in self.tokensetF1[i:i+3] and "chòir" in self.tokensetF1[i:i+4]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+4]))
                                                self.tokensetF1.remove("'s")
                                                self.tokensetF1.remove("a")
                                                self.tokensetF1.remove("chòir")
                                                DA = ''

                                if DA== "tuilleadh"  and "sa" in self.tokensetF1[i:i+2] and "chòir" in self.tokensetF1[i:i+3] :
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("sa")
                                                self.tokensetF1.remove("chòir")
                                                DA = ''
                                                
                                if DA== "ann"  and "a'" in self.tokensetF1[i:i+2] and "shiudach" in self.tokensetF1[i:i+3] :
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("shiudach")
                                                self.tokensetF1.remove("a'")
                                                DA = ''
                                                
                                if DA== "ann"  and "a" in self.tokensetF1[i:i+2] and "shiudach" in self.tokensetF1[i:i+3] :
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("shiudach")
                                                self.tokensetF1.remove("a")
                                                DA = ''

                                if DA== "a's"  and "a" in self.tokensetF1[i:i+2] and "sineach" in self.tokensetF1[i:i+3] :
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("a")
                                                self.tokensetF1.remove("sineach")
                                                DA = ''
                                                
                                if DA== "ann"  and "a" in self.tokensetF1[i:i+2] and "shineach" in self.tokensetF1[i:i+3] :
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("a")
                                                self.tokensetF1.remove("ann")
                                                DA = ''

                                if DA== "ann"  and "an" in self.tokensetF1[i:i+2] and "shin" in self.tokensetF1[i:i+3] :
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("an")
                                                self.tokensetF1.remove("shin")
                                                DA = ''
                                else:
                                         if DA== "ann"  and "an" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("an")
                                               # self.tokensetF1.remove("shin")
                                                DA = ''

                                if DA== "ann"  and "an" in self.tokensetF1[i:i+2] and "seo" in self.tokensetF1[i:i+3] :
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("an")
                                                self.tokensetF1.remove("seo")
                                                DA = ''

                                else:
                                         if DA== "ann"  and "seo" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("seo")
                                               # self.tokensetF1.remove("shin")
                                                DA = ''


                                if DA== "brist"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA = ''

                                if DA== "lost-s"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA = ''

                                if DA== "thoilicht"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA = ''


                                if DA== "thus"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA = ''

                                if DA== "ath-oidhch"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA = ''

                                if DA== "bonnant"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA = ''

                                if DA== "bheath"  and "’." in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append("bheath’")
                                                self.tokensetF2.append(".")
                                                self.tokensetF1.remove("’.")
                                                DA = ''
                                                
                                if DA== "bheath"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA = ''
                                                
                                if DA== "chual"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA = ''

                                                     
                                if DA== "uisg"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA = ''

                                if DA== "uisg"  and "’." in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append("uisg’")
                                                self.tokensetF2.append(".")
                                                self.tokensetF1.remove("’.")
                                                DA = ''

                                if DA== "teoth"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA = '' 
                                        
                                if DA== "do-sheachant"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA = ''

                                if DA== "dòch"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA = ''
                                                
                                if DA== "bioraicht"  and "’" in self.tokensetF1[i:i+2]:
                                                self.tokensetF2.append(''.join(self.tokensetF1[i:i+2]))
                                                self.tokensetF1.remove("’")
                                                DA = '' 

                                        
                                if DA== "ann"  and "a" in self.tokensetF1[i:i+2] and "shin" in self.tokensetF1[i:i+3] :
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("a")
                                                self.tokensetF1.remove("shin")
                                                DA = ''

                                if DA== "ann"  and "a" in self.tokensetF1[i:i+2] and "sheo" in self.tokensetF1[i:i+3] :
                                                self.tokensetF2.append(' '.join(self.tokensetF1[i:i+3]))
                                                self.tokensetF1.remove("a")
                                                self.tokensetF1.remove("sheo")
                                                DA = ''
                                                
                                if DA== "(’"  and "S" in self.tokensetF1[i:i+2] :
                                                self.tokensetF2.append("(")
                                                self.tokensetF2.append("’S")
                                                self.tokensetF1.remove("S")
                                                DA = ''

                                if DA== "(’"  and "s" in self.tokensetF1[i:i+2] :
                                                self.tokensetF2.append("(")
                                                self.tokensetF2.append("’s")
                                                self.tokensetF1.remove("s")
                                                DA = ''


                                              
                                else:
                                                self.tokensetF2.append(DA)  


                                

                      for  i, nn in enumerate(self.tokensetF2):
        
                          secondQuots = re.findall(r"(\w+[' " "])", str(nn)) ## appostrophe 
                          secondQuots1 = re.findall(r"(?<!=[' " "])\w+", str(nn))

                          if len(nn)< 4 and secondQuots and  "s" in self.tokensetF2[i:i+2]:  ##  reconstructs possesive tokens (eg M's)
                       
                                    dd = ''.join(self.tokensetF2[i:i+2])
                                    self.tokensetF3.append(dd.strip())
                                    nn = ''
            
        
                          if nn in self.abbr  and "." in self.tokensetF2[i:i+2]:
                                self.tokensetF3.append(''.join(self.tokensetF2[i:i+2]))
                                nn=''

                          if nn =="la’"  and "r-na-mhàireach" in self.tokensetF2[i:i+2]:
                                self.tokensetF3.append(''.join(self.tokensetF2[i:i+2]))
                                nn=''
                                self.Junk.append("r-na-mhàireach")

                          if nn =="dhìoms"  and "’" in self.tokensetF2[i:i+2]:
                                self.tokensetF3.append(''.join(self.tokensetF2[i:i+2]))
                                self.tokensetF2.remove("’")
                                nn=''
                                        

                          else:
                             self.tokensetF3.append(nn.strip())

                     
                      for q in self.tokensetF3:
                            if q not in self.Junk and ''.join(q)!='':
                                self.tokensetF4.append(q)


                      for x in self.tokensetF4:
                            y = re.sub("[‘’´`]", "'", str(x)) ## normliasing apostrophies
               
                            w = re.sub("[“”]", '"', str(y))
                        
                            self.tokensetF5.append(w)

                  
                      return self.tokensetF5

                    


class Tagger(GaelicTokeniser, GaelicPartOfSpeechTagger):
                 def  __init__(self):
                     GaelicTokeniser.__init__(self)
                     GaelicPartOfSpeechTagger. __init__(self, 'inputfile', 'outputfile')
                
                 
                 def tagDefault(self):
                      #self.inputlist = inputlist
                      self.tkonisedText=[]
                      self.TokenSetSentence = []
                      self.TagSetSentence =[]
                      self.TokenTagSetSentence =[]
                      self.tkonisedTag=[]
                      self.overSample = []
                      self.englishLexicon = ''
                      self.BrillAmendedOutput= ''
                      self.algT = []
                      self.algV = []
                                      
                      self.trainingFile = csv.reader(codecs.open(os.path.join(os.getcwd(), 'data', 'TrainingFile10102014.csv'),'r'))
                     # self.trainingFile = csv.reader(codecs.open(r'C:\ScottishGaelicProject\TestSystem\data\TrainingFile10102014.csv','r'))
                      self.englishLexicon  = list(csv.reader(codecs.open(os.path.join(os.getcwd(), 'data', 'EnglishLexiconFinal06082014.csv'),'r')))
                      #self.englishLexicon  = list(csv.reader(codecs.open(r'C:\ScottishGaelicProject\TestSystem\data\EnglishLexiconFinal06082014.csv','r')))
  
                      for y in self.trainingFile:
                          x1 = y[:1]
                          x2=y[1:]
                          if ''.join(x1) =='':
                              self.TokenSetSentence.append(self.tkonisedText)
                              self.tkonisedText = []
                              self.TagSetSentence.append(self.tkonisedTag)
                              self.tkonisedTag = []
                          else:
                              self.tkonisedText.extend(x1)
                              self.tkonisedTag.extend(x2)

                      for i, c in enumerate(self.TokenSetSentence):
                                   for ii,b in enumerate(self.TagSetSentence):
                                           if i == ii:
                                               xx = zip(c, b)
                                               self.TokenTagSetSentence.append(list(xx))

 
                      print ("Number of Sentences in training file:", len(self.TokenTagSetSentence))
                      for x in range(int((len(self.TokenTagSetSentence)/100)*50)):
                                    a = random.randrange(1, len(self.TokenTagSetSentence), 2)
                                    self.overSample.append(self.TokenTagSetSentence[a])

                      self.TokenTagSetSentence.extend(self.overSample)

          
                      print ("Number of Sentences in training set after oversmaple:", len(self.TokenTagSetSentence))

                      

                      default_tagger = nltk.DefaultTagger('Ncsmn')

                      Afitagger = nltk.AffixTagger(self.TokenTagSetSentence, affix_length=-3, min_stem_length=3, backoff=default_tagger)
                      Afitagger1 = nltk.AffixTagger(self.TokenTagSetSentence, affix_length=2, min_stem_length=2, backoff=Afitagger)
                      Unitagger = UnigramTagger(self.TokenTagSetSentence, backoff=Afitagger1)
                                        

                      templates = [
                            SymmetricProximateTokensTemplate(ProximateTagsRule, (1,1)),
                            SymmetricProximateTokensTemplate(ProximateTagsRule, (2,2)),
                            SymmetricProximateTokensTemplate(ProximateTagsRule, (1,2)),
                            SymmetricProximateTokensTemplate(ProximateTagsRule, (1,3)),
                            SymmetricProximateTokensTemplate(ProximateTagsRule, (1,4)),
                            SymmetricProximateTokensTemplate(ProximateTagsRule, (1,5)),
                            SymmetricProximateTokensTemplate(ProximateWordsRule, (1,1)),
                            SymmetricProximateTokensTemplate(ProximateWordsRule, (2,2)),
                            SymmetricProximateTokensTemplate(ProximateWordsRule, (1,2)),
                            SymmetricProximateTokensTemplate(ProximateWordsRule, (1,3)),
                            SymmetricProximateTokensTemplate(ProximateWordsRule, (1,4)),
                            SymmetricProximateTokensTemplate(ProximateWordsRule, (1,5)),
                            ProximateTokensTemplate(ProximateTagsRule, (-1, -1), (1,1)),
                            ProximateTokensTemplate(ProximateWordsRule, (-1, -1), (1,1)),
                            ProximateTokensTemplate(ProximateTagsRule, (-2, -2), (2,2)),
                            ProximateTokensTemplate(ProximateWordsRule, (-2, -2), (2,2)),
                            ProximateTokensTemplate(ProximateWordsRule, (-3, -3), (3,3)),
                            ProximateTokensTemplate(ProximateWordsRule, (-4, -4), (4,4)),
                            ProximateTokensTemplate(ProximateWordsRule, (-5, -5), (5,5)),
                            ]

                      trainer = FastBrillTaggerTrainer(initial_tagger=Unitagger, templates=templates, trace=0, deterministic=True)

                      brill_tagger = trainer.train(self.TokenTagSetSentence, max_rules=200, min_score=2)
                      
                      saveDefaultModel(brill_tagger)

                      return 
                      
                     


                 def tagSimplified(self,inputlist):
                      self.inputlist = inputlist
                      self.tkonisedText=[]
                      self.TokenSetSentence = []
                      self.TagSetSentence =[]
                      self.TokenTagSetSentence =[]
                      self.tkonisedTag=[]
                      self.overSample = []
                      self.englishLexicon = ''
                      self.BrillAmendedOutput= ''
                      self.algT = []
                      self.algV = []
                                      
                      self.trainingFile = csv.reader(codecs.open(os.path.join(os.getcwd(), 'data', 'TrainingFile10102014.csv'),'r'))
                      #self.trainingFile = csv.reader(codecs.open(r'C:\ScottishGaelicProject\TestSystem\data\SimplifiedTrainingFile17112014.csv','r'))
                      self.englishLexicon  = list(csv.reader(codecs.open(os.path.join(os.getcwd(), 'data', 'EnglishLexiconFinal06082014.csv'),'r')))
                      #self.englishLexicon  = list(csv.reader(codecs.open(r'C:\ScottishGaelicProject\TestSystem\data\EnglishLexiconFinal06082014.csv','r')))
  
                      for y in self.trainingFile:
                              x1 = y[:1]
                              x2=y[1:]
                              if ''.join(x1) =='':
                                  self.TokenSetSentence.append(self.tkonisedText)
                                  self.tkonisedText = []
                                  self.TagSetSentence.append(self.tkonisedTag)
                                  self.tkonisedTag = []
                              else:
                                  self.tkonisedText.extend(x1)
                                  self.tkonisedTag.extend(x2)

                      for i, c in enumerate(self.TokenSetSentence):
                                   for ii,b in enumerate(self.TagSetSentence):
                                           if i == ii:
                                               xx = zip(c, b)
                                               self.TokenTagSetSentence.append(list(xx))

 
                      print ("Number of Sentences in training file:", len(self.TokenTagSetSentence))
                      for x in range(int((len(self.TokenTagSetSentence)/100)*50)):
                                    a = random.randrange(1, len(self.TokenTagSetSentence), 2)
                                    self.overSample.append(self.TokenTagSetSentence[a])

                      self.TokenTagSetSentence.extend(self.overSample)

          
                      print ("Number of Sentences in training set after oversmaple:", len(self.TokenTagSetSentence))

                      

                      default_tagger = nltk.DefaultTagger('Nc')

                      Afitagger = nltk.AffixTagger(self.TokenTagSetSentence, affix_length=-3, min_stem_length=3, backoff=default_tagger)
                      Afitagger1 = nltk.AffixTagger(self.TokenTagSetSentence, affix_length=2, min_stem_length=2, backoff=Afitagger)
                      Unitagger = UnigramTagger(self.TokenTagSetSentence, backoff=Afitagger1)
                                        

                      templates = [
                            SymmetricProximateTokensTemplate(ProximateTagsRule, (1,1)),
                            SymmetricProximateTokensTemplate(ProximateTagsRule, (2,2)),
                            SymmetricProximateTokensTemplate(ProximateTagsRule, (1,2)),
                            SymmetricProximateTokensTemplate(ProximateTagsRule, (1,3)),
                            SymmetricProximateTokensTemplate(ProximateTagsRule, (1,4)),
                            SymmetricProximateTokensTemplate(ProximateTagsRule, (1,5)),
                            SymmetricProximateTokensTemplate(ProximateWordsRule, (1,1)),
                            SymmetricProximateTokensTemplate(ProximateWordsRule, (2,2)),
                            SymmetricProximateTokensTemplate(ProximateWordsRule, (1,2)),
                            SymmetricProximateTokensTemplate(ProximateWordsRule, (1,3)),
                            SymmetricProximateTokensTemplate(ProximateWordsRule, (1,4)),
                            SymmetricProximateTokensTemplate(ProximateWordsRule, (1,5)),
                            ProximateTokensTemplate(ProximateTagsRule, (-1, -1), (1,1)),
                            ProximateTokensTemplate(ProximateWordsRule, (-1, -1), (1,1)),
                            ProximateTokensTemplate(ProximateTagsRule, (-2, -2), (2,2)),
                            ProximateTokensTemplate(ProximateWordsRule, (-2, -2), (2,2)),
                            ProximateTokensTemplate(ProximateWordsRule, (-3, -3), (3,3)),
                            ProximateTokensTemplate(ProximateWordsRule, (-4, -4), (4,4)),
                            ProximateTokensTemplate(ProximateWordsRule, (-5, -5), (5,5)),
                            ]

                      trainer = FastBrillTaggerTrainer(initial_tagger=Unitagger, templates=templates, trace=0, deterministic=True)

                      brill_tagger = trainer.train(self.TokenTagSetSentence, max_rules=200, min_score=2)
                      

                      BrillTagSimp = brill_tagger.tag(self.inputlist)

                      for (c, d) in BrillTagSimp: # algorithm output
                                self.algT.append(c)
                                self.algV.append(d)

                      self.BrillAmendedOutputSimp = zip(self.algT,self.algV)

                      return list(self.BrillAmendedOutputSimp)

                                  
              

if __name__ == "__main__":
    buildGUI()
    
    
           


    
    

    
    
    
