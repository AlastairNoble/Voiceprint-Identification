from tkinter import *
import numpy as np
import os
pi = np.pi
directory_to_project = dir_path = os.path.dirname(os.path.realpath(__file__))
model_val_accuracy = 0.555
model_accuracy = .575

def ChangeScreen(screen, frame):
    for widget in frame.winfo_children():
        widget.destroy()
    screen(window)


def HighlightLabel(label, all_labels):
    for label2 in all_labels:
        if label2 == label:
            pass
        label2.config(bg="#F0F0F0")
    label.config(bg="Yellow")

class HomePage:
    def __init__(self, master):
        # Control the Menu Bar
        frame1 = Frame(master, height=455, width=500)
        frame1.pack(side=LEFT, anchor=NW)

        optionsframe = Frame(master, height=95, width=500, bg="#ABB2B9")
        optionsframe.place(x=0, y=455)

        dir_record_img = directory_to_project + "\\tools\\images\\microphone.png"
        # Photo for Record Button
        photorecord = PhotoImage(file=dir_record_img)
        photoimagerecord = photorecord.subsample(16, 16)
        panelrecord = Label(frame1, image=photoimagerecord)
        panelrecord.photo = photoimagerecord

        # Functionality of Record Live button
        RecordButton = Button(optionsframe, image=photoimagerecord, relief="flat", border=1, bd=0, highlightthickness=0,
                         command=lambda: HighlightLabel(EliLabel, all_labels))
        RecordButton.place(x=208, y=5)

        # Add new data
        AddDataButton = Button(optionsframe, text="Add New Data", command=lambda: HighlightLabel(HarleyLabel, all_labels), height=2, width=13, font="Helvetica 15 bold")
        AddDataButton.place(x=20, y=5)

        HarleyFrame = Frame(master, height=200, width=250, borderwidth="4", relief="groove")
        HarleyFrame.place(x=0, y=0)
        HarleyLabel = Label(HarleyFrame, text="Harley", anchor=CENTER, font="Helvetica 16 bold", height=8, width=18)
        HarleyLabel.place(x=0, y=0)

        EliFrame = Frame(master, height=200, width=250, borderwidth="4", relief="groove")
        EliFrame.place(x=0, y=200)
        EliLabel = Label(EliFrame, text="Eli", anchor=CENTER, font="Helvetica 16 bold", height=8, width=18)
        EliLabel.place(x=0, y=0)

        AlistarFrame = Frame(master, height=200, width=250, borderwidth="4", relief="groove")
        AlistarFrame.place(x=250, y=0)
        AlistarLabel = Label(AlistarFrame, text="Alistar", anchor=CENTER, font="Helvetica 16 bold", height=8, width=18)
        AlistarLabel.place(x=0, y=0)

        AlexFrame = Frame(master, height=200, width=250, borderwidth="4", relief="groove")
        AlexFrame.place(x=250, y=200)
        AlexLabel = Label(AlexFrame, text="Alex", anchor=CENTER, font="Helvetica 16 bold", height=8, width=18)
        AlexLabel.place(x=0, y=0)

        # Train Model
        TrainModelButton = Button(optionsframe, text="Train Model", command=lambda: print("Train Model"), height=2, width=13, font="Helvetica 15 bold")
        TrainModelButton.place(x=315, y=5)

        model_accuracy_label = Label(frame1, text=f"Accuracy={model_accuracy} Value Accuracy={model_val_accuracy}", anchor=CENTER, font="Helvetica 16 bold", height=2)
        model_accuracy_label.place(x=50, y=400)

        all_labels = [AlexLabel, HarleyLabel, AlistarLabel, EliLabel]
        # Record new data
        # record live
        # train model - print accuracy



def main():
    global window
    window = Tk()

    HomePage(window)

    # Icon
    microphone_icon = directory_to_project + "\\tools\\images\\Record_icon.png"
    photo = PhotoImage(file=microphone_icon)
    window.iconphoto(False, photo)

    # Window Title
    window.title('Voice Print Recognition System')

    # Set size of the window to not change.
    windowx = 500
    windowy = 550
    window.minsize(windowx, windowy)
    window.maxsize(windowx, windowy)

    # window.after(1, tasks())
    window.mainloop()




main()
