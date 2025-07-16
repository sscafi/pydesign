import customtkinter as ctk
from tkinter import colorchooser
import colorsys
import tkinter as tk
from typing import Tuple, Optional

class ColorGenerator:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Color Generator Pro")
        self.root.geometry("650x550")  # Slightly larger window
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure grid weights for better resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.current_color = "#FFFFFF"
        self.create_widgets()
        self.update_color("#FFFFFF")

    def create_widgets(self):
        """Create all GUI widgets with improved layout and organization"""
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        # Left panel (color preview and info)
        left_frame = ctk.CTkFrame(main_frame, width=250)
        left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=False, padx=(0, 10))

        # Right panel (controls)
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=(10, 0))

        self.create_color_preview(left_frame)
        self.create_color_info(left_frame)
        self.create_controls(right_frame)

    def create_color_preview(self, parent):
        """Create the color preview area"""
        preview_frame = ctk.CTkFrame(parent)
        preview_frame.pack(fill=ctk.X, pady=(0, 15))

        self.color_preview = ctk.CTkLabel(
            preview_frame, 
            text="", 
            width=200, 
            height=200,
            corner_radius=15  # Rounded corners
        )
        self.color_preview.pack(pady=10)

    def create_color_info(self, parent):
        """Create color information display and copy buttons"""
        # Color info labels
        info_frame = ctk.CTkFrame(parent)
        info_frame.pack(fill=ctk.X, pady=(0, 15))

        self.hex_label = ctk.CTkLabel(info_frame, text="HEX: #FFFFFF", font=("Arial", 12))
        self.hex_label.pack(anchor="w", pady=2)

        self.rgb_label = ctk.CTkLabel(info_frame, text="RGB: (255, 255, 255)", font=("Arial", 12))
        self.rgb_label.pack(anchor="w", pady=2)

        self.hsl_label = ctk.CTkLabel(info_frame, text="HSL: (0°, 0%, 100%)", font=("Arial", 12))
        self.hsl_label.pack(anchor="w", pady=2)

        # Copy buttons
        copy_frame = ctk.CTkFrame(parent)
        copy_frame.pack(fill=ctk.X, pady=10)

        buttons = [
            ("Copy HEX", "hex"),
            ("Copy RGB", "rgb"),
            ("Copy HSL", "hsl")
        ]

        for text, cmd in buttons:
            btn = ctk.CTkButton(
                copy_frame, 
                text=text, 
                command=lambda c=cmd: self.copy_to_clipboard(c),
                width=70
            )
            btn.pack(side=ctk.LEFT, padx=5, expand=True)

    def create_controls(self, parent):
        """Create control widgets (picker, sliders, palette)"""
        # Color picker button
        self.color_picker = ctk.CTkButton(
            parent, 
            text="🎨 Pick a Color", 
            command=self.pick_color,
            height=35,
            font=("Arial", 12, "bold")
        )
        self.color_picker.pack(fill=ctk.X, pady=(0, 15))

        # Sliders with better labels and value displays
        self.create_slider_with_value(parent, "Hue", 0, 360, self.update_from_sliders)
        self.create_slider_with_value(parent, "Saturation", 0, 100, self.update_from_sliders)
        self.create_slider_with_value(parent, "Brightness", 0, 100, self.update_from_sliders)

        # Color palette with better organization
        self.create_enhanced_color_palette(parent)

    def create_slider_with_value(self, parent, text, from_, to, command):
        """Create slider with value label"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill=ctk.X, pady=5)

        # Label
        ctk.CTkLabel(frame, text=f"{text}:", width=80).pack(side=ctk.LEFT)

        # Slider
        slider = ctk.CTkSlider(
            frame, 
            from_=from_, 
            to=to,
            command=command
        )
        slider.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=(5, 10))

        # Value display
        value_label = ctk.CTkLabel(frame, text="0", width=40)
        value_label.pack(side=ctk.LEFT)

        # Store references
        setattr(self, f"{text.lower()}_slider", slider)
        setattr(self, f"{text.lower()}_value", value_label)

    def create_enhanced_color_palette(self, parent):
        """Create an improved color palette with sections"""
        palette_frame = ctk.CTkFrame(parent)
        palette_frame.pack(fill=ctk.X, pady=15)

        # Section label
        ctk.CTkLabel(palette_frame, text="Color Palette", font=("Arial", 12, "bold")).pack(anchor="w")

        # Primary colors
        primary_frame = ctk.CTkFrame(palette_frame)
        primary_frame.pack(fill=ctk.X, pady=5)
        
        primary_colors = ["#FF0000", "#00FF00", "#0000FF"]
        for color in primary_colors:
            self.create_palette_button(primary_frame, color)

        # Secondary colors
        secondary_frame = ctk.CTkFrame(palette_frame)
        secondary_frame.pack(fill=ctk.X, pady=5)
        
        secondary_colors = ["#FFFF00", "#FF00FF", "#00FFFF"]
        for color in secondary_colors:
            self.create_palette_button(secondary_frame, color)

        # Grayscale
        grayscale_frame = ctk.CTkFrame(palette_frame)
        grayscale_frame.pack(fill=ctk.X, pady=5)
        
        grayscale_colors = ["#FFFFFF", "#808080", "#000000"]
        for color in grayscale_colors:
            self.create_palette_button(grayscale_frame, color)

    def create_palette_button(self, parent, color):
        """Create a palette color button"""
        btn = ctk.CTkButton(
            parent, 
            text="", 
            width=30, 
            height=30, 
            fg_color=color,
            hover_color=color,
            command=lambda c=color: self.update_color(c)
        )
        btn.pack(side=ctk.LEFT, padx=2)

    def pick_color(self):
        """Open color picker dialog"""
        color = colorchooser.askcolor(title="Select Color", parent=self.root)[1]
        if color:
            self.update_color(color)

    def update_color(self, color):
        """Update all elements with the new color"""
        self.current_color = color.upper()
        self.color_preview.configure(fg_color=color)
        
        # Update labels
        rgb = self.hex_to_rgb(color)
        hsl = self.rgb_to_hsl(rgb)
        
        self.hex_label.configure(text=f"HEX: {self.current_color}")
        self.rgb_label.configure(text=f"RGB: {rgb}")
        self.hsl_label.configure(text=f"HSL: {hsl}")

        # Update sliders and their value displays
        h, s, v = self.rgb_to_hsv(rgb)
        
        self.hue_slider.set(h)
        self.saturation_slider.set(s * 100)
        self.brightness_slider.set(v * 100)
        
        self.hue_value.configure(text=f"{int(h)}")
        self.saturation_value.configure(text=f"{int(s * 100)}")
        self.brightness_value.configure(text=f"{int(v * 100)}")

    def update_from_sliders(self, _):
        """Update color based on slider values"""
        h = self.hue_slider.get()
        s = self.saturation_slider.get() / 100
        v = self.brightness_slider.get() / 100
        
        # Update value displays
        self.hue_value.configure(text=f"{int(h)}")
        self.saturation_value.configure(text=f"{int(s * 100)}")
        self.brightness_value.configure(text=f"{int(v * 100)}")
        
        # Convert to RGB and update color
        rgb = colorsys.hsv_to_rgb(h / 360, s, v)
        color = self.rgb_to_hex(tuple(int(x * 255) for x in rgb))
        self.update_color(color)

    def copy_to_clipboard(self, color_format):
        """Copy color value to clipboard"""
        self.root.clipboard_clear()
        
        if color_format == "hex":
            self.root.clipboard_append(self.current_color)
        elif color_format == "rgb":
            rgb = self.hex_to_rgb(self.current_color)
            self.root.clipboard_append(f"rgb{rgb}")
        elif color_format == "hsl":
            rgb = self.hex_to_rgb(self.current_color)
            hsl = self.rgb_to_hsl(rgb)
            self.root.clipboard_append(f"hsl{hsl}")
        
        # Show temporary feedback
        self.show_copy_feedback(color_format)

    def show_copy_feedback(self, color_format):
        """Show temporary feedback when color is copied"""
        feedback = ctk.CTkLabel(
            self.root,
            text=f"{color_format.upper()} copied!",
            fg_color="#2E7D32",  # Green
            text_color="white",
            corner_radius=10
        )
        feedback.place(relx=0.5, rely=0.9, anchor="center")
        feedback.after(1500, feedback.destroy)

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}".upper()

    @staticmethod
    def rgb_to_hsv(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """Convert RGB to HSV (Hue 0-360, Saturation 0-1, Value 0-1)"""
        r, g, b = [x / 255 for x in rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return h * 360, s, v

    @staticmethod
    def rgb_to_hsl(rgb: Tuple[int, int, int]) -> str:
        """Convert RGB to HSL string representation"""
        r, g, b = [x / 255 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return f"({int(h * 360)}°, {int(s * 100)}%, {int(l * 100)}%)"

if __name__ == "__main__":
    app = ColorGenerator()
    app.root.mainloop()
