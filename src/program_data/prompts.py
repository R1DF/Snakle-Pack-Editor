# Prompt Imports
from tkinter import Toplevel, Frame, Label, Entry, Button, messagebox

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

        # building widgets
        self.word_intro_frame = Frame(self)
        self.word_intro_frame.pack()

        self.word_name_label = Label(self.word_intro_frame, text="Enter word:")
        self.word_name_label.grid(row=0, column=0)

        self.word_name_entry = Entry(self.word_intro_frame, width=30)
        self.word_name_entry.grid(row=0, column=1)

        self.edit_word_button = Button(self, text="Save", command=self.edit_word)
        self.edit_word_button.pack()

        # Adding protocol to modify when
        self.protocol("WM_DELETE_WINDOW", self.handle_exit)

        # Showing edited word
        self.word_name_entry.insert(0, self.word_to_edit.title())

    def edit_word(self):
        if self.word_name_entry.get().strip() == "":
            messagebox.showerror("Empty input", "Please enter a word.")
        elif len(self.word_name_entry.get().strip().lower()) != 5:
            messagebox.showerror("Invalid word", "The entered word must be 5 letters long.")
        elif (self.word_name_entry.get().strip().upper() in self.master.entries_listbox.get(0, "end")) and (self.self.word_name_entry.get().strip().upper() != self.word_to_edit):
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
