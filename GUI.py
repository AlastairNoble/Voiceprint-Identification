from tkinter import *
import numpy as np
import os
from tools.dataCreation import *
from VoiceClassification import *
pi = np.pi
directory_to_project = dir_path = os.path.dirname(os.path.realpath(__file__))
model_val_accuracy = 0.555
model_accuracy = .575
global names
global label_list
global label_list_button

def ChangeScreen(screen, frame):
    for widget in frame.winfo_children():
        widget.destroy()
    screen(window)


def updateLabelList():
    global label_list, label_list_button, names
    label_list = []
    label_list_button = []
    for name in names:
        name_item = name + "Label"
        label_list.append(name_item)
        button_item = name + "LButton"
        label_list_button.append(button_item)


def HighlightLabel(name):
    index = names.index(name)
    for label in label_list:
        if label == label_list[index]:
            pass
        label.config(bg="#F0F0F0")
    label_list[index].config(bg="Yellow")


def captureUserInput(userfield, name_frame, frame2):
    user_name = userfield.get()
    if user_name != "" and user_name not in names:
        names.append(user_name)
        updateLabelList()
        print_names(name_frame)
        record_sentence_UI(user_name, frame2, user_name)


def print_names(frame):
    name_title = Label(frame, text="Speaking", anchor=CENTER, font="Helvetica 20 bold underline")
    name_title.place(x=60, y=0)
    ypos = 50
    for i in range(len(label_list)):
        label_list[i] = Label(frame, text=names[i], anchor=CENTER, font="Helvetica 16 bold", height=0, width=10)
        label_list[i].place(x=0, y=ypos)
        label_list_button[i] = Button(frame, text="X", anchor=CENTER, font="Helvetica 10", command=lambda i=i: delete_user(names[i], frame))
        label_list_button[i].place(x=200, y=ypos)
        ypos += 30


def delete_user(name_item, frame):
    shutil.rmtree(f"words\\sentence\\{name_item}")
    for i in range(len(label_list)):
        label_list[i].destroy()
        label_list_button[i].destroy()
    names.remove(name_item)
    updateLabelList()
    ypos=50
    for i in range(len(label_list)):
        label_list[i] = Label(frame, text=names[i], anchor=CENTER, font="Helvetica 16 bold", height=0, width=10)
        label_list[i].place(x=0, y=ypos)
        label_list_button[i] = Button(frame, text="X", anchor=CENTER, font="Helvetica 10",command=lambda i=i: delete_user(names[i], frame))
        label_list_button[i].place(x=200, y=ypos)
        ypos += 30
    # print_names(frame)


def continue_function(instructions, button, user_input):
    global iteration
    if iteration == 1:
        instructions.config(text="Record this Sentence:\nThat quick beige fox jumped in\nthe air over each thin dog. \nLook out, I shout, for he\'s foiled \nyou again, creating chaos")
        button.config(text="Start Recording")
    elif iteration == 2:
        create_recorded_data("sentence", 10)
        instructions.config(text="Stopped Recording")
        button.config(text="Ok")
        break_up_audio(["sentence"])
        export_recordings(user_input, ["sentence"])
    elif iteration == 3:
        instructions.destroy()
        button.destroy()
    iteration += 1


def record_sentence_UI(name, frame, user_input):
    global iteration
    iteration = 1

    instructions1 = Label(frame, text="Get ready to record audio input", anchor=CENTER, font="Helvetica 11")
    instructions1.place(x=5, y=110)

    continue_button = Button(frame, text="Ok", command=lambda: continue_function(instructions1, continue_button, user_input))
    continue_button.place(x=110, y=80)

    # print(f"you will have {10} seconds to read the following sentence \n")
    # sleep(2)
    # print('"That quick beige fox jumped in the air over each thin dog. Look out, I shout, for he\'s foiled you again, creating chaos"\n')
    # sleep(1)
    #
    # create_recorded_data("sentence", 10)
    #
    # break_up_audio(["sentence"])
    #
    # export_recordings(name, ["sentence"])


def train_model_UI(acc_label):
    model = word_model(['sentence'])
    accuracy = model.accuracy[-1]
    acc_label.config(text=f"Accuracy={round(accuracy,3)}")


class HomePage:
    def record_live_setup_UI(self, recordButton, frame):
        recordButton.destroy()
        dir_record_img = directory_to_project + "\\tools\\images\\stop-button.png"
        # Photo for Record Button
        photorecord = PhotoImage(file=dir_record_img)
        photoimagerecord = photorecord.subsample(16, 16)
        panelrecord = Label(frame, image=photoimagerecord)
        panelrecord.photo = photoimagerecord

        stopButton = Button(frame, image=photoimagerecord, relief="flat", border=1, bd=0, highlightthickness=0,
                         command=lambda: print("hi"))
        stopButton.place(x=208, y=5)

        # self.record_live_UI(self)

    # def record_live_UI(self):
    #     self.stopButton.after(1000)
    #     # Change UI display. Delete microphone and add stop button
    #
    #     # Check stop button
    #     print("hi")
    #     # record for 2 sec
    #     # process results
    #     # highlight name


    def __init__(self, master):
        # Control the Menu Bar
        frame1 = Frame(master, height=455, width=500)
        frame1.pack(side=LEFT, anchor=NW)
        frame2 = Frame(frame1, height=455, width=250)
        frame2.place(x=250, y=0)

        optionsframe = Frame(master, height=95, width=500, bg="#ABB2B9")
        optionsframe.place(x=0, y=455)

        dir_record_img = directory_to_project + "\\tools\\images\\microphone-edited.png"
        # Photo for Record Button
        photorecord = PhotoImage(file=dir_record_img)
        photoimagerecord = photorecord.subsample(16, 16)
        panelrecord = Label(frame1, image=photoimagerecord)
        panelrecord.photo = photoimagerecord

        # Functionality of Record Live button
        RecordButton = Button(optionsframe, image=photoimagerecord, relief="flat", border=1, bd=0, highlightthickness=0,
                         command=lambda: self.record_live_setup_UI(RecordButton, optionsframe))
        RecordButton.place(x=208, y=5)

        name_frame = Frame(master, height=400, width=250, borderwidth="4", relief="groove")
        name_frame.place(x=0, y=0)

        print_names(name_frame)

        user_input_title = Label(frame2, text="Options", anchor=CENTER, font="Helvetica 20 bold underline")
        user_input_title.place(x=65, y=0)

        # User Input field
        userfield = Entry(frame2)
        userfield.place(x=5, y=50)
        userfield.focus_set()

        # Button to close temp window
        collect_name = Button(frame2, text="Add User", command=lambda: captureUserInput(userfield, name_frame, frame2))
        collect_name.place(x=140, y=45)

        # Train Model
        TrainModelButton = Button(optionsframe, text="Train Model", command=lambda: train_model_UI(model_accuracy_label), height=2, width=13, font="Helvetica 15 bold")
        TrainModelButton.place(x=315, y=5)

        model_accuracy_label = Label(frame1, text=f"Accuracy= N/A", anchor=CENTER, font="Helvetica 16 bold", height=2)
        model_accuracy_label.place(x=50, y=400)

        # Record new data
        # record live
        # train model - print accuracy


def start_UI():
    global window, names, label_list, label_list_button
    names = os.listdir("words\\sentence")
    updateLabelList()
    print(names, label_list, label_list_button)
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


def main():
    start_UI()


main()
