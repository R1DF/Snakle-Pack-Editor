# Prompt Imports
import os
import webbrowser
import json
from tkinter import Toplevel, Frame, Label, Entry, Button, ttk, StringVar, messagebox, filedialog, PhotoImage, Text

# Making the adder window
class WordAdder(Toplevel):
    def __init__(self, master):
        # Initialization
        Toplevel.__init__(self, master)
        self.master = master
        self.title("Add")
        self.master.opened_window_parameters["add"] = True
        self.resizable(False, False)

        # building widgets
        self.word_intro_frame = Frame(self)
        self.word_intro_frame.pack()

        self.word_name_label = Label(self.word_intro_frame, text="Enter word:")
        self.word_name_label.grid(row=0, column=0)

        self.word_name_entry = Entry(self.word_intro_frame, width=30)
        self.word_name_entry.grid(row=0, column=1)

        self.add_word_button = Button(self, text="Add", command=self.add_word)
        self.add_word_button.pack()

        # Adding protocol to modify when
        self.protocol("WM_DELETE_WINDOW", self.handle_exit)

    def add_word(self):
        if self.word_name_entry.get().strip() == "":
            messagebox.showerror("Empty input", "Please enter a word.")
        elif len(self.word_name_entry.get().strip().lower()) != 5:
            messagebox.showerror("Invalid word", "The entered word must be 5 letters long.")
        elif self.word_name_entry.get().strip().upper() in self.master.entries_listbox.get(0, "end"):
            messagebox.showerror("Already exists", "The entered word has already been entered.")
        else:
            self.master.word_amount += 1
            self.master.entries_listbox.insert("end", self.word_name_entry.get().strip().upper())
            self.master.update_word_amount()
            self.master.switch_updated_status(False)
            self.handle_exit()

    def handle_exit(self):
        self.master.opened_window_parameters["add"] = False
        self.master.word_adder = None
        self.destroy()

# Making the editor window
class WordEditor(Toplevel):
    def __init__(self, master, word_to_edit, word_index):
        # Initialization
        Toplevel.__init__(self, master)
        self.master = master
        self.title("Edit")
        self.master.opened_window_parameters["edit"] = True
        self.resizable(False, False)
        self.word_to_edit = word_to_edit
        self.word_index = word_index

        # Building widgets
        self.word_intro_frame = Frame(self)
        self.word_intro_frame.pack()

        self.word_name_label = Label(self.word_intro_frame, text="Enter word:")
        self.word_name_label.grid(row=0, column=0)

        self.word_name_entry = Entry(self.word_intro_frame, width=30)
        self.word_name_entry.grid(row=0, column=1)

        self.edit_word_button = Button(self, text="Save", command=self.edit_word)
        self.edit_word_button.pack()

        # Adding protocol to modify when exited
        self.protocol("WM_DELETE_WINDOW", self.handle_exit)

        # Showing edited word
        self.word_name_entry.insert(0, self.word_to_edit.title())

    def edit_word(self):
        if self.word_name_entry.get().strip() == "":
            messagebox.showerror("Empty input", "Please enter a word.")
        elif len(self.word_name_entry.get().strip().lower()) != 5:
            messagebox.showerror("Invalid word", "The entered word must be 5 letters long.")
        elif (self.word_name_entry.get().strip().upper() in self.master.entries_listbox.get(0, "end")) and (self.word_name_entry.get().strip().upper() != self.word_to_edit):
            messagebox.showerror("Already exists", "The entered word has already been entered.")
        else:
            self.master.entries_listbox.delete(self.word_index)
            self.master.entries_listbox.insert(self.word_index, self.word_name_entry.get().strip().upper())
            self.master.switch_updated_status(False)
            self.handle_exit()

    def handle_exit(self):
        self.master.opened_window_parameters["edit"] = False
        self.master.word_editor = None
        self.destroy()

# Making the Info window
class InfoWindow(Toplevel):
    def __init__(self, master):
        # Initialization
        self.master = master
        Toplevel.__init__(self, self.master)
        self.title("About Snakle Pack Editor")
        self.geometry("330x130")
        self.master.opened_window_parameters["info"] = True

        # Image
        self.image = PhotoImage(file=os.getcwd()+ "\\program_data\\icon.png")
        self.image_label = Label(self, image=self.image)
        self.image_label.pack()

        # Labels
        self.labels = []
        self.labels.append(Label(self, text="Snakle Pack Editor"))
        self.labels.append(Label(self, text=f"Version {self.master.version}"))
        self.labels.append(Label(self, text=f"Coded by R1DF with Python, Tkinter, and JSON."))

        for label in self.labels:
            label.pack()

        # Buttons
        self.buttons_frame = Frame(self)
        self.buttons_frame.pack()

        self.get_snakle_button = Button(self.buttons_frame, text="Get Legacy Snakle", command=lambda: webbrowser.open("https://github.com/R1DF/Legacy-Snakle"))
        self.get_snakle_button.grid(row=0, column=0)

        self.open_repository_button = Button(self.buttons_frame, text="Open Repository", command=lambda: webbrowser.open("https://github.com/R1DF/Snakle-Pack-Editor"))
        self.open_repository_button.grid(row=0, column=1)

        # Adding protocol to modify when
        self.protocol("WM_DELETE_WINDOW", self.handle_exit)

    def handle_exit(self):
        self.master.opened_window_parameters["info"] = False
        self.master.info_window = None
        self.destroy()

# Making the Deploy window
class DeployWindow(Toplevel):
    def __init__(self, master):
        # Initialization
        self.master = master
        Toplevel.__init__(self, self.master)
        self.title("Deploy")
        self.geometry("630x230")
        self.master.opened_window_parameters["deploy"] = True
        self.resizable(False, False)
        self.has_game_folder_set = False

        # Adding protocol to modify when exited
        self.protocol("WM_DELETE_WINDOW", self.handle_exit)

        # Widgets
        self.warning_label = Label(self, text="Please make sure the information below is correct!", fg="red")
        self.warning_label.pack()

        self.author_label = Label(self, text=f"Author: {self.master.author_entry.get()}")
        self.author_label.pack()

        self.title_label = Label(self, text=f"Title: {self.master.title_entry.get()}")
        self.title_label.pack()

        self.description_label = Label(self, text=f"Description:\n{self.format_description(self.master.description_entry.get(1.0, 'end').strip())}")
        self.description_label.pack()

        self.file_name_frame = Frame(self)
        self.file_name_frame.pack()

        self.file_name_label = Label(self.file_name_frame, text="File name: ")
        self.file_name_label.grid(row=0, column=0)

        self.file_name_entry = Entry(self.file_name_frame, width=30)
        self.file_name_entry.grid(row=0, column=1)

        self.directory_frame = Frame(self)
        self.directory_frame.pack()

        self.game_directory_label = Label(self.directory_frame, text="Game Folder: ")
        self.game_directory_label.grid(row=0, column=0)

        self.game_directory_entry = Entry(self.directory_frame, width=70)
        self.game_directory_entry.grid(row=0, column=1)

        self.set_directory_button = Button(self.directory_frame, text="Set Game Folder", command=self.set_directory)
        self.set_directory_button.grid(row=0, column=2)

        # Managing game folder entry
        self.game_directory_entry.insert(0, "No game folder set.")
        self.game_directory_entry.config(state="disabled")

        # Deploy area
        self.deploy_label = Label(self, text="After configuring everything, hit the button below:", fg="blue")
        self.deploy_label.pack()

        self.deploy_button = Button(self, text="Deploy", command=self.deploy)
        self.deploy_button.pack()

    def deploy(self):
        # Entry validation
        if not self.has_game_folder_set:
            messagebox.showerror("Unable to deploy", "Please enter a directory.")
            return

        if self.file_name_entry.get().strip() == "":
            messagebox.showerror("Unable to deploy", "Please enter a name for the file.")
            return

        elif not os.path.exists(f"{self.game_directory_entry.get()}\\packs\\"):  # If the path is invalid
            messagebox.showerror("Invalid folder", "The folder either doesn't contain the game or the game is damaged.")
            return

        if os.path.exists(f"{self.game_directory_entry.get()}\\packs\\{self.file_name_entry.get()}.json"): # Overwrite prompt
            if not messagebox.askyesno("Pack already exists", "A pack in the same folder and with the same name already exists. Replace it?"):
                return


        # Finding path
        directory = self.game_directory_entry.get()
        json.dump({
            "title": self.master.title_entry.get().strip(),
            "description": self.master.description_entry.get(1.0, "end").strip(),
            "creator": self.master.author_entry.get().strip(),
            "dateCreated": self.master.format_date(),
            "words": self.master.entries_listbox.get(0, "end")
        }, open(f"{directory}\\packs\\{self.file_name_entry.get()}.json", "w"))
        messagebox.showinfo("Success", "Deployed to the folder.")
        self.handle_exit()

    def set_directory(self):
        # Getting folder
        directory = filedialog.askdirectory()

        # Checking to see if a folder was selected
        if directory == "":
            return

        # Changing directory entry
        self.has_game_folder_set = True
        self.game_directory_entry.config(state="normal")
        self.game_directory_entry.delete(0, "end")
        self.game_directory_entry.insert(0, directory)
        self.game_directory_entry.config(state="disabled")

    def format_description(self, description):
        formatted = description[0]
        for i in range(1, len(description)):
            if i % 80 == 0:
                formatted += f"{'-' if description[i] != ' ' else ''}\n"

                # Spaces don't get extra treatment
                if description[i] == " ":
                    continue

            formatted += description[i]
        return formatted

    def handle_exit(self):
        self.master.opened_window_parameters["deploy"] = False
        self.destroy()


# Helper window
class HelpWindow(Toplevel):
    def __init__(self, master):
        # Initialization
        self.master = master
        Toplevel.__init__(self, self.master)
        self.title("Help")
        self.geometry("700x310")
        self.master.opened_window_parameters["help"] = True
        self.resizable(False, False)
        self.has_game_folder_set = False

        # List of questions
        self.questions = [
            "What is Snakle Pack Editor?",
            "What is Snakle?",
            "How to use this program?",
            "Should I save or deploy?",
            "How do I rename my pack?",
            "I don't see my question here."
        ]

        self.answers = json.load(open(os.getcwd() + "\\program_data\\answers.json", "r")) # Must add exception checking

        # Adding protocol to modify when exited
        self.protocol("WM_DELETE_WINDOW", self.handle_exit)

        # Widgets + StrVar
        self.introduction_label = Label(self, text="Please select a question that you would like an answer to:")
        self.introduction_label.pack()

        self.question_stringvar = StringVar()

        self.question_optionmenu = ttk.OptionMenu(self, self.question_stringvar, "Select an option...", *self.questions)  # better styling
        self.question_optionmenu.pack()

        self.answer_field = Text(self, height=11, font="Calibri 13")
        self.answer_field.pack()
        self.answer_field.insert("end", "Use the drop-down menu above to select a question.")
        self.answer_field.config(state="disabled")

        # Buttons
        self.buttons_frame = Frame(self)
        self.buttons_frame.pack()

        self.repository_button = Button(self.buttons_frame, text="Open Repository", command=lambda: webbrowser.open_new_tab("https://github.com/R1DF/Snakle-Pack-Editor"))
        self.repository_button.grid(row=0, column=0)

        self.links_page_button = Button(self.buttons_frame, text="Creator's Links", command=lambda: webbrowser.open_new_tab("https://r1df.github.io/links.html"))
        self.links_page_button.grid(row=0, column=1)

        # Tracing
        self.question_stringvar.trace_add("write", lambda x, y, z: self.trace_select())

    def trace_select(self):
        index_of_answer = self.questions.index(self.question_stringvar.get()) + 1
        self.answer_field.config(state="normal")
        self.answer_field.delete(1.0, "end")

        for entry in self.answers[str(index_of_answer)]:
            self.answer_field.insert("end", entry)

        self.answer_field.config(state="disabled")


    def handle_exit(self):
        self.master.opened_window_parameters["help"] = False
        self.destroy()

