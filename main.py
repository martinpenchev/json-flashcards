import json

from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog

from backend import Flashcards

class Application:

    def __init__(self, master):
        master.title('Flashcards')
        master.resizable(False, False)
        master.configure(background = '#e1e1e1')

        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#e1e1e1')
        self.style.configure('TNotebook', background = '#e1e1e1')
        self.style.configure('TNotebook.Tab', background = '#e1e1e1')
        self.style.configure('TButton', background = '#9a9a9a')
        self.style.configure('TLabel', background = "#e1e1e1", font = ('Arial', 11))
        self.style.configure('Header.TLabel', font = ('Arial', 18, 'bold'))
        self.style.configure('Title.TLabel', font = ('Arial', 14, 'bold'))

        master.option_add('*tearOff', False)
        menu = Menu(master)
        master.config(menu=menu)

        # File menu
        file_menu = Menu(menu)
        menu.add_cascade(label='File', menu=file_menu, underline=0)
        file_menu.add_command(label="Import", command=self.import_file, compound="left", accelerator="Ctrl+I", underline=0)
        file_menu.add_command(label="Export", command=self.export, compound="left", accelerator="Ctrl+S", underline=0)
        file_menu.add_separator()
        file_menu.add_command(label="Close", command=self.close_file, compound="left", accelerator="Ctrl+Q", underline=0)

        # Edit menu
        edit_menu = Menu(menu)
        menu.add_cascade(label='Edit', menu=edit_menu, underline=0)

        # Database menu
        db_menu = Menu(menu)
        menu.add_cascade(label="Database", menu=db_menu, underline=0)
        db_menu.add_command(label="Open", command=self.load_db, compound="left", accelerator="Ctrl+O")
        db_menu.add_command(label="Add records", command=self.add_from_json, compound="left")
        db_menu.add_command(label="Delete all records", command=self.delete_all, compound="left")

        # HEADER FRAME
        self.frame_header = ttk.Frame(master)
        self.frame_header.grid(row = 0, column = 0)
        ttk.Label(self.frame_header, text = "FLASHCARDS", style = 'Header.TLabel').grid(row = 0, column = 0, pady = 10)

        # MAIN AREA FRAME
        self.frame_main = ttk.Frame(master)
        self.frame_main.grid(row = 1, column = 0)

        # ADD CARD FRAME
        ttk.Label(self.frame_main, text="ADD NEW CARD", style='Title.TLabel').grid(row=0, column=1)

        self.frame_add_card = ttk.Frame(self.frame_main)
        self.frame_add_card.grid(row = 1, column = 1)

        ttk.Label(self.frame_add_card, text = "Front side").grid(row = 0, column = 0, columnspan = 2, pady = 5)
        ttk.Label(self.frame_add_card, text = "Back side").grid(row = 2, column = 0, columnspan = 2, pady = 5)
    
        self.text_front = Text(self.frame_add_card, width = 40, height = 4, font = ('Arial', 10))
        self.text_back = Text(self.frame_add_card, width = 40, height = 4, font = ('Arial', 10))

        self.text_front.grid(row = 1, column = 0, columnspan = 2, pady=5, padx=5)
        self.text_back.grid(row = 3, column = 0, columnspan = 2, pady=5, padx=5)

        # A tuple containing text editor tags
        self.text_tags = ('strong','em','u')

        self.text_front.tag_configure("strong", font = ('Arial', 10, 'bold',))
        self.text_back.tag_configure("strong", font = ('Arial', 10, 'bold',))
        self.text_front.tag_configure("em", font = ('Arial', 10, 'italic'))
        self.text_back.tag_configure("em", font = ('Arial', 10, 'italic'))
        self.text_front.tag_configure("u", font = ('Arial', 10, 'underline',))
        self.text_back.tag_configure("u", font = ('Arial', 10, 'underline',))

        self.add_button = ttk.Button(self.frame_add_card, text = "Add", command = self.add, padding=4)
        self.add_button.grid(row = 4, column = 0, columnspan = 2, pady=2)

        # SEPARATOR
        ttk.Separator(self.frame_main, orient=HORIZONTAL).grid(row=2, column=0, columnspan=2, sticky=EW, pady=4)

        # EDIT CARD FRAME
        ttk.Label(self.frame_main, text="CARD PREVIEW", style='Title.TLabel').grid(row=0, column=0)

        self.frame_edit_card = ttk.Frame(self.frame_main)
        self.frame_edit_card.grid(row = 1, column = 0)

        ttk.Label(self.frame_edit_card, text = "Front side").grid(row = 0, column = 0, columnspan = 2, pady = 5)
        ttk.Label(self.frame_edit_card, text = "Back side").grid(row = 2, column = 0, columnspan = 2, pady = 5)

        self.front_preview = Text(self.frame_edit_card, width=40, height=4, font=('Arial', 10))
        self.front_preview.grid(row = 1, column = 0, columnspan = 2, pady=5, padx=5)

        self.back_preview = Text(self.frame_edit_card, width=40, height=4, font=('Arial', 10))
        self.back_preview.grid(row = 3, column = 0, columnspan = 2, pady=5, padx=5)

        self.update_button = ttk.Button(self.frame_edit_card, text = "Update", command = self.update, padding=4)
        self.update_button.grid(row = 4, column = 0, sticky=E, padx=2)

        self.delete_button = ttk.Button(self.frame_edit_card, text = "Delete", command = self.delete, padding=4)
        self.delete_button.grid(row = 4, column = 1, sticky=W, padx=2)

        # CONTENT FRAME
        self.frame_content = ttk.Frame(self.frame_main)
        self.frame_content.grid(row=3, column=0, columnspan=2)

        self.card_list = Listbox(self.frame_content, width=90, height=10)
        self.card_list.grid(row=2, column=0, pady=8)
        self.card_list.bind("<<ListboxSelect>>", self.select)

        self.bold_button = ttk.Button(self.frame_add_card,
                                      text = "B",
                                      command = lambda: self.text_edit("BOLD"),
                                      width = 2)
        self.italic_button = ttk.Button(self.frame_add_card,
                                      text = "I",
                                      command = lambda: self.text_edit("ITALIC"),
                                      width = 2)
        self.underline_button = ttk.Button(self.frame_add_card,
                                      text = "U",
                                      command = lambda: self.text_edit("UNDERLINE"),
                                      width = 2)

        # self.bold_button.grid(row = 5, column = 0, padx = 5)
        # self.italic_button.grid(row = 5, column = 1, padx = 5)
        # self.underline_button.grid(row = 6, column = 0, pady = 5)

        self.selection = None
        self.view()

    # Menu methods
    def import_file(self):
        pass

    def export_file(self):
        pass

    def close_file(self):
        pass

    # Database menu methods
    def load_db(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select database", filetypes=(('db files', '*.db'),))
        Flashcards.set_db_file(filename)
        self.view()

    def delete_all(self):
        confirmation = messagebox.askyesno(title = "Confirmation", message = "Are you sure that you want to delete all flascards ?")
        if confirmation == True:
            Flashcards.delete_all()
            self.view()

            self.front_preview.delete("1.0", END)
            self.back_preview.delete("1.0", END)

            self.selection = None

    def add_from_json(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(('json files', '*.json'),))
        with open(filename, 'r') as fp:
            cards = json.load(fp)

        records_inserted = 0
        for card in cards:
            success = self.insert_record(card["front"], card["back"])
            records_inserted += success

        messagebox.showinfo(title="Import",
                        message="Imported successfully {0} out of {1} records".format(records_inserted, len(cards)))

    def add(self):
        if len(self.text_front.get("1.0", END)) <= 1 and len(self.text_back.get("1.0", END)) <= 1:
            messagebox.showerror(title = "Required field", message = "Please fill the front and the back side!")
        elif len(self.text_front.get("1.0", END)) <= 1:
            messagebox.showerror(title = "Required field", message = "Please fill the front side!")
        elif len(self.text_back.get("1.0", END)) <= 1:
            messagebox.showerror(title = "Required field", message = "Please fill the back side!")
        else:
            front_html = self.convert_to_html(self.text_front)
            back_html = self.convert_to_html(self.text_back)
            Flashcards.add(front_html, back_html)

            self.text_front.delete("1.0", END)
            self.text_back.delete("1.0", END)

            self.view()

    def insert_record(self, front, back):
        if type(front) == 'str' and type(back) == 'str':
            Flashcards.add(front, back)
            return 1
        return 0

    def view(self):
        self.card_list.delete(0, END)
        for row in Flashcards.view():
            self.card_list.insert(END, row)

    def update(self):
        if self.selection:
            Flashcards.update(self.selection[0],
                              self.convert_to_html(self.front_preview),
                              self.convert_to_html(self.back_preview))

            self.view()

    def delete(self):
        if self.selection:
            Flashcards.delete(self.selection[0])
            self.view()

            self.front_preview.delete("1.0", END)
            self.back_preview.delete("1.0", END)

            self.selection = None

    def select(self, event):
        if len(self.card_list.curselection()) > 0:
            idx = self.card_list.curselection()[0]
            self.selection = self.card_list.get(idx) # selects a tuple

            self.front_preview.delete("1.0", END)
            self.front_preview.insert("1.0", self.selection[1])

            self.back_preview.delete("1.0", END)
            self.back_preview.insert("1.0", self.selection[2])

    def export(self):
        data = [{"front":row[1], "back":row[2]} for row in Flashcards.view()]
        filename = filedialog.asksaveasfilename(defaultextension = ".json")
        if filename is not None:
            with open(filename, 'w') as outfile:
                json.dump(data, outfile)

        messagebox.showinfo(title = "Export", message = "All flashcards were exported!")

    def convert_to_html(self, text_widget):
        html = ""
        for (key, value, idx) in text_widget.dump("1.0", END):
            if key == "tagon" and value in self.text_tags:
                html += "<{}>".format(value.strip())
            elif key == "tagoff" and value in self.text_tags:
                html += "</{}>".format(value.strip())
            elif key == "text":
                html += value.strip()
        return str(html)

    def text_edit(self, action):
        actions = {
            "BOLD" : "strong",
            "ITALIC": "em",
            "UNDERLINE": "u",
        }
        tag = actions.get(action)

        if self.text_front.tag_ranges("sel"):
            self.text_front.tag_add(tag, SEL_FIRST, SEL_LAST)
        elif self.text_back.tag_ranges("sel"):
            self.text_back.tag_add(tag, SEL_FIRST, SEL_LAST)

def main():
    root = Tk()
    app = Application(root)
    root.mainloop()

if __name__ == "__main__": main()