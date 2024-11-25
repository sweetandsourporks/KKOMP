import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import ttkbootstrap as ttk

class Professor:
    def __init__(self, name, title, contact, email):
        self.name = name
        self.title = title
        self.contact = contact
        self.email = email


class local:
    def __init__(self, root):
        self.root = root
        self.root.title("Professor Directory")
        self.root.geometry("800x600")
        
        # Sample professor data
        self.professors = [
           Professor("Mr. Brian Sarmiento", "Instructor", 
                     "+1-555-0123", 
                     "brianjmesonez@gmail.com"),
            Professor("Dr. Charles Tabares", " Professor", 
                      "+1-555-0124", 
                     "sarah.johnson@university.edu"),
            Professor("Dr. Wensley Naarte", "Instructor", 
                      "+1-555-0125", 
                     "michael.brown@university.edu")
        ]
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.profile_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.search_tab, text='Professor Profiles')
        
        self.create_profile_widgets()
        self.create_search_widgets()
        
    def create_profile_widgets(self):
        # Professor selection
        select_frame = ttk.Frame(self.profile_tab, padding="10")
        select_frame.pack(fill=tk.X)
        
        ttk.Label(select_frame, text="Select Professor:").pack(side=tk.LEFT)
        self.professor_var = tk.StringVar()
        professor_names = [prof.name for prof in self.professors]
        self.professor_combo = ttk.Combobox(select_frame, 
                                          textvariable=self.professor_var,
                                          values=professor_names)
        self.professor_combo.pack(side=tk.LEFT, padx=5)
        self.professor_combo.bind('<<ComboboxSelected>>', self.update_profile)
        
        # Profile display
        self.profile_frame = ttk.LabelFrame(self.profile_tab, text="Professor Profile", 
                                          padding="20")
        self.profile_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Profile labels
        self.name_label = ttk.Label(self.profile_frame, text="")
        self.name_label.pack(anchor=tk.W, pady=2)
        
        self.title_label = ttk.Label(self.profile_frame, text="")
        self.title_label.pack(anchor=tk.W, pady=2)
        
        self.dept_label = ttk.Label(self.profile_frame, text="")
        self.dept_label.pack(anchor=tk.W, pady=2)
        
        self.contact_label = ttk.Label(self.profile_frame, text="")
        self.contact_label.pack(anchor=tk.W, pady=2)
        
        self.email_label = ttk.Label(self.profile_frame, text="")
        self.email_label.pack(anchor=tk.W, pady=2)
        
        self.spec_label = ttk.Label(self.profile_frame, text="")
        self.spec_label.pack(anchor=tk.W, pady=2)
        
        # Set default selection
        if professor_names:
            self.professor_combo.set(professor_names[0])
            self.update_profile(None)
            
    def create_search_widgets(self):
        # Search frame
        search_frame = ttk.Frame(self.search_tab, padding="10")
        search_frame.pack(fill=tk.X)
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        
        search_entry = ttk.Entry(search_frame, 
                               textvariable=self.search_var,
                               width=40,
                               font=('Arial', 12))
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.insert(0, "Search professors...")
        search_entry.bind('<FocusIn>', self.on_entry_click)
        search_entry.bind('<FocusOut>', self.on_focus_out)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.search_tab, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create Treeview for results
        self.tree = ttk.Treeview(results_frame, 
                                columns=('Name', 'Title', 'Contact', 'Email'),
                                show='headings')
        
        # Define headings
        headers = ['Name', 'Title', 'Contact', 'Email']
        for header in headers:
            self.tree.heading(header, text=header)
            self.tree.column(header, width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the Treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initial population of results
        self.update_results()
    
    def update_profile(self, event):
        selected_name = self.professor_var.get()
        professor = next((p for p in self.professors if p.name == selected_name), None)
        
        if professor:
            self.name_label.config(text=f"Name: {professor.name}")
            self.title_label.config(text=f"Title: {professor.title}")
            self.contact_label.config(text=f"Contact: {professor.contact}")
            self.email_label.config(text=f"Email: {professor.email}")
            
    def on_entry_click(self, event):
        if self.search_var.get() == 'Search professors...':
            event.widget.delete(0, tk.END)
            event.widget.config(foreground='black')
            
    def on_focus_out(self, event):
        if self.search_var.get() == '':
            event.widget.insert(0, 'Search professors...')
            event.widget.config(foreground='grey')
            
    def on_search_change(self, *args):
        self.update_results()
        
    def update_results(self):
        # Clear the current results
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        search_text = self.search_var.get().lower()
        if search_text == 'search professors...':
            search_text = ''
            
        # Filter and display results
        for professor in self.professors:
            if (search_text in professor.name.lower() or 
                search_text in professor.title.lower()):
                self.tree.insert('', tk.END, values=(
                    professor.name,
                    professor.title,
                    professor.contact,
                    professor.email,
                ))



# Function to upload and display an image
def upload_image():
    global img_label  # Make img_label global to update it if needed
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if file_path:
        img = Image.open(file_path)
        img = img.resize((100, 100), Image.ANTIALIAS)  # Resize image to fit in the window
        img_tk = ImageTk.PhotoImage(img)
        img_label.configure(image=img_tk)
        img_label.image = img_tk  # Keep a reference to avoid garbage collection


# Function to add professor details to the output box
def add_professor():
    name = name_entry.get()
    title = title_entry.get()
    contact = contact_entry.get()
    email = email_entry.get()

    if name and title and contact and email:
        output_textbox.insert(
            "end", 
            f"Name: {name}\nTitle: {title}\nContact: {contact}\nEmail: {email}\n\n"
        )
        name_entry.delete(0, "end")
        title_entry.delete(0, "end")
        contact_entry.delete(0, "end")
        email_entry.delete(0, "end")
    else:
        output_textbox.insert("end", "Please fill in all fields before adding.\n\n")

# Window setup
window = ttk.Window(themename="journal")
window.title("Professor Details")
window.geometry("500x400")

# Frame for the image
img_frame = ttk.Frame(master=window)
img_frame.pack(side="top", anchor="w", padx=10, pady=10)

# Image label (placeholder before uploading)
img_label = ttk.Label(master=img_frame)
img_label.pack()

# Button to upload image
upload_button = ttk.Button(
    master=img_frame, text="Upload Image", command=upload_image
)
upload_button.pack(pady=5)

# Input frame for professor details
input_frame = ttk.Frame(master=window)
input_frame.pack(pady=10)

# Name label and entry
name_label = ttk.Label(master=input_frame, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = ttk.Entry(master=input_frame, width=40)
name_entry.grid(row=0, column=1, padx=5, pady=5)

# Title label and entry
title_label = ttk.Label(master=input_frame, text="Title:")
title_label.grid(row=1, column=0, padx=5, pady=5)
title_entry = ttk.Entry(master=input_frame, width=40)
title_entry.grid(row=1, column=1, padx=5, pady=5)

# Contact label and entry
contact_label = ttk.Label(master=input_frame, text="Contact:")
contact_label.grid(row=2, column=0, padx=5, pady=5)
contact_entry = ttk.Entry(master=input_frame, width=40)
contact_entry.grid(row=2, column=1, padx=5, pady=5)

# Email label and entry
email_label = ttk.Label(master=input_frame, text="Email:")
email_label.grid(row=3, column=0, padx=5, pady=5)
email_entry = ttk.Entry(master=input_frame, width=40)
email_entry.grid(row=3, column=1, padx=5, pady=5)

# Button to add professor
add_button = ttk.Button(master=input_frame, text="Add Professor", command=add_professor)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

# Output text box to display details
output_textbox = tk.Text(master=window, height=10, width=60)
output_textbox.pack(pady=10)

# Run the application
window.mainloop()

def main():
    root = tk.Tk()
    app = local(root)
    root.mainloop()

if __name__ == "__main__":
    main()
