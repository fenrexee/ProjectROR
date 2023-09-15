import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import numpy as np
from ttkthemes import ThemedStyle
user_data = {"tomato": "123"}  

class LoginPage:
    def __init__(self, root):
        self.root = root
        root.title("Login Page")

        self.style = ThemedStyle(root)
        self.style.set_theme("plastik")

        self.username_label = ttk.Label(root, text="Username:")
        self.username_label.grid(row=0, column=0, sticky="w")

        self.username_entry = ttk.Entry(root)
        self.username_entry.grid(row=0, column=1)

        self.password_label = ttk.Label(root, text="Password:")
        self.password_label.grid(row=1, column=0, sticky="w")

        self.password_entry = ttk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = ttk.Button(root, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2)

        self.forgot_password_button = ttk.Button(root, text="Forgot Password", command=self.forgot_password)
        self.forgot_password_button.grid(row=2, column=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in user_data:
            stored_password = user_data[username]
            if password == stored_password:
                self.root.destroy()
                self.open_main_app()
            else:
                messagebox.showerror("Login Failed", "Incorrect password.")
        else:
            messagebox.showerror("Login Failed", "User not found.")

    def open_main_app(self):
        main_app_window = tk.Tk()
        main_app = MainApplication(main_app_window)
        main_app_window.mainloop()

    def forgot_password(self):
        username = self.username_entry.get()
        if username in user_data:
            messagebox.showinfo("Forgot Password", f"Your password for {username} is: {user_data[username]}")
        else:
            messagebox.showerror("Forgot Password", "User not found.")

class MainApplication:
    def __init__(self, root):
        self.root = root
        root.title("Main Application")

        self.style = ThemedStyle(root)
        self.style.set_theme("plastik")

        self.welcome_label = ttk.Label(root, text="Welcome to the Main Application!")
        self.welcome_label.pack(pady=20)

        self.fruit_mode_label = ttk.Label(root, text="Fruit Type:")
        self.fruit_mode_label.pack()

        self.fruit_mode_var = tk.StringVar()
        self.fruit_mode_var.set("Tomato")
        self.fruit_mode_menu = ttk.OptionMenu(root, self.fruit_mode_var, "Tomato", "Apple", "Banana", "Tomato")
        self.fruit_mode_menu.pack()

        self.start_button = ttk.Button(root, text="Start Detection", command=self.start_detection)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Stop Detection", command=self.stop_detection)
        self.stop_button.pack()

        self.logout_button = ttk.Button(root, text="Logout", command=self.logout)
        self.logout_button.pack()

        self.cam = None

    def start_detection(self):
        try:
            self.cam = cv2.VideoCapture(0)
            if self.cam.isOpened():
                self.show_webcam()
            else:
                messagebox.showerror("Error", "Failed to start webcam.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_webcam(self):
        if self.cam:
            while True:
                ret, frame = self.cam.read()
                if not ret:
                    break

                green_pixels = np.sum(frame[:, :, 1] > 100)
                red_pixels = np.sum(frame[:, :, 2] > 100)

                color_message = "Unclassified"
                if green_pixels > red_pixels:
                    color_message = "Green"
                elif red_pixels > green_pixels:
                    color_message = "Red"

                cv2.putText(frame, f"Detected Color: {color_message}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                cv2.imshow("Webcam Feed", frame)

                key = cv2.waitKey(1)
                if key == 27:
                    break

            self.cam.release()
            cv2.destroyAllWindows()
        else:
            messagebox.showerror("Error", "Webcam is not active.")

    def stop_detection(self):
        if self.cam:
            self.cam.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Detection Stopped", "Webcam is now stopped.")
        else:
            messagebox.showerror("Error", "Webcam is not active.")

    def logout(self):
        self.root.destroy()
        login_window = tk.Tk()
        login_page = LoginPage(login_window)
        login_window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    login_page = LoginPage(root)
    root.mainloop()
