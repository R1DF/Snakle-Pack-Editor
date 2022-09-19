# Imports
import json
from datetime import  datetime
from tkinter import Tk, Canvas, Menu, Frame, Listbox, Label, Scrollbar, Button, Entry, Text, messagebox, filedialog
from program_data.prompts import WordAdder, WordEditor

# Horizontal Line function
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
        self.title("Pack Editor - Untitled")
        self.geometry("400x470")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.handle_exit)
        self.opened_window_parameters = {
            "add": False,
            "edit": False,
            "save": False
        }
        self.word_adder = None
        self.word_editor = None
        self.word_amount = 0
        self.title_length = 0
        self.description_length = 0

        # Making menu bar
        self.make_menu()
        self.make_widgets()

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
        self.entries_intro_label = Label(self.entries_frame, text=f"Words ({self.word_amount}/500):")
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

        self.save_button = Button(self.buttons_frame, text="Save", width=25, command=self.validate_save)
        self.save_button.pack(pady=5)

        self.open_button = Button(self.buttons_frame, text="Open", width=25, command=self.open_file)
        self.open_button.pack(pady=5)

        # Metadata: Author
        self.author_frame = Frame(self.bottom_widgets_frame)
        self.author_frame.pack()

        self.author_label = Label(self.author_frame, text="Author:")
        self.author_label.pack()

        self.author_entry = Entry(self.author_frame, width=20)
        self.author_entry.pack()

        # Metadata: Title
        self.title_frame = Frame(self.bottom_widgets_frame)
        self.title_frame.pack()

        self.title_label = Label(self.title_frame, text="Title:")
        self.title_label.pack()

        self.title_entry = Entry(self.title_frame, width=52)
        self.title_entry.pack()

        # Metadata: Description
        self.description_frame = Frame(self.bottom_widgets_frame)
        self.description_frame.pack()

        self.description_label = Label(self.description_frame, text="Description:")
        self.description_label.pack()

        self.description_entry = Text(self.description_frame, width=53, height=3)
        self.description_entry.pack()

    def make_menu(self):
        self.master_menu = Menu(self)

        # Commands meny
        self.commands_menu = Menu(self.master_menu, tearoff=0)
        self.commands_menu.add_command(label="Add", command=self.make_word_adder)
        self.commands_menu.add_command(label="Delete", command=self.delete_selected)
        self.commands_menu.add_command(label="Edit", command=self.make_word_editor)
        self.master_menu.add_cascade(label="Commands", menu=self.commands_menu)

        # Pack menu
        self.pack_menu = Menu(self.master_menu, tearoff=0)
        self.pack_menu.add_command(label="Open", command=self.open_file)
        self.pack_menu.add_command(label="Save", command=self.validate_save)
        self.pack_menu.add_separator()
        self.pack_menu.add_command(label="Reset", command=self.reset)
        self.pack_menu.add_command(label="Close")
        self.pack_menu.add_separator()
        self.pack_menu.add_command(label="Deploy")
        self.master_menu.add_cascade(label="Pack", menu=self.pack_menu)

        # About menu
        self.about_menu = Menu(self.master_menu, tearoff=0)
        self.about_menu.add_command(label="About Snakle Pack Editor")
        self.about_menu.add_command(label="Help")
        self.about_menu.add_separator()
        self.about_menu.add_command(label="Open Repository")
        self.about_menu.add_command(label="Version", accelerator="1.0.0")
        self.master_menu.add_cascade(label="About", menu=self.about_menu)

        # Adding the menu to self
        self.config(menu=self.master_menu)

    def make_word_adder(self):
        if not self.opened_window_parameters["add"]:
            self.font_adder = WordAdder(self)

    def make_word_editor(self):
        if self.entries_listbox.curselection() == ():
            messagebox.showerror("Error", "Please select a word.")
            return

        if not self.opened_window_parameters["edit"]:
            self.font_editor = WordEditor(self, self.entries_listbox.get(self.entries_listbox.curselection()), self.entries_listbox.curselection()[0])

    def delete_selected(self):
        if self.entries_listbox.curselection() == ():
            messagebox.showerror("Error", "Please select a word to delete.")
        else:
            self.word_amount -= 1
            self.entries_listbox.delete(self.entries_listbox.curselection())
            self.update_word_amount()

    def update_word_amount(self):
        self.entries_intro_label.config(text=f"Words ({self.word_amount}/500):")

    def validate_save(self):
        # Getting variables
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        description = self.description_entry.get("1.0", "end").strip()

        # Checking lengths
        if self.word_amount < 10:
            messagebox.showerror("Unable to save", "Please enter at least 10 words.")
            return
        elif len(title) == 0:
            messagebox.showerror("Unable to save", "Please enter a title.")
            return
        elif len(author) == 0:
            messagebox.showerror("Unable to save", "Please enter the author name.")
        elif len(title) > 30:
            messagebox.showerror("Unable to save", "Your title is way too long. Please enter one that is less than 30 characters.")
            return
        elif len(author) > 20:
            messagebox.showerror("Unable to save", "Please enter a shorter author name (less than 20 characters).")
            return
        elif len(description.strip()) == 0:
            messagebox.showerror("Unable to save", "Please enter a description.")
            return
        elif len(description.strip()) > 100:
            messagebox.showerror("Unable to save", "Please enter a shorter description (less than 100 characters).")
            return

        # If the above tests pass, begin save process
        self.save_to_file()

    def validate_file(self, file_data):
        # Checking if the needed keys exist
        for key in ["title", "description", "creator", "dateCreated", "words"]:
            if key not in file_data:
                return False
        # Otherwise... (this will also allow modified files that have extra keys)
        return True

    def open_file(self):
        # Querying the file location
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=(("JSON file", "*.json"),))
        file_data = json.load(open(file_path, "r"))

        # Making sure the operation wasn't cancelled
        if file_path == "":
            return

        # Validating the file
        if self.validate_file(file_data):
            title = file_data["title"]
            author = file_data["creator"]
            description = file_data["description"]
            words = file_data["words"]

            # Adding author
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

            # Updating word amount
            self.word_amount = len(words)
            self.update_word_amount()

        else:
            messagebox.showerror("Invalid file", "The file is invalid. Are you sure it's a pack?")

    def save_to_file(self):
        # Getting dictionary data
        data = {
            "title": self.title_entry.get().strip(),
            "description": self.description_entry.get("1.0", "end").strip(),
            "creator": self.author_entry.get(),
            "dateCreated": self.format_date(),
            "words": self.entries_listbox.get(0, "end")
        }

        # Getting file path
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=(
            ("JSON file", "*.json"),
        ))

        if file_path == "":
            return  # operation cancelled

        # Dumping + notifying
        json.dump(data, open(file_path, "w"))
        messagebox.showinfo("Success", "Pack saved successfully.")

    def reset(self):
        pass

    def handle_exit(self):
        self.quit()

# Creating application
app = App()
app.mainloop()
