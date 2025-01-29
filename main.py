import customtkinter as ctk
from tkinter import colorchooser
import colorsys

class ColorGenerator:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Color Generator Pro")
        self.root.geometry("600x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_widgets()
        self.current_color = "#FFFFFF"
        self.update_color("#FFFFFF")

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=(0, 10))

        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=(10, 0))

        # Color preview
        self.color_preview = ctk.CTkLabel(left_frame, text="", width=200, height=200)
        self.color_preview.pack(pady=(0, 20))

        # Color information
        self.hex_label = ctk.CTkLabel(left_frame, text="HEX: #FFFFFF")
        self.hex_label.pack(pady=5)

        self.rgb_label = ctk.CTkLabel(left_frame, text="RGB: (255, 255, 255)")
        self.rgb_label.pack(pady=5)

        self.hsl_label = ctk.CTkLabel(left_frame, text="HSL: (0°, 0%, 100%)")
        self.hsl_label.pack(pady=5)

        # Copy buttons
        copy_frame = ctk.CTkFrame(left_frame)
        copy_frame.pack(pady=10)

        ctk.CTkButton(copy_frame, text="Copy HEX", command=lambda: self.copy_to_clipboard("hex")).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(copy_frame, text="Copy RGB", command=lambda: self.copy_to_clipboard("rgb")).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(copy_frame, text="Copy HSL", command=lambda: self.copy_to_clipboard("hsl")).pack(side=ctk.LEFT, padx=5)

        # Color picker button
        self.color_picker = ctk.CTkButton(right_frame, text="Pick a color", command=self.pick_color)
        self.color_picker.pack(pady=(0, 20))

        # Sliders
        self.create_slider(right_frame, "Hue", 0, 360, self.update_from_sliders)
        self.create_slider(right_frame, "Saturation", 0, 100, self.update_from_sliders)
        self.create_slider(right_frame, "Brightness", 0, 100, self.update_from_sliders)

        # Color palette
        palette_frame = ctk.CTkFrame(right_frame)
        palette_frame.pack(pady=20)
        self.create_color_palette(palette_frame)

    def create_slider(self, parent, text, from_, to, command):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill=ctk.X, pady=5)
        ctk.CTkLabel(frame, text=text, width=100).pack(side=ctk.LEFT)
        slider = ctk.CTkSlider(frame, from_=from_, to=to, command=command)
        slider.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=(10, 0))
        setattr(self, f"{text.lower()}_slider", slider)

    def create_color_palette(self, parent):
        colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
        for color in colors:
            ctk.CTkButton(parent, text="", width=30, height=30, fg_color=color, command=lambda c=color: self.update_color(c)).pack(side=ctk.LEFT, padx=2)

    def pick_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.update_color(color)

    def update_color(self, color):
        self.current_color = color
        self.color_preview.configure(fg_color=color)
        
        # Update labels
        self.hex_label.configure(text=f"HEX: {color.upper()}")
        rgb = self.hex_to_rgb(color)
        self.rgb_label.configure(text=f"RGB: {rgb}")
        hsl = self.rgb_to_hsl(rgb)
        self.hsl_label.configure(text=f"HSL: {hsl}")

        # Update sliders
        h, s, v = self.rgb_to_hsv(rgb)
        self.hue_slider.set(h)
        self.saturation_slider.set(s * 100)
        self.brightness_slider.set(v * 100)

    def update_from_sliders(self, _):
        h = self.hue_slider.get()
        s = self.saturation_slider.get() / 100
        v = self.brightness_slider.get() / 100
        rgb = colorsys.hsv_to_rgb(h / 360, s, v)
        color = self.rgb_to_hex(tuple(int(x * 255) for x in rgb))
        self.update_color(color)

    def copy_to_clipboard(self, color_format):
        if color_format == "hex":
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_color.upper())
        elif color_format == "rgb":
            rgb = self.hex_to_rgb(self.current_color)
            self.root.clipboard_clear()
            self.root.clipboard_append(f"rgb{rgb}")
        elif color_format == "hsl":
            rgb = self.hex_to_rgb(self.current_color)
            hsl = self.rgb_to_hsl(rgb)
            self.root.clipboard_clear()
            self.root.clipboard_append(f"hsl{hsl}")

    @staticmethod
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def rgb_to_hex(rgb):
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    @staticmethod
    def rgb_to_hsv(rgb):
        r, g, b = [x / 255 for x in rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return h * 360, s, v

    @staticmethod
    def rgb_to_hsl(rgb):
        r, g, b = [x / 255 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return f"({int(h * 360)}°, {int(s * 100)}%, {int(l * 100)}%)"

if __name__ == "__main__":
    app = ColorGenerator()
    app.root.mainloop()

