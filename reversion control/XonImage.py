import tkinter as tk

def draw_x(event):
    x, y = event.x, event.y
    canvas.create_line(x-10, y-10, x+10, y+10, fill="red")
    canvas.create_line(x-10, y+10, x+10, y-10, fill="red")

# Create the main window
root = tk.Tk()

# Load the image
image_path = "images/gimp/PA-Spine.png"
image = tk.PhotoImage(file=image_path)

# Create a canvas widget to display the image
canvas = tk.Canvas(root, width=image.width(), height=image.height())
canvas.create_image(0, 0, image=image, anchor="nw")
canvas.pack()

# Bind the mouse click event to the canvas
canvas.bind("<Button-1>", draw_x)

# Start the main event loop
root.mainloop()
