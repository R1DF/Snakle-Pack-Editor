# Imports
import json
import os
import webbrowser
from datetime import  datetime
from tkinter import Tk, Canvas, Menu, Frame, Listbox, Label, Scrollbar, Button, Entry, Text, StringVar, PhotoImage, messagebox, filedialog
from program_data.prompts import WordAdder, WordEditor, InfoWindow, DeployWindow, HelpWindow

# Horizontal Line class
class HorizontalLine:
    def __init__(self, master):
        # Initialization
        self.master = master

        # Canvas creation
        self.canvas = Canvas(self.master, height=5, width=400)
        self.canvas.pack()

        # Making the line
        self.canvas.create_line(0, 3, 400, 3)

# Application
class App(Tk):
    def __init__(self):
        # Initialization
        super().__init__()
        self.title("Snakle Pack Editor - Untitled")
        self.pack_title = None
        self.geometry("400x470")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.handle_exit)
        self.opened_window_parameters = {
            "add": False,
            "edit": False,
            "save": False,
            "info": False,
            "deploy": False,
            "help": False
        }
        self.word_adder = None
        self.word_editor = None
        self.info_window = None
        self.help_window = None
        self.word_amount = 0
        self.title_length = 0
        self.description_length = 0
        self.up_to_date = True
        self.version = "v1.0.0"
        self.variables_since_last_save = {
            "author": "",
            "title": ""
        }
        self.valid_trace_origin = True

        # Making menu bar
        self.make_menu()
        self.make_widgets()

        # Tracing
        self.author_stringvar.trace_add("write", lambda x, y, z: self.trace_entry())
        self.title_stringvar.trace_add("write", lambda x, y, z: self.trace_entry())

        # Binding
        self.bind("<Control-n>", lambda x: self.make_word_adder())
        self.bind("<Delete>", lambda x: self.delete_selected())
        self.bind("<Control-e>", lambda x: self.make_word_editor())
        self.bind("<Control-o>", lambda x: self.open_file())
        self.bind("<Control-s>", lambda x: self.query_save(True))

        # Icon
        self.iconphoto(True, PhotoImage(file=os.getcwd() + "\\program_data\\icon.png"))

    def format_date(self):
        date = datetime.now()
        day = str(date.day) if date.day > 9 else f"0{date.day}"
        month = str(date.month) if date.month > 9 else f"0{date.month}"
        year = str(date.year)[-2:]
        return f"{day}.{month}.{year}"

    def make_widgets(self):
        # Introduction
        self.introduction_label = Label(self, text="Snakle Pack Editor")
        self.introduction_label.pack()

        self.divider_1 = HorizontalLine(self)

        self.top_widgets_frame = Frame(self)
        self.top_widgets_frame.pack()

        self.bottom_widgets_frame = Frame(self)
        self.bottom_widgets_frame.pack()

        self.divider_2 = HorizontalLine(self.bottom_widgets_frame)

        # Frame system
        self.entries_frame = Frame(self.top_widgets_frame)
        self.entries_frame.grid(row=0, column=0)

        self.buttons_frame = Frame(self.top_widgets_frame)
        self.buttons_frame.grid(row=0, column=1)

        # Entries listbox frame
        self.entries_intro_label = Label(self.entries_frame, text=f"Words: {self.word_amount}")
        self.entries_intro_label.pack()

        self.listbox_area_entry = Frame(self.entries_frame)  # Due to the scrollbar existing I have to do this
        self.listbox_area_entry.pack()

        self.entries_listbox = Listbox(self.listbox_area_entry, width=30, height=15)
        self.entries_listbox.pack(side="left")

        self.entries_listbox_scrollbar = Scrollbar(self.listbox_area_entry)
        self.entries_listbox_scrollbar.pack(side="right", fill="both")

        self.entries_listbox.config(yscrollcommand=self.entries_listbox_scrollbar.set)
        self.entries_listbox_scrollbar.config(command=self.entries_listbox.yview)

        # Control panel
        self.control_panel_introduction_label = Label(self.buttons_frame, text="Commands:")
        self.control_panel_introduction_label.pack(pady=5)

        self.add_button = Button(self.buttons_frame, text="Add", width=25, command=self.make_word_adder)
        self.add_button.pack(pady=5)

        self.delete_button = Button(self.buttons_frame, text="Delete", width=25, command=self.delete_selected)
        self.delete_button.pack(pady=5)

        self.edit_button = Button(self.buttons_frame, text="Edit", width=25, command=self.make_word_editor)
        self.edit_button.pack(pady=5)

        self.save_button = Button(self.buttons_frame, text="Save", width=25, command=lambda: self.query_save(True))
        self.save_button.pack(pady=5)

        self.open_button = Button(self.buttons_frame, text="Open", width=25, command=self.open_file)
        self.open_button.pack(pady=5)

        # Metadata: StringVars
        self.author_stringvar = StringVar()
        self.title_stringvar = StringVar()
        # No Text StringVar sadly

        # Metadata: Author
        self.author_frame = Frame(self.bottom_widgets_frame)
        self.author_frame.pack()

        self.author_label = Label(self.author_frame, text="Author:")
        self.author_label.pack()

        self.author_entry = Entry(self.author_frame, width=20, textvariable=self.author_stringvar)
        self.author_entry.pack()

        # Metadata: Title
        self.title_frame = Frame(self.bottom_widgets_frame)
        self.title_frame.pack()

        self.title_label = Label(self.title_frame, text="Title:")
        self.title_label.pack()

        self.title_entry = Entry(self.title_frame, width=52, textvariable=self.title_stringvar)
        self.title_entry.pack()

        # Metadata: Description
        self.description_frame = Frame(self.bottom_widgets_frame)
        self.description_frame.pack()

        self.description_label = Label(self.description_frame, text="Description:")
        self.description_label.pack()

        self.description_entry = Text(self.description_frame, width=53, height=3, font="Arial 9")
        self.description_entry.pack()

    def make_menu(self):
        self.master_menu = Menu(self)

        # Commands meny
        self.commands_menu = Menu(self.master_menu, tearoff=0)
        self.commands_menu.add_command(label="Add", command=self.make_word_adder, accelerator="Ctrl+N")
        self.commands_menu.add_command(label="Delete", command=self.delete_selected, accelerator="Delete")
        self.commands_menu.add_command(label="Edit", command=self.make_word_editor, accelerator="Ctrl+E")
        self.master_menu.add_cascade(label="Commands", menu=self.commands_menu)

        # Pack menu
        self.pack_menu = Menu(self.master_menu, tearoff=0)
        self.pack_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.pack_menu.add_command(label="Save", command=self.query_save, accelerator="Ctrl+S")
        self.pack_menu.add_separator()
        self.pack_menu.add_command(label="Reset", command=self.reset)
        self.pack_menu.add_separator()
        self.pack_menu.add_command(label="Deploy", command=self.deploy)
        self.master_menu.add_cascade(label="Pack", menu=self.pack_menu)

        # About menu
        self.about_menu = Menu(self.master_menu, tearoff=0)
        self.about_menu.add_command(label="About Snakle Pack Editor", command=self.make_info_window)
        self.about_menu.add_command(label="Help", command=self.make_help_window)
        self.about_menu.add_separator()
        self.about_menu.add_command(label="Open Repository", command=lambda: webbrowser.open_new_tab("https://github.com/R1DF/Snakle-Pack-Editor"))
        self.about_menu.add_command(label="Version", accelerator=self.version)
        self.master_menu.add_cascade(label="About", menu=self.about_menu)

        # Adding the menu to self
        self.config(menu=self.master_menu)

    def trace_entry(self):  # valid_trace_origin used so that open file can't trigger it
        if not self.valid_trace_origin:
            return

        if self.author_stringvar.get() != self.variables_since_last_save["author"] or self.title_stringvar.get() != self.variables_since_last_save["author"]:
            self.switch_updated_status(False)

    def make_word_adder(self):
        if not self.opened_window_parameters["add"]:
            self.font_adder = WordAdder(self)

    def make_word_editor(self):
        if self.entries_listbox.curselection() == ():
            messagebox.showerror("Error", "Please select a word.")
            return

        if not self.opened_window_parameters["edit"]:
            self.font_editor = WordEditor(self, self.entries_listbox.get(self.entries_listbox.curselection()), self.entries_listbox.curselection()[0])

    def make_info_window(self):
        if not self.opened_window_parameters["info"]:
            self.info_window = InfoWindow(self)

    def make_help_window(self):
        if not self.opened_window_parameters["help"]:
            self.help_window = HelpWindow(self)

    def delete_selected(self):
        if self.entries_listbox.curselection() == ():
            messagebox.showerror("Error", "Please select a word to delete.")
        else:
            self.word_amount -= 1
            self.entries_listbox.delete(self.entries_listbox.curselection())
            self.update_word_amount()
            self.switch_updated_status(False)

    def update_word_amount(self):
        self.entries_intro_label.config(text=f"Words: {self.word_amount}")

    def can_save(self):
        # Getting variables
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        description = self.description_entry.get(1.0, "end").strip()

        # Tests
        if self.word_amount < 10:
            return False, "Please enter at least 10 words."
        elif len(title) == 0:
            return False, "Please enter a title."
        elif len(author) == 0:
            return False, "Please enter the author name."
        elif len(title) > 30:
            return False, "Your title is way too long. Please enter one that is less than 30 characters."
        elif len(author) > 20:
            return False, "Please enter a shorter author name (less than 20 characters)."
        elif len(description.strip()) == 0:
            return False, "Please enter a description."
        elif len(description.strip()) > 100:
            return False, "Please enter a shorter description (less than 100 characters)."

        # If tests were passed
        return True, None

    def query_save(self, check=False):
        # Checking
        if check:
            test = self.can_save()
            if not test[0]:
                messagebox.showerror("Unable to save", test[1])
                return

        # If tests pass, begin save process
        self.save_to_file()

    def validate_file(self, file_data):
        # Checking if the needed keys exist
        for key in ["title", "description", "creator", "dateCreated", "words"]:
            if key not in file_data:
                return False
        # Otherwise... (this will also allow modified files that have extra keys)
        return True

    def open_file(self):
        # Checking if the file is updated
        if (not self.up_to_date) and self.can_save()[0]:
            if messagebox.askyesno("Save?", "It appears you haven't saved your latest changes! Would you like to save them now?"):
                self.query_save(True)

        # Querying the file location
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=(("JSON file", "*.json"),))

        # Making sure the operation wasn't cancelled and the file is decodable
        if file_path == "":
            return

        try:
            file_data = json.load(open(file_path, "r"))
        except UnicodeDecodeError:
            messagebox.showerror("Invalid file", "This file is unreadable.")
            return

        # Validating the file
        if self.validate_file(file_data):
            try:
                author = file_data["creator"]
                title = file_data["title"]
                description = file_data["description"]
                words = file_data["words"]

                # Updating title
                self.pack_title = title
                self.title(f"Snakle Pack Editor - {self.pack_title}")

                # Adding author + briefly blocking trace
                self.valid_trace_origin = False
                self.author_entry.delete(0, "end")
                self.author_entry.insert(0, author)

                # Adding title
                self.title_entry.delete(0, "end")
                self.title_entry.insert(0, title)

                # Adding description
                self.description_entry.delete(1.0, "end")
                self.description_entry.insert("end", description)

                # Getting words
                self.entries_listbox.delete(0, "end")
                for word in words:
                    self.entries_listbox.insert("end", word)

                # Updating
                self.word_amount = len(words)
                self.update_word_amount()
                self.variables_since_last_save = {"author": author, "title": title}
                self.valid_trace_origin = True

            except json.JSONDecodeError:
                messagebox.showerror("Invalid file", "This file is invalid. Are you sure it's a pack?")

        else:
            messagebox.showerror("Invalid file", "The file is invalid. Are you sure it's a pack?")

    def save_to_file(self):
        # To not call .get() twice
        author = self.author_entry.get()
        title = self.title_entry.get().strip()
        description = self.description_entry.get(1.0, "end").strip()

        # Getting dictionary data
        data = {
            "title": title,
            "description": description,
            "creator": author,
            "dateCreated": self.format_date(),
            "words": self.entries_listbox.get(0, "end")
        }

        # Getting file path
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=(
            ("JSON file", "*.json"),
        ))

        if file_path == "":
            return  # operation cancelled

        # Configuring
        self.variables_since_last_save = {"author": author, "title": title}

        # Dumping + updating + notifying
        json.dump(data, open(file_path, "w"))
        self.pack_title = title
        self.switch_updated_status(True)
        messagebox.showinfo("Success", "Pack saved successfully.")

    def reset(self, already_confirm=False):
        # Checking if everything is already empty
        creator = self.author_entry.get().strip()
        title = self.title_entry.get().strip()
        description = self.description_entry.get(1.0, "end").strip()
        if self.entries_listbox.get(0, "end") == () and creator == title == description == "" and self.pack_title is None:
            messagebox.showerror("Unable to reset", "There's already nothing!")
            return

        # Confirmation
        if not messagebox.askyesno("Reset?", "Clear all pack contents from the program?"):
            return

        # Changing title + blocking trace
        self.valid_trace_origin = False
        self.pack_title = None
        self.title("Snakle Pack Editor - Untitled")

        # Removing all words
        self.word_amount = 0
        self.entries_listbox.delete(0, "end")
        self.update_word_amount()

        # Removing metadata + updating
        self.author_entry.delete(0, "end")
        self.title_entry.delete(0, "end")
        self.description_entry.delete(1.0, "end")
        self.switch_updated_status(True)
        self.valid_trace_origin = True

    def deploy(self):
        # Pass checking
        test = self.can_save()

        if not test[0]:
            messagebox.showerror("Unable to deploy", test[1])
            return

        if not self.up_to_date:
            messagebox.showerror("Unable to deploy", "Please save the pack before deploying!")
            return

        # Deployment
        if not self.opened_window_parameters["deploy"]:
            self.deploy_window = DeployWindow(self)


    def switch_updated_status(self, is_up_to_date, keep_asterisk=True):
        if is_up_to_date:
            self.up_to_date = True
            self.title(f"Snakle Pack Editor - {self.pack_title if self.pack_title is not None else 'Untitled'}")
        else:
            self.up_to_date = False
            self.title(
                f"Snakle Pack Editor - {self.pack_title if self.pack_title is not None else 'Untitled'}{'*' if keep_asterisk else ''}")

    def toggle_updated_status(self, keep_asterisk=True):
        if self.up_to_date:
            self.switch_updated_status(False, keep_asterisk)
        else:
            self.switch_updated_status(True)

    def handle_exit(self):
        if (not self.up_to_date) and self.can_save()[0]:
            if messagebox.askyesno("Quit?", "You haven't saved your changes. Do you want to save them before quitting?"):
                self.query_save(True)
        self.quit()


# Creating application
app = App()
app.mainloop()
