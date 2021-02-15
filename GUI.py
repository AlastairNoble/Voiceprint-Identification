from tkinter import *
import numpy as np
import os
pi = np.pi
directory_to_project = dir_path = os.path.dirname(os.path.realpath(__file__))


def ChangeScreen(screen, frame):
    for widget in frame.winfo_children():
        widget.destroy()
    screen(window)


def HighlightLabel(label):
    label.config(bg="Yellow")

class HomePage:
    def __init__(self, master):
        # Control the Menu Bar
        frame1 = Frame(master, height=500, width=500)
        frame1.pack(side=LEFT, anchor=NW)

        dir_record_img = directory_to_project + "\\tools\\images\\Record_icon.png"
        # Photo for Record Button
        photorecord = PhotoImage(file=dir_record_img)
        photoimagerecord = photorecord.subsample(2, 2)
        panelrecord = Label(frame1, image=photoimagerecord)
        panelrecord.photo = photoimagerecord

        # Functionality of Record Live button
        RecordButton = Button(frame1, image=photoimagerecord, relief="flat", border=1, bd=0, highlightthickness=0,
                         command=lambda: print("RECORDING"))
        RecordButton.place(x=195, y=410)

        # Add new data
        AddDataButton = Button(frame1, text="Add New Data", command=lambda: print("Add New Data"))
        AddDataButton.place(x=60, y=450)

        HarleyFrame = Frame(master, height=200, width=250, borderwidth="4", relief="groove")
        HarleyFrame.place(x=0, y=0)
        HarleyLabel = Label(HarleyFrame, text="Harley", anchor=CENTER, font="Helvetica 16 bold")
        HarleyLabel.place(x=85, y=80)

        EliFrame = Frame(master, height=200, width=250, borderwidth="4", relief="groove")
        EliFrame.place(x=0, y=200)
        EliLabel = Label(EliFrame, text="Eli", anchor=CENTER, font="Helvetica 16 bold")
        EliLabel.place(x=90, y=80)

        AlistarFrame = Frame(master, height=200, width=250, borderwidth="4", relief="groove")
        AlistarFrame.place(x=250, y=0)
        AlistarLabel = Label(AlistarFrame, text="Alistar", anchor=CENTER, font="Helvetica 16 bold")
        AlistarLabel.place(x=85, y=80)

        AlexFrame = Frame(master, height=200, width=250, borderwidth="4", relief="groove")
        AlexFrame.place(x=250, y=200)
        AlexLabel = Label(AlexFrame, text="Alex", anchor=CENTER, font="Helvetica 16 bold")
        AlexLabel.place(x=90, y=80)

        # Train Model
        TrainModelButton = Button(frame1, text="Train Model", command=lambda: print("Train Model"))
        TrainModelButton.place(x=400, y=450)

        # Record new data
        # record live
        # train model - print accuracy



def main():
    global window
    window = Tk()

    HomePage(window)

    # Set size of the window to not change.
    windowx = 500
    windowy = 500
    window.minsize(windowx, windowy)
    window.maxsize(windowx, windowy)

    # window.after(1, tasks())
    window.mainloop()




main()
