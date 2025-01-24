import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk, ImageEnhance

# Create the main window
root = tk.Tk()
root.title("Library Management System")
root.geometry('500x500')
root.resizable(0, 0)

# Center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position to center the window
x = (screen_width // 2) - (500 // 2)
y = (screen_height // 2) - (500 // 2)

# Position the window at the center of the screen
root.geometry(f"500x500+{x}+{y}")

root.iconbitmap('C:/Users/GIVEN/Downloads/target_icon.ico')

# Load the background image
image_path = "C:/Users/GIVEN/Pictures/WhatsApp_Image_lib.jpg"
image = Image.open(image_path)

# Convert to RGB mode in case it's not
image = image.convert("RGB")

# Enhance the image brightness
enhancer = ImageEnhance.Brightness(image)
faded_image = enhancer.enhance(0.5)

# Function to update the background image
def update_background():
    # Get the updated window size after it's rendered
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Resize the image to fit the window size
    resized_image = faded_image.resize((window_width, window_height), Image.Resampling.LANCZOS)

    # Convert the resized image to a Tkinter-compatible format
    bg_image = ImageTk.PhotoImage(resized_image)

    # Set as background image
    background_label.configure(image=bg_image)
    background_label.image = bg_image  # Keep a reference to avoid garbage collection

# Create the background label and place it
background_label = tk.Label(root)
background_label.place(relwidth=1, relheight=1)

# Update the background after window initialization
root.update_idletasks()
update_background()

# Create a frame to hold the username and password fields
frame = tk.Frame(root)
frame.pack(expand=True)
  # Use 'expand=True' to center it in the window

# frame = tk.Frame(root, bg="white", bd=2)  # White background, set border width
# frame.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.6, anchor="center")
# frame.config(bg="white")



# Username label and entry
username_label = tk.Label(frame, text="Username:")
username_label.grid(row=0, column=0, pady=10, padx=10)
username_entry = tk.Entry(frame,background='black', fg='white')
username_entry.grid(row=0, column=1, pady=10, padx=10)

# Password label and entry
password_label = tk.Label(frame, text="Password:")
password_label.grid(row=1, column=0, pady=10, padx=10)
password_entry = tk.Entry(frame, show="*",background='black', fg='white')
password_entry.grid(row=1, column=1, pady=10, padx=10)

c_v1 = IntVar(value=0)
def show_password():
  if (c_v1.get()==1):
    password_entry.config(show='')
  else:
     password_entry.config(show='*') 
c1 = tk.Checkbutton(frame, text = 'show password                          ', variable=c_v1, onvalue=1, offvalue=0, command=show_password)
c1.grid(row=2, column=0, columnspan=8)

# Dropdown for user role selection
clicked = StringVar() 
clicked.set('Student/Staff')
role_dropdown = OptionMenu(frame, clicked, 'Student', 'Staff')
role_dropdown.grid(row=3, columnspan=2, pady=10)

# Checkbuttons for terms and conditions
tk.Checkbutton(frame, text='Remember me                            ').grid(columnspan=5)
tk.Checkbutton(frame, text='Agree to Terms and Conditions?').grid(columnspan=5)


def on_click():
  login_button.config(text='Welcome back') #changes the login text to welcome back
# Login button
login_button = tk.Button(frame, background='black', fg='white', text="Login", command= on_click)
login_button.grid(row=6, columnspan=2, pady=10)

# Register button
register_button = tk.Button(frame, background='black', fg='white', text="Register")
register_button.grid(row=7, columnspan=2, pady=10)

# Bind resizing event to update the background image when window size changes
#root.bind('<Configure>', lambda event: update_background())

# Run the application
root.mainloop()
