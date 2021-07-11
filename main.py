import _thread
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import instaloader


class InstaBackup(Frame):
    def __init__(self):
        super().__init__()

        self.master.title("Insta Backup")
        self.pack(fill=BOTH, expand=True)
        self.frame = None
        self.label = None
        self.entry = None
        self.button = None
        self.progress = None
        self.ui_form()

    def ui_form(self):
        self.frame = Frame(self)
        self.frame.pack(fill=X)
        
        self.label = Label(self.frame, text='Username:', width=10)
        self.label.pack(fill=X, padx=5, pady=5)

        self.entry = Entry(self.frame)
        self.entry.pack(fill=X, padx=5, pady=5)

        self.button = Button(self.frame, 
                             text='Run', 
                             width=10,
                             command=self.running_task)
        self.button.pack(fill=X, padx=5, pady=5)

        self.progress = Progressbar(self, 
                                    orient=HORIZONTAL,
                                    length=100)
        self.progress.pack(fill=X, padx=5, pady=5)

    def running_task(self):
        _thread.start_new_thread(self.run, ())

    def progress_bar(self, counter, count):
        percentage = (counter / count) * 100
        self.progress['value'] = percentage
        self.master.update_idletasks()

    def run(self):
        username = self.entry.get()
        # disable button
        self.button.configure(state=DISABLED)
        L = instaloader.Instaloader()
        posts = instaloader.Profile.from_username(
            L.context, username
        ).get_posts()
        counter = 1
        for post in posts:
            L.download_post(post, username)
            self.progress_bar(counter, posts.count)
            counter += 1
        
        messagebox.showinfo(
            "Done", 
            "Backup successfully..."
        )
        self.progress['value'] = 0
        self.button.configure(state=ACTIVE)
        self.master.update_idletasks()
    

if __name__ == '__main__':
    root = Tk()
    root.geometry("400x150")
    app = InstaBackup()
    root.mainloop()