import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import ttkbootstrap as ttk
import FINALSSEARCHBAR

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
