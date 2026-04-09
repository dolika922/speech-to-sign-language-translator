import tkinter as tk
from tkinter import ttk
from tkinter import Label, Button, Text, Entry, StringVar, messagebox
from PIL import Image, ImageTk, ImageSequence
import speech_recognition as sr
import os
import string
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- Globals ----------
image_refs = []
# ✅ Get correct project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Correct file paths
USER_FILE = os.path.join(BASE_DIR, "users.json")
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
LETTERS_PATH = os.path.join(BASE_DIR, "letters")

current_user = None
from datetime import datetime

# ✅ Create files if not exist
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump([], f)

# ---------- Functions ----------

# Switch pages
def show_page(page):
    page.tkraise()

# Save new user
def signup_user():
    username = su_username.get().strip()
    password = su_password.get().strip()
    age = su_age.get().strip()
    gender = su_gender.get().strip()
    city = su_city.get().strip()
    

    if not all([username, password, age, gender]) or city == "Select City":
        messagebox.showerror("Error", "All fields required")
        return

    with open(USER_FILE, "r") as f:
        users = json.load(f)

    if any(u["username"] == username for u in users):
        messagebox.showerror("Error", "Username already exists")
        return

    users.append({
        "username": username,
        "password": password,
        "age": age,
        "gender": gender,
        "city": city
    })

    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

    messagebox.showinfo("Success", "Signup successful! Please login.")
    su_username.set(""); su_password.set(""); su_age.set(""); su_gender.set(""); su_city.set("")

####
def save_history(text):
    if not current_user:
        return

    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)

    data.append({
        "username": current_user["username"],
        "text": text,
        "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Login
def login_user():
    username = li_username.get().strip()
    password = li_password.get().strip()

    with open(USER_FILE, "r") as f:
        users = json.load(f)

    for u in users:
        if u["username"] == username and u["password"] == password:
            global current_user
            current_user = u
            show_page(main_page)
            show_home()
            return

    messagebox.showerror("Error", "Invalid username or password")

# ---------- Logout ----------
def logout_user():
    global current_user
    current_user = None
    show_page(home_page)
def add_greeting(parent):
    try:
        name = current_user.get("username", "")
        tk.Label(parent,
                 text=f"Hello, {name} 👋",
                 font=("Helvetica", 18, "bold"),
                 bg="#f0f8ff").pack(pady=10)
    except:
        pass



# Show Profile
def show_profile():
    for widget in content_frame.winfo_children():
        widget.destroy()
    add_greeting(content_frame)
    

    tk.Label(content_frame, text="Your Profile",
             font=("Helvetica", 24, "bold"),
             bg="#f0f8ff").pack(pady=20)

    profile_frame = tk.Frame(content_frame, bg="white", bd=3, relief="solid")
    profile_frame.pack(pady=10, ipadx=40, ipady=30)

    fields = ["username", "age", "gender", "city"]
    entries = {}

    for field in fields:
        tk.Label(profile_frame, text=field.capitalize(),
                 font=("Helvetica", 14), bg="white").pack(pady=5)

        var = StringVar(value=current_user[field])
        ent = tk.Entry(profile_frame, textvariable=var,
                       font=("Helvetica", 14), state="readonly")
        ent.pack(pady=5)
        entries[field] = (var, ent)

    tk.Label(profile_frame, text="Enter Password to Edit",
             font=("Helvetica", 14), bg="white").pack(pady=10)

    verify_pass = StringVar()
    tk.Entry(profile_frame, textvariable=verify_pass,
             show="*", font=("Helvetica", 14)).pack(pady=5)

    def enable_edit():
        if verify_pass.get() == current_user["password"]:
            for var, ent in entries.values():
                ent.config(state="normal")
            messagebox.showinfo("Verified", "You can now edit")
        else:
            messagebox.showerror("Error", "Wrong password")

    def save_changes():
        with open(USER_FILE, "r") as f:
            users = json.load(f)

        for u in users:
            if u["username"] == current_user["username"]:
                for field in fields:
                    u[field] = entries[field][0].get()
                current_user.update(u)

        with open(USER_FILE, "w") as f:
            json.dump(users, f, indent=4)

        messagebox.showinfo("Success", "Profile Updated")
        show_profile()

    tk.Button(profile_frame, text="Verify Password",
              command=enable_edit, bg="#4CAF50", fg="white").pack(pady=10)

    tk.Button(profile_frame, text="Save Changes",
              command=save_changes, bg="#2196F3", fg="white").pack(pady=5)


# Show Contact / Info
def show_contact():
    for widget in content_frame.winfo_children():
        widget.destroy()
    add_greeting(content_frame)


    # Header
    tk.Label(content_frame, text="Contact / Info", font=("Helvetica", 20, "bold")).pack(pady=10)
    tk.Label(content_frame, text="Indian Sign Language Translator App", font=("Helvetica", 14)).pack(pady=5)

    # Column headers
    headers = ["Name", "Roll No", "Email", "College", "Role"]
    header_frame = tk.Frame(content_frame, bg="#f0f8ff")
    header_frame.pack(pady=10, fill="x")
    for h in headers:
        tk.Label(header_frame, text=h, font=("Helvetica", 14, "bold"), width=20, anchor="w").pack(side="left", padx=5)

    # Team members data
    members = [
        {"name": "N. Dolika", "roll": "227R1A73A8", "email": "227r1a73a8@cmrtc.ac.in", "college": "CMR Technical Campus", "role": "Team Leader"},
        {"name": "K. Satish Kumar", "roll": "227R1A7393", "email": "227r1a7393@cmrtc.ac.in", "college": "CMR Technical Campus", "role": "Team Mate"},
        {"name": "D. Pooja", "roll": "237R5A7313", "email": "237r1a7313@cmrtc.ac.in", "college": "CMR Technical Campus", "role": "Team Mate"},
    ]

    # Display members in horizontal rows
    for member in members:
        row_frame = tk.Frame(content_frame, bg="#f0f8ff")
        row_frame.pack(fill="x", pady=2)
        tk.Label(row_frame, text=member["name"], font=("Helvetica", 12), width=20, anchor="w").pack(side="left", padx=5)
        tk.Label(row_frame, text=member["roll"], font=("Helvetica", 12), width=20, anchor="w").pack(side="left", padx=5)
        tk.Label(row_frame, text=member["email"], font=("Helvetica", 12), width=30, anchor="w").pack(side="left", padx=5)
        tk.Label(row_frame, text=member["college"], font=("Helvetica", 12), width=25, anchor="w").pack(side="left", padx=5)
        tk.Label(row_frame, text=member["role"], font=("Helvetica", 12), width=15, anchor="w").pack(side="left", padx=5)

def clear_history():
    if not current_user:
        return

    confirm = messagebox.askyesno("Confirm", "Clear all history?")
    if not confirm:
        return

    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    # ✅ FIXED
    new_data = [
        h for h in data
        if h.get("username") != current_user.get("username")
    ]

    with open(HISTORY_FILE, "w") as f:
        json.dump(new_data, f, indent=4)

    messagebox.showinfo("Done", "History cleared!")
    show_history()


def show_history():
    for widget in content_frame.winfo_children():
        widget.destroy()

    add_greeting(content_frame)

    tk.Label(content_frame, text="Your Translation History",
             font=("Helvetica", 22, "bold"),
             bg="#f0f8ff").pack(pady=10)

    tk.Button(content_frame, text="Clear History 🗑",
              command=clear_history,
              bg="red", fg="white",
              font=("Helvetica", 12)).pack(pady=5)

    canvas = tk.Canvas(content_frame, bg="#f0f8ff")
    scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#f0f8ff")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    # ✅ FIXED
    if not current_user:
        tk.Label(scroll_frame, text="Please login first",
                 font=("Helvetica", 14), bg="#f0f8ff").pack(pady=20)
        return

    user_history = [
        h for h in data
        if h.get("username") == current_user.get("username")
    ]

    if not user_history:
        tk.Label(scroll_frame, text="No history found",
                 font=("Helvetica", 14), bg="#f0f8ff").pack(pady=20)
        return

    for h in reversed(user_history):
        frame = tk.Frame(scroll_frame, bg="white", bd=2, relief="solid")
        frame.pack(pady=5, padx=40, fill="x")

        tk.Label(frame, text=h.get("time", ""),
                 font=("Helvetica", 10), bg="white", fg="gray").pack(anchor="e", padx=5)

        tk.Label(frame, text=h.get("text", ""),
                 font=("Helvetica", 14),
                 bg="white").pack(anchor="w", padx=10, pady=5)
# Show Home / Translator
def show_home():
    for widget in content_frame.winfo_children():
        widget.destroy()
    add_greeting(content_frame)


    tk.Label(content_frame, text="Indian Sign Language Translator", font=("Helvetica", 20, "bold")).pack(pady=10)

    global text_box, status_label, image_frame
    text_box = Text(content_frame, height=2, font=("Helvetica", 16))
    text_box.pack(pady=10)

    status_label = Label(content_frame, text="", font=("Helvetica", 12), bg="#f0f8ff")
    status_label.pack(pady=5)

    listen_btn = Button(content_frame, text="Start Listening", font=("Helvetica", 14),
                        command=start_listening, bg="#4CAF50", fg="white")
    listen_btn.pack(pady=5)

    refresh_btn = Button(content_frame, text="Refresh", font=("Helvetica", 14),
                         command=refresh_text, bg="#2196F3", fg="white")
    refresh_btn.pack(pady=5)

    image_frame = tk.Frame(content_frame, bg="#f0f8ff")
    image_frame.pack(pady=20)

    exit_btn = Button(content_frame, text="Exit", font=("Helvetica", 12),
                      command=root.destroy, bg="red", fg="white")
    exit_btn.pack(pady=5)

# Refresh translator
def refresh_text():
    text_box.delete(1.0, tk.END)
    for widget in image_frame.winfo_children():
        widget.destroy()
    image_refs.clear()
    status_label.config(text="")

# Speech recognition function
def start_listening():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        root.update()
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, text)
            status_label.config(text="Speech Recognized!")
            show_images(text)
            save_history(text)

        except sr.UnknownValueError:
            status_label.config(text="Could not understand audio")
        except sr.RequestError as e:
            status_label.config(text=f"Recognition error: {e}")


def show_images(text):
    global image_frame
    text = text.lower().strip()
    for widget in image_frame.winfo_children():
        widget.destroy()
    image_refs.clear()

    # First, try GIF
    gif_path = os.path.join("ISL_Gifs", f"{text}.gif")
    if os.path.exists(gif_path):
        img = Image.open(gif_path)
        w, h = img.size
        ratio = min(300/w, 300/h)
        new_w, new_h = int(w*ratio), int(h*ratio)
        frames = [ImageTk.PhotoImage(frame.copy().resize((new_w, new_h)))
                  for frame in ImageSequence.Iterator(img)]
        lbl = Label(image_frame)
        lbl.pack()
        def animate(index):
            frame = frames[index]
            lbl.config(image=frame)
            root.after(100, animate, (index + 1) % len(frames))
        animate(0)
        return  # GIF exists, we don't need letters

    # If GIF doesn't exist, show letter images
    row_frame = tk.Frame(image_frame, bg="#f0f8ff")
    row_frame.pack()
    count = 0

    for char in text:
        if char in string.ascii_lowercase:
            img_path = os.path.join(LETTERS_PATH, f"{char}.jpg")
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((120, 120))
                photo = ImageTk.PhotoImage(img)
                image_refs.append(photo)
                lbl = tk.Label(row_frame, image=photo, bg="#f0f8ff")
                lbl.pack(side="left", padx=5, pady=5)
                count += 1
                if count % 8 == 0:
                    row_frame = tk.Frame(image_frame, bg="#f0f8ff")
                    row_frame.pack()

# ---------- UI Setup ----------
root = tk.Tk()
root.title("ISL Translator")
root.geometry("1000x700")
root.configure(bg="#f0f8ff")

# --- Frames ---
home_page = tk.Frame(root, bg="#f0f8ff")
home_page.place(relwidth=1, relheight=1)

main_page = tk.Frame(root, bg="#f0f8ff")
main_page.place(relwidth=1, relheight=1)

# ---------- Home Page UI with Scrollable Signup ----------
# ---------- Home Page UI ----------

# Titles
tk.Label(home_page, text="Speech to Sign Language Translator",
         font=("Helvetica", 26, "bold"), bg="#f0f8ff").pack(pady=20)

tk.Label(home_page, text="Indian Sign Language Translator",
         font=("Helvetica", 20), bg="#f0f8ff").pack(pady=10)

tk.Label(home_page, text="Existing User ? login",
         font=("Helvetica", 16, "bold"),
         bg="#f0f8ff").place(relx=0.2, rely=0.32, anchor="center")

tk.Label(home_page, text="New user ? sign up",
         font=("Helvetica", 16, "bold"),
         bg="#f0f8ff").place(relx=0.8, rely=0.28, anchor="center")


# ========== LOGIN BOX (LEFT) ==========
login_frame = tk.Frame(home_page, bg="white", bd=3, relief="solid")
login_frame.place(relx=0.2, rely=0.62, anchor="center", width=350, height=300)

tk.Label(login_frame, text="LOGIN", font=("Helvetica", 18, "bold"), bg="white").pack(pady=15)

tk.Label(login_frame, text="Username", font=("Helvetica", 12), bg="white").pack()
li_username = StringVar()
tk.Entry(login_frame, textvariable=li_username, font=("Helvetica", 12)).pack(pady=5)

tk.Label(login_frame, text="Password", font=("Helvetica", 12), bg="white").pack()
li_password = StringVar()
tk.Entry(login_frame, textvariable=li_password, show="*", font=("Helvetica", 12)).pack(pady=5)

tk.Button(login_frame, text="Login", font=("Helvetica", 12),
          command=login_user, bg="#4CAF50", fg="white").pack(pady=15)


# ========== SIGNUP BOX (RIGHT) ==========
# ========== SIGNUP BOX (RIGHT) ==========
signup_frame = tk.Frame(home_page, bg="white", bd=3, relief="solid")
signup_frame.place(relx=0.8, rely=0.58, anchor="center", width=360, height=440)

tk.Label(signup_frame, text="NEW USER SIGN UP",
         font=("Helvetica", 18, "bold"), bg="white").pack(pady=15)

entry_style = {
    "font": ("Helvetica", 12),
    "bg": "#2b2b2b",
    "fg": "white",
    "insertbackground": "white",
    "width": 25
}

# Username
tk.Label(signup_frame, text="Username", bg="white").pack()
su_username = StringVar()
tk.Entry(signup_frame, textvariable=su_username, **entry_style).pack(pady=6)

# Password
tk.Label(signup_frame, text="Password", bg="white").pack()
su_password = StringVar()
tk.Entry(signup_frame, textvariable=su_password, show="*", **entry_style).pack(pady=6)

# Age Dropdown
tk.Label(signup_frame, text="Age", bg="white").pack()
su_age = StringVar()
age_combo = ttk.Combobox(
    signup_frame,
    textvariable=su_age,
    values=[str(i) for i in range(8, 61)],
    state="readonly",
    width=23
)
age_combo.pack(pady=6)
age_combo.set("Select Age")

# Gender
tk.Label(signup_frame, text="Gender", bg="white").pack()
su_gender = StringVar(value="Male")
gender_frame = tk.Frame(signup_frame, bg="white")
gender_frame.pack(pady=5)
tk.Radiobutton(gender_frame, text="Male", variable=su_gender, value="Male", bg="white").pack(side="left", padx=5)
tk.Radiobutton(gender_frame, text="Female", variable=su_gender, value="Female", bg="white").pack(side="left", padx=5)
tk.Radiobutton(gender_frame, text="Rather not say", variable=su_gender, value="Rather not say", bg="white").pack(side="left", padx=5)

# City
# City Dropdown (Capital Cities)
tk.Label(signup_frame, text="City", bg="white").pack()

su_city = StringVar()

cities = [
    "Amaravati", "Hyderabad", "Bengaluru", "Chennai",
    "Mumbai", "Panaji", "Bhopal", "Jaipur",
    "Lucknow", "Patna", "Ranchi", "Raipur",
    "Bhubaneswar", "Kolkata", "Gangtok", "Shillong",
    "Dispur", "Agartala", "Imphal", "Aizawl",
    "Kohima", "Itanagar", "Chandigarh", "Dehradun",
    "Shimla", "Srinagar"
]

city_combo = ttk.Combobox(
    signup_frame,
    textvariable=su_city,
    values=cities,
    state="readonly",
    width=23
)
city_combo.pack(pady=6)
city_combo.set("Select City")
# Button
tk.Button(signup_frame, text="Create Account", font=("Helvetica", 13, "bold"),
          command=signup_user, bg="#2196F3", fg="white", width=20).pack(pady=20)



# ---------- Main Page UI ----------
nav_frame = tk.Frame(main_page, bg="#f0f8ff")
nav_frame.pack(fill="x", pady=10)
tk.Button(nav_frame, text="Profile", font=("Helvetica", 14), command=show_profile).pack(side="left", padx=10)
tk.Button(nav_frame, text="Home", font=("Helvetica", 14), command=show_home).pack(side="left", padx=10)
tk.Button(nav_frame, text="History", font=("Helvetica", 14), command=show_history).pack(side="left", padx=10)
tk.Button(nav_frame, text="Contact", font=("Helvetica", 14), command=show_contact).pack(side="left", padx=10)
tk.Button(nav_frame, text="Logout", font=("Helvetica", 14), command=logout_user, bg="#f44336", fg="white").pack(side="right", padx=10)




content_frame = tk.Frame(main_page, bg="#f0f8ff")
content_frame.pack(fill="both", expand=True)

# ---------- Start App ----------
show_page(home_page)
root.mainloop()