from Tkinter import *
import tkFileDialog
import os
from time import sleep
from dataAcq import target_download
import csv
from analysis_script import target_analysis


class Display(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.index=0
        self.initUI()

        self.image_data = {'tam_cat_sample.csv':'FITS/TAM/',
                          'random_catalog_sample+1000.csv':'FITS/RandSample-1000/',
                          'random_catalog_sample+2000.csv':'FITS/RandSample-2000/',
                          'tycho_2mass_wise_XMATCH-POS.csv':'FITS/Full_Cat/'}
        self.num_data = {'tam_cat_sample.csv':'Results/TAM/',
                          'random_catalog_sample+1000.csv':'Results/RandSample_1000/',
                          'random_catalog_sample+2000.csv':'Results/RandSample_2000/',
                          'tycho_2mass_wise_XMATCH-POS.csv':'Results/Full_Cat/'}

        

    def initUI(self):

        self.parent.title('exocode GUI')
        self.pack(fill=BOTH,expand=1)
        self.frame = Frame(self,relief=RAISED,bd=1)
        self.frame.pack(expand=2,fill=BOTH)
        
        self.data = Frame(self.frame)
        self.data.pack(fill=BOTH,side=LEFT,expand=1)
        top = Frame(self.data,width=40)
        bot = Frame(self.data,height=90)
        top.pack()
        bot.pack(fill=Y)

        self.dwnld = StringVar()
        self.dwnld.set('Checking Download...\nSelect catalog to run')
        self.check = Label(top,textvariable=self.dwnld,anchor=N,justify=LEFT,width=17)
        self.check.pack(side=LEFT,fill=BOTH)
        scrollbar = Scrollbar(bot)
        self.listbox = Listbox(bot, yscrollcommand=scrollbar.set,height=13)
        scrollbar.pack(side=RIGHT,fill=Y)
        self.listbox.pack(side=LEFT,fill=BOTH)

        scrollbar.config(command=self.listbox.yview)

        csv_frame = Frame(self.frame,width=200,padx=5)
        csv_frame.pack(fill=BOTH,side=LEFT,expand=1)
        csv_title = Frame(csv_frame)
        csv_title.pack(fill=BOTH)
        csv_label = Label(csv_title,text='Data')
        csv_label.pack(fill=BOTH)
        self.csv_table = Frame(csv_frame)
        self.csv_table.pack(fill=BOTH)

        grid = Frame(self.csv_table)
        grid.pack(side=LEFT)

        self.l0 = Listbox(grid, height=15)
        self.l1 = Listbox(grid, height=15)
        self.l2 = Listbox(grid, height=15)
        self.l3 = Listbox(grid, height=15)
        self.l4 = Listbox(grid, height=15)
        self.l5 = Listbox(grid, height=15)
        self.l6 = Listbox(grid, height=15)
        self.l7 = Listbox(grid, height=15)
        self.l8 = Listbox(grid, height=15)
        self.l9 = Listbox(grid, height=15)

        self.l0.pack(side=LEFT,fill=Y)
        self.l1.pack(side=LEFT,fill=Y)
        self.l2.pack(side=LEFT,fill=Y)
        self.l3.pack(side=LEFT,fill=Y)
        self.l4.pack(side=LEFT,fill=Y)
        self.l5.pack(side=LEFT,fill=Y)
        self.l6.pack(side=LEFT,fill=Y)
        self.l7.pack(side=LEFT,fill=Y)
        self.l8.pack(side=LEFT,fill=Y)
        self.l9.pack(side=LEFT,fill=Y)



        self.list_map = {0:self.l0,1:self.l1,2:self.l2,3:self.l3,
                    4:self.l4,5:self.l5,6:self.l6,7:self.l7,
                    8:self.l8,9:self.l9}
        list_titles = ['Image Address','Target Index','Target Right Ascension',
                       'Target Declination','Survey','Band',
                       'Number of Central Blobs','Main Blob Center',
                       'Main Blob Radius','Main Blob Displacement',
                       'Percent Outside Diffraction','Threshold Value',
                       'Percent of Image White','Validation','Error']
        list_titles = [list_titles[0],list_titles[2],list_titles[3],
                       list_titles[6],list_titles[7],list_titles[8],
                       list_titles[9],list_titles[11],list_titles[12],list_titles[14]]
        for i in range(len(list_titles)):
            self.list_map[i].insert(END,str(list_titles[i]))

        close_button = Button(self,text='Close',command=self.parent.destroy)
        close_button.pack(side=RIGHT,padx=5,pady=5)
        self.catalog = StringVar()
        self.catalog.set('Select Catalog')
        cat_button = Button(self,textvariable=self.catalog,command=self.update_catalog)
        cat_button.pack(side=RIGHT,padx=5,pady=5)

        self.current = StringVar()
        self.current_id = Label(self.data,textvariable=self.current)
        self.img_display = Button(self.csv_table.master,text='Display Next Index',command=self.data_display)
        self.download_button = Button(self.data,text='Click to Download',command=self.data_protocol)


    def update_catalog(self):
        self.download_button.destroy()
        self.listbox.delete(0, END)
        for key in self.list_map:
            self.list_map[key].delete(1,END)
        self.current.set('')
        self.index=0
        self.catalog_file = tkFileDialog.askopenfilename(initialdir='Catalogs/')
        self.data_container = self.image_data[self.catalog_file.split('/')[-1]]
        self.catalog.set('Catalog: '+self.data_container)
        with open(self.catalog_file,'rb') as f:
            self.num_lines = sum(1 for line in f)
        self.data_button = Button(self.csv_table.master,text='Display New Catalog Data',command=self.data_display)
        for i in range(0,self.num_lines):
            if os.path.isdir(self.data_container+'index-'+str(i)+'/'):
                self.listbox.insert(END,'index-'+str(i)+':   EXISTS')
                if i == self.num_lines-1:
                    print 'success check'
                    self.dwnld.set('\nDownload Complete!')
                    self.check.config(fg='green')
                    
                    self.data_button.pack(side=BOTTOM,fill=X)
            else:
                print 'error check'
                self.listbox.insert(END,'ERROR')
                self.listbox.insert(END,'MISSING index-'+str(i))
                
                self.download_button = Button(self.data,text='Click to Download',command=self.data_protocol)
		self.download_button.pack(padx=5,pady=5)

                self.dwnld.set('\nDownload Incomplete')
                self.check.config(fg='red')
                break


    def data_protocol(self):
        print 'in protocol'
        self.listbox.delete(0,END)
        self.dwnld.set('\nDownloading Now...')
        with open(self.catalog_file,'rb') as csvfile: #rand cat
            reader = csv.reader(csvfile)
            table = [[e for e in r] for r in reader]
        for i in range(self.num_lines):
            target_download(i,self.data_container,table)
            self.listbox.insert(END,'index-'+str(i)+':   EXISTS')
            if i == self.num_lines-1:
                self.dwnld.set('\nDownload Complete!')
                self.check.config(fg='green')
        self.download_button.destroy()
        self.data_button = Button(self.csv_table.master,text='Display New Catalog Data',command=self.data_display)
        self.data_button.pack(side=BOTTOM,fill=X)


    def data_display(self):
        self.data_button.destroy()
        print 'in display'
        for key in self.list_map:
            self.list_map[key].delete(1,END)
        full = target_analysis(self.index,self.data_container)[1:]
        full.sort(key=lambda x: x[0])

        for row in full:
            row = [row[0],row[2],row[3],row[6],row[7],row[8],
                   row[9],row[11],row[12],row[14]]
            for i in range(len(row)):
                self.list_map[i].insert(END,str(row[i]))
        self.index+=1

        self.img_display.pack(padx=5,pady=5)

        self.current.set('\nDisplaying\nIndex '+str(self.index-1))
	self.current_id.pack(padx=5,pady=5)


        
def main():
    root = Tk()
    root.geometry('2000x350')
    app = Display(root)
    root.mainloop()

if __name__ == '__main__':
    main()
