import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkfont
from PIL import Image, ImageTk
import tkinter.filedialog as filedialog

class Professor:
    def __init__(self, Name, Title, Contact, Email, Picture=None):
        self.Name = Name
        self.Title = Title
        self.Contact = Contact
        self.Email = Email
        self.Picture = Picture

class ProfessorDirectory:
    def __init__(self, root):
        self.root = root
        self.root.title("Professor Directory")
        self.root.geometry("1000x700")  # Increased window size for better spacing
        
        # Modern color palette
        self.colors = {
            'primary': '#2563eb',      # Modern blue
            'secondary': '#3b82f6',    # Lighter blue
            'background': '#f8fafc',   # Light gray background
            'surface': '#ffffff',      # White surface
            'text': '#1e293b',         # Dark text
            'text_secondary': '#64748b' # Secondary text
        }
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure modern styles
        self.style.configure('Modern.TFrame',
                           background=self.colors['background'])
        
        # Modern button style
        self.style.configure('Modern.TButton',
                           padding=(20, 10),
                           background=self.colors['primary'],
                           foreground='white',
                           font=('Segoe UI', 10),
                           borderwidth=0)
        self.style.map('Modern.TButton',
                      background=[('active', self.colors['secondary'])])
        
        # Modern title style
        self.style.configure('Modern.Title.TLabel',
                           font=('Segoe UI', 28, 'bold'),
                           background=self.colors['background'],
                           foreground=self.colors['text'])
        
        # Modern treeview style
        self.style.configure('Modern.Treeview',
                           background=self.colors['surface'],
                           fieldbackground=self.colors['surface'],
                           foreground=self.colors['text'],
                           rowheight=40,
                           font=('Segoe UI', 10))
        self.style.configure('Modern.Treeview.Heading',
                           font=('Segoe UI', 11, 'bold'),
                           background=self.colors['primary'],
                           foreground='white',
                           padding=10)
        self.style.map('Modern.Treeview',
                      background=[('selected', self.colors['secondary'])],
                      foreground=[('selected', 'white')])
        
        # Modern entry style
        self.style.configure('Modern.TEntry',
                           padding=10,
                           fieldbackground=self.colors['surface'])
        
        self.professors = [
            Professor("Mr. Brian Sarmiento", "Instructor", "+1-555-0123", "brianjmesonez@gmail.com"),
            Professor("Dr. Charles Tabares", "Professor", "+1-555-0124", "sarah.johnson@university.edu"),
            Professor("Dr. Wensley Naarte", "Instructor", "+1-555-0125", "michael.brown@university.edu")
        ]
        
        self.root.configure(bg=self.colors['background'])
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with padding
        main_container = ttk.Frame(self.root, style='Modern.TFrame', padding=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title with modern spacing
        title_frame = ttk.Frame(main_container, style='Modern.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 30))
        ttk.Label(title_frame, 
                 text="Professor Directory",
                 style='Modern.Title.TLabel').pack(anchor='w')
        ttk.Label(title_frame,
                 text="Manage and search for professors",
                 font=('Segoe UI', 12),
                 foreground=self.colors['text_secondary'],
                 background=self.colors['background']).pack(anchor='w', pady=(5,0))

        # Search and action frame
        search_frame = ttk.Frame(main_container, style='Modern.TFrame')
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Modern search box
        search_container = ttk.Frame(search_frame, style='Modern.TFrame')
        search_container.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.update_results)
        search_entry = ttk.Entry(search_container,
                               textvariable=self.search_var,
                               font=('Segoe UI', 11),
                               width=40)
        search_entry.pack(side=tk.LEFT, padx=(0, 20), ipady=8)
        search_entry.insert(0, "Search professors...")
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, tk.END) if search_entry.get() == "Search professors..." else None)
        search_entry.bind('<FocusOut>', lambda e: search_entry.insert(0, "Search professors...") if not search_entry.get() else None)
        
        # Add button with modern style
        add_btn = ttk.Button(search_frame,
                           text="+ Add Professor",
                           style='Modern.TButton',
                           command=self.add_professor)
        add_btn.pack(side=tk.RIGHT)
        
        # Results tree with modern styling
        tree_container = ttk.Frame(main_container, style='Modern.TFrame')
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(tree_container,
                                columns=('Name', 'Title', 'Contact', 'Email'),
                                show='headings',
                                style='Modern.Treeview')
        
        # Modern column configuration
        column_widths = {
            'Name': 300,
            'Title': 200,
            'Contact': 200,
            'Email': 250
        }
        for header, width in column_widths.items():
            self.tree.heading(header, text=header)
            self.tree.column(header, width=width, anchor='w')
        
        # Lock column movement by disabling drag functionality
        def disable_column_drag(event):
            return "break" 

        self.tree.bind("<B1-Motion>", disable_column_drag)

        # Modern scrollbar
        scrollbar = ttk.Scrollbar(tree_container,
                                orient=tk.VERTICAL,
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind('<<TreeviewSelect>>', self.show_selected_profile)
        self.update_results()

    def update_results(self, *args):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        search_text = self.search_var.get().lower()
        if search_text == "search professors...":
            search_text = ""
            
        for professor in self.professors:
            if (search_text in professor.Name.lower() or 
                search_text in professor.Title.lower() or 
                not search_text):
                self.tree.insert('', tk.END, values=(
                    professor.Name,
                    professor.Title,
                    professor.Contact,
                    professor.Email
                ))
    
    def show_selected_profile(self, event):
        selected = self.tree.selection()
        if not selected:
            return
            
        # Find the selected professor
        selected_name = self.tree.item(selected[0])['values'][0]
        selected_professor = next((prof for prof in self.professors if prof.Name == selected_name), None)
        
        if not selected_professor:
            return
        
        win = tk.Toplevel(self.root)
        win.title("Professor Profile")
        win.geometry("800x700")
        win.configure(bg=self.colors['background'])
        
        # Center the window
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        
        frame = ttk.Frame(win, style='Modern.TFrame', padding=30)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Profile header with picture
        header_frame = ttk.Frame(frame, style='Modern.TFrame')
        header_frame.pack(fill=tk.X, pady=(0,30))
        
        # Picture display
        picture_frame = ttk.Frame(header_frame, style='Modern.TFrame')
        picture_frame.pack(side=tk.LEFT, padx=(0,20))
        
        # Default profile picture
        default_image_path = 'default_profile.png'  # Create this default image
        
        try:
            if selected_professor.Picture:
                # Open and resize the image
                image = Image.open(selected_professor.Picture)
                image.thumbnail((250, 250))  # Larger preview
                photo = ImageTk.PhotoImage(image)
            else:
                # Use default image if no picture is set
                image = Image.open(default_image_path)
                image.thumbnail((250, 250))
                photo = ImageTk.PhotoImage(image)
        except Exception as e:
            # Fallback to a default image if loading fails
            try:
                image = Image.open(default_image_path)
                image.thumbnail((250, 250))
                photo = ImageTk.PhotoImage(image)
            except:
                # If even default image fails, create a blank image
                photo = None
        
        # Picture label
        if photo:
            picture_label = ttk.Label(picture_frame, 
                                      image=photo, 
                                      background=self.colors['background'])
            picture_label.image = photo  # Keep a reference
            picture_label.pack()
        
        # Name and title next to the picture
        name_frame = ttk.Frame(header_frame, style='Modern.TFrame')
        name_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(name_frame,
                 text=selected_professor.Name,
                 font=('Segoe UI', 24, 'bold'),
                 foreground=self.colors['text'],
                 background=self.colors['background']).pack(anchor='w')
        
        ttk.Label(name_frame,
                 text=selected_professor.Title,
                 font=('Segoe UI', 16),
                 foreground=self.colors['text_secondary'],
                 background=self.colors['background']).pack(anchor='w', pady=(5,0))
        
        # Profile details with modern layout
        details_frame = ttk.Frame(frame, style='Modern.TFrame')
        details_frame.pack(fill=tk.X, pady=20)
        
        # Detailed contact information with icons
        contact_info = [
            ('Contact', selected_professor.Contact, '📞'),
            ('Email', selected_professor.Email, '✉️')
        ]
        
        for field, value, icon in contact_info:
            detail_frame = ttk.Frame(details_frame, style='Modern.TFrame')
            detail_frame.pack(fill=tk.X, pady=10)
            
            ttk.Label(detail_frame,
                     text=f"{icon} {field}",
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['text_secondary'],
                     background=self.colors['background']).pack(anchor='w')
                     
            ttk.Label(detail_frame,
                     text=value,
                     font=('Segoe UI', 14),
                     foreground=self.colors['text'],
                     background=self.colors['background']).pack(anchor='w', pady=(5,0))
        
        # Close button
        ttk.Button(frame,
                  text="Close Profile",
                  style='Modern.TButton',
                  command=win.destroy).pack(pady=20)

    def add_professor(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add a new Professor")
        dialog.geometry("1000x1000")
        dialog.configure(bg=self.colors['background'])
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        main_frame = ttk.Frame(dialog, style='Modern.TFrame', padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with description
        ttk.Label(main_frame,
                 text="Add New Professor",
                 font=('Segoe UI', 24, 'bold'),
                 foreground=self.colors['text'],
                 background=self.colors['background']).pack(anchor='w')
        
        ttk.Label(main_frame,
                 text="Fill in the details below to add a new professor",
                 font=('Segoe UI', 12),
                 foreground=self.colors['text_secondary'],
                 background=self.colors['background']).pack(anchor='w', pady=(5,20))
        
        entries = {}
        field_info = {
            'Name': 'Full name of the professor',
            'Title': 'Academic title or position',
            'Contact': 'Contact number',
            'Email': 'Professional email address'
        }
        
        # Create entry fields
        for field, hint in field_info.items():
            field_frame = ttk.Frame(main_frame, style='Modern.TFrame')
            field_frame.pack(fill=tk.X, pady=10)
            
            ttk.Label(field_frame,
                     text=field,
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['text_secondary'],
                     background=self.colors['background']).pack(anchor='w')
            
            ttk.Label(field_frame,
                     text=hint,
                     font=('Segoe UI', 10),
                     foreground=self.colors['text_secondary'],
                     background=self.colors['background']).pack(anchor='w', pady=(0,5))
            
            entry = ttk.Entry(field_frame,
                            font=('Segoe UI', 11),
                            width=40)
            entry.pack(fill=tk.X, ipady=8)
            entries[field] = entry
        
        # Add picture frame
        picture_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        picture_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(picture_frame, text="Profile Picture", 
                 font=('Segoe UI', 12, 'bold'),
                 background=self.colors['background']).pack(anchor='w')
        
        ttk.Label(picture_frame, text="Upload a profile picture (optional)",
                 font=('Segoe UI', 10),
                 background=self.colors['background']).pack(anchor='w', pady=(0,5))
        
        picture_preview = ttk.Label(picture_frame, background=self.colors['background'])
        picture_preview.pack(pady=10)
        
        selected_picture = {'path': None}
        
        def select_picture():
            file_path = filedialog.askopenfilename(
                title="Select Profile Picture",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )
            if file_path:
                try:
                    image = Image.open(file_path)
                    image.thumbnail((150, 150))  # Resize for preview
                    photo = ImageTk.PhotoImage(image)
                    picture_preview.configure(image=photo)
                    picture_preview.image = photo  # Keep reference
                    selected_picture['path'] = file_path
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load image: {str(e)}")
        
        ttk.Button(picture_frame, text="Choose Picture",
                  style='Modern.TButton',
                  command=select_picture).pack(anchor='w')
        
        def save_professor():
            values = {field: entry.get().strip() for field, entry in entries.items()}
            
            # Validation
            if not all(values.values()):
                empty_fields = [field for field, value in values.items() if not value]
                messagebox.showerror("Error", f"Please fill in all fields: {', '.join(empty_fields)}")
                entries[empty_fields[0]].focus_set()
                return
            
            # Email validation
            if '@' not in values['Email'] or '.' not in values['Email']:
                messagebox.showerror("Error", "Please enter a valid email address")
                entries['Email'].focus_set()
                return
            
            # Phone validation
            if not any(c.isdigit() for c in values['Contact']):
                messagebox.showerror("Error", "Contact number must contain at least one digit")
                entries['Contact'].focus_set()
                return
            
            # Add picture to values
            values['Picture'] = selected_picture['path']
            
            self.professors.append(Professor(**values))
            self.update_results()
            dialog.destroy()
            messagebox.showinfo("Success", "Professor added successfully!")
        
        # Button frame
        button_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        button_frame.pack(fill=tk.X, pady=(20,0))
        
        # Cancel button
        ttk.Button(button_frame,
                  text="Cancel",
                  style='Modern.TButton',
                  command=dialog.destroy).pack(side=tk.LEFT)
        
        # Save button
        save_btn = ttk.Button(button_frame,
                            text="Save Professor",
                            style='Modern.TButton',
                            command=save_professor)
        save_btn.pack(side=tk.RIGHT)
        
        # Set initial focus
        entries['Name'].focus_set()
        
        # Keyboard shortcuts
        dialog.bind('<Return>', lambda e: save_professor())
        dialog.bind('<Escape>', lambda e: dialog.destroy())

def main():
    root = tk.Tk()
    app = ProfessorDirectory(root)
    root.mainloop()

if __name__ == "__main__":
    main()
