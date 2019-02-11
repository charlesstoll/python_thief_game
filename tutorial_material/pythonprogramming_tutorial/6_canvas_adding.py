from Tkinter import *
from PIL import Image, ImageTk

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("MY_GUIIII")
        self.pack(fill=BOTH, expand=1)
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)
        edit = Menu(menu)
        edit.add_command(label="Clear", command = self.clear_frame)
        edit.add_command(label="Show Img", command = self.show_img)
        edit.add_command(label="Show Text", command = self.show_text)
        edit.add_command(label="Draw Lines", command = self.draw_lines)
        menu.add_cascade(label="Edit", menu=edit)

        canvas = Canvas(self)
        self.canvas = canvas

    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def client_exit(self):
        exit()

    def show_img(self):
        load = Image.open("mario.png")
        render = ImageTk.PhotoImage(load)

        img = Label(self, image = render)
        img.image = render
        img.place(x=0, y=0)

    def show_text(self):
        text = Label(self, text="Hey there!!")
        text.pack()

    def draw_lines(self):
        self.canvas.create_line(15, 25, 200, 25)
        self.canvas.create_line(300, 35, 300, 200, dash=(4, 2))
        self.canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)
        self.canvas.pack(fill=BOTH, expand=1)

root = Tk()
root.geometry("400x300")
app = Window(root)
root.mainloop()
