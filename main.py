import tkinter as tk
from tkinter import colorchooser

class ColorGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Color Generator")
        self.master.geometry("400x300")

        # Create color picker
        self.color_picker = tk.Button(master, text="Pick a color", command=self.pick_color)
        self.color_picker.pack()

        # Create hue slider
        self.hue_slider = tk.Scale(master, from_=0, to=360, orient=tk.HORIZONTAL)
        self.hue_slider.pack()

        # Create saturation slider
        self.saturation_slider = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL)
        self.saturation_slider.pack()

        # Create brightness slider
        self.brightness_slider = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL)
        self.brightness_slider.pack()

        # Create color preview
        self.color_preview = tk.Label(master, width=20, height=10, bg="white")
        self.color_preview.pack()

        # Create RGB code display
        self.rgb_code_display = tk.Label(master, text="RGB: (0, 0, 0)")
        self.rgb_code_display.pack()

    def pick_color(self):
        color = colorchooser.askcolor()[1]
        self.update_color_preview(color)

    def update_color_preview(self, color):
        # Convert color to HSB values
        hsb = self.rgb_to_hsb(color)
        self.hue_slider.set(hsb[0])
        self.saturation_slider.set(hsb[1])
        self.brightness_slider.set(hsb[2])

        # Update color preview
        self.color_preview.config(bg=color)

        # Update RGB code display
        self.rgb_code_display.config(text=f"RGB: {color}")

    def rgb_to_hsb(self, rgb):
        r, g, b = self.hex_to_rgb(rgb)
        r /= 255
        g /= 255
        b /= 255

        max_c = max(r, g, b)
        min_c = min(r, g, b)
        delta = max_c - min_c

        if delta == 0:
            h = 0
        elif max_c == r:
            h = (g - b) / delta
        elif max_c == g:
            h = 2 + (b - r) / delta
        else:
            h = 4 + (r - g) / delta

        h *= 60
        if h < 0:
            h += 360

        s = delta / max_c
        v = max_c

        return h, s * 100, v * 100

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

root = tk.Tk()
color_generator = ColorGenerator(root)
root.mainloop()