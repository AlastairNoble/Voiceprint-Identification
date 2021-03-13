from tkinter import *
import math
from VoiceClassification import *
import keras
pi = np.pi
directory_to_project = dir_path = os.path.dirname(os.path.realpath(__file__))
model_val_accuracy = 0.555
model_accuracy = .575

global names, label_list, label_list_button, model


def ChangeScreen():
    """
    Deletes UI and resets back to original frame (HomePage)
    """
    for widget in window.winfo_children():
        widget.destroy()
    HomePage(window)


def updateLabelList():
    """
    Organizes global variable list of people by adding both label and button lists
    """
    global label_list, label_list_button, names
    label_list = []
    label_list_button = []
    for name in names:
        name_item = name + "Label"
        label_list.append(name_item)
        button_item = name + "LButton"
        label_list_button.append(button_item)


def HighlightLabel(name, percent_chance_label, percent_chance):
    """
    Highlight the user that is talking
    :param name: String
        Desired name to highlight. (None to un-highlight all of them)
    """
    # if name == '':
    #     return
    if name == "None" or name == "":
        for label in label_list:
            label.config(bg="#F0F0F0")
        return
    index = names.index(name)
    for label in label_list:
        if label == label_list[index]:
            pass
        label.config(bg="#F0F0F0")
    label_list[index].config(bg="Yellow")
    percent_chance_label.config(text=f"Confidence: {math.floor(100 * percent_chance)}%")


def captureUserInput(userfield, name_frame, frame2):
    """
    Capture user input and calls record_sentence_UI to finish setting up the user
    :param userfield: Tkinter text box widget
        Used to get input
    :param name_frame: Tkinter Frame
        Frame of the names to add respective name
    :param frame2: Tkinter frame
        Frame of the user input to give instructions on how to continue recording
    """
    user_name = userfield.get()
    if user_name != "" and user_name not in names:
        names.append(user_name)
        updateLabelList()
        print_names(name_frame)
        record_sentence_UI(frame2, user_name)


def print_names(frame):
    """
    Update the Tkinter name frame to print all names with a delete option
    :param frame: Tkinter frame
        the name_frame frame so it can be updated
    """
    name_title = Label(frame, text="Speaking", anchor=CENTER, font="Helvetica 20 bold ")
    name_title.place(x=60, y=0)
    ypos = 50
    for i in range(len(label_list)):
        label_list[i] = Label(frame, text=names[i], anchor=CENTER, font="Helvetica 16 bold", height=0, width=10)
        label_list[i].place(x=0, y=ypos)
        label_list_button[i] = Button(frame, text="X", anchor=CENTER, font="Helvetica 10", command=lambda i=i: delete_user(names[i], frame))
        label_list_button[i].place(x=200, y=ypos)
        ypos += 30


def delete_user(name_item, frame):
    """
    Functionality of the delete user button. Deletes audio files, removes from name list, and updates UI
    :param name_item: String
        the name of the respective user to delete
    :param frame: Tkinter frame
        name_frame to update the tkinter frame.
    """
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


def continue_function(instructions, button, user_input):
    """
    Button that has multiple uses to make recording new data easy! (OK button)
    :param instructions: Tkinter label
        instructions1 as it needs to update text as the button is pressed
    :param button: Tkinter button
        continue_button to update text as the button is pressed
    :param user_input: String
        name to distinguish profiles
    """
    RECORD_SECONDS = 34
    global iteration
    if iteration == 1:
        instructions.config(text="Record Prompt")
        button.config(text="Start Recording")
    elif iteration == 2:
        create_recorded_data("sentence", RECORD_SECONDS)
        instructions.config(text="Stopped Recording")
        button.config(text="Ok")
        break_up_audio(["sentence"])
        export_recordings(user_input, ["sentence"])
    elif iteration == 3:
        instructions.destroy()
        button.destroy()
    iteration += 1


def record_sentence_UI(frame, user_input):
    """
    Helper function to record new data for new user
    :param frame: Tkinter frame
        frame2 as this frame needs to change
    :param user_input: String
        Users name to distinguish between users
    """
    global iteration
    iteration = 1

    instructions1 = Label(frame, text="Get ready to record audio input", anchor=CENTER, font="Helvetica 11")
    instructions1.place(x=5, y=110)

    continue_button = Button(frame, text="Ok", command=lambda: continue_function(instructions1, continue_button, user_input))
    continue_button.place(x=110, y=80)


def acc_label():
    """
    Returns the label for the accuracy so it can dynamically update when the frame is reloaded
    :return: String
        this string will be the text of the accuracy label
    """
    try:
        model
    except:
        return "Accuracy= N/A"
    accuracy = model.accuracy[-1]
    return f"Accuracy={round(accuracy, 3)}"


def train_model_UI(acc_label):
    """
    Trains the model and places it in global variable model
    :param acc_label: Tkinter Label
        accuracy label to change the accuracy after updating the mode
    """
    global model
    model = word_model(['sentence'])
    accuracy = model.accuracy[-1]
    acc_label.config(text=f"Accuracy={round(accuracy, 3)}")


def popup_error(text, flag=False):
    """
    Creates popup screen to display a message
    :param text: String
        Message on the popup window
    :param flag: Boolean
        if True, the message is an error and is red. if false, normal messag
    """
    # Initialize popup
    win = Toplevel()
    win.wm_title("Error")
    winx = 400
    winy = 170
    win.minsize(winx, winy)
    win.maxsize(winx, winy)

    # Title of the popup (if error or not)
    if flag:
        message = Label(win, text=text, font=('Ariel', 20), bg="red")
        message.pack(side=TOP, pady=10)
    else:
        message = Label(win, text=text, font=('Ariel', 20))
        message.pack(side=TOP, pady=10)

    # Create canvas
    canvas = Canvas(win, width=winx, height=winy)
    canvas.pack(side=LEFT)

    # Exit button to close the popup window
    exitpop = Button(win, text="Okay", command=win.destroy, height=2, width=12)
    exitpop.place(x=(winx / 2) - 55, y=winy - 60)


def stop_rec(action):
    """
    Multifunctional function to either return live or change live's value
    :param action: String
        Either STOP or CHECK to either stop the recording or to check if it should be stopped
    :return: Boolean
        Only returns when action = CHECK
    """
    global live
    if action == "STOP":
        live = False
    else:
        return live


def save_acc():
    f = open("tools\\model\\saved_model\\m_accuracy.txt", "w")
    accuracy = model.accuracy[-1]
    acc_str = str(round(accuracy, 3))
    f.write(acc_str)
    f.close()


def load_acc(acc_label):
    f = open("tools\\model\\saved_model\\m_accuracy.txt", "r")
    accuracy = f.read()
    acc_label.config(text=f"Accuracy={accuracy}")
    f.close()


def save_model():
    try:
        model
    except NameError:
        popup_error("Model Not Trained", True)
        return
    dir_model = "tools\\model\\saved_model"
    model.model.save(dir_model)
    save_acc()


def loadModel(acc_label):
    try:
        dir_model = "tools\\model\\saved_model"
        global model
        model = word_model(['sentence'], load=True, path=dir_model)
        load_acc(acc_label)
    except:
        popup_error("No Saved Model", True)



class HomePage:
    def record_live_setup_UI(self, recordButton, frame, nameframe):
        """
        Sets up liverecording by changing the button to stop and other functions that do not loop
        :param recordButton: Tkinter button
            To destroy and replace with a stop button
        :param frame: Tkinter frame
            Options frame to get access to build a stop button
        """
        global model, live
        try:
            model
        except NameError:
            popup_error("Model Not Trained", True)
            return

        recordButton.destroy()
        dir_record_img = directory_to_project + "\\tools\\images\\stop-button.png"
        # Photo for Record Button
        photorecord = PhotoImage(file=dir_record_img)
        photoimagerecord = photorecord.subsample(16, 16)
        panelrecord = Label(frame, image=photoimagerecord)
        panelrecord.photo = photoimagerecord

        live = True
        stopButton = Button(frame, image=photoimagerecord, relief="flat", border=1, bd=0, highlightthickness=0,
                         command=lambda: stop_rec("STOP"))
        stopButton.place(x=208, y=5)

        percent_chance_label = Label(nameframe, text="", font="Helvetica 18")
        percent_chance_label.place(x=15, y=350)

        self.record_live_UI(percent_chance_label)

    def record_live_UI(self, percent_chance_label):
        """
        Helper function that loops when recording starts and can be terminated by pressing the stop button
        """
        global model, window, live

        live = stop_rec("CHECK")
        if live:
            window.after(2000, lambda: self.record_live_UI(percent_chance_label))
        else:
            ChangeScreen()
            return

        # Change UI display. Delete microphone and add stop button

        # record for 2 sec
        guess, confidence = short_prediction(model, 1.5)
        print(f"{guess} {confidence}")
        # process results
        # highlight name
        HighlightLabel(guess, percent_chance_label, confidence)

    def __init__(self, master):
        """
        The initialization of the HomePage.
        :param master: Tkinter frame
            is window after the program starts.
        """
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
                         command=lambda: self.record_live_setup_UI(RecordButton, optionsframe, name_frame))
        RecordButton.place(x=208, y=5)

        name_frame = Frame(master, height=400, width=250, borderwidth="4", relief="groove")
        name_frame.place(x=0, y=0)

        print_names(name_frame)

        user_input_title = Label(frame2, text="Options", anchor=CENTER, font="Helvetica 20 bold")
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

        saveModelButton = Button(optionsframe, text="Save Model", command=lambda: save_model(), height=0, width=0, font="Helvetica 14 bold")
        saveModelButton.place(x=50, y=5)

        loadModelButton = Button(optionsframe, text="Load Model", command=lambda: loadModel(model_accuracy_label), height=0, width=0, font="Helvetica 14 bold")
        loadModelButton.place(x=50, y=50)

        model_accuracy_label = Label(frame1, text=acc_label(), anchor=CENTER, font="Helvetica 16 bold", height=2)
        model_accuracy_label.place(x=50, y=400)

        # Record new data
        # record live
        # train model - print accuracy


def start_UI():
    """
    Helper function to clean up main and set up the UI of tkinter
    """
    global window, names, label_list, label_list_button
    names = os.listdir("words\\sentence")
    updateLabelList()

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
