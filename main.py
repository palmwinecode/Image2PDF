import tkinter as tk
from tkinter import ttk, filedialog
from reportlab.pdfgen import canvas
from PIL import Image

import os

class Image2PDFConverter:

    def __init__(self, root) -> None:
        # Create instance variables
        self.root = root
 
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)

        # Initilize UI
        self.initialize_ui()

    def initialize_ui(self) -> None:
        # Add title
        title_label = tk.Label(self.root, text="Image to PDF Converter", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Add button to select images
        select_images_button = tk.Button(self.root, text="Select Images", command=self.select_images)
        select_images_button.pack(pady=(0, 10))

        # Add listbox to display selected images
        self.selected_images_listbox.pack(padx=50, pady=(0, 10), fill=tk.BOTH, expand=True)

        # Add label for output name field
        label = tk.Label(self.root, text="Enter output PDF name:")
        label.pack()

        # Add entry for output name field
        pdf_name_entry = tk.Entry(self.root ,textvariable=self.output_pdf_name, width=40, justify="center")
        pdf_name_entry.pack()

        # Add button to convert selected images to PDF
        convert_button = tk.Button(self.root, text="Convert to PDF", command=self.convert_images_to_pdf)
        convert_button.pack(pady=(20, 40))

    # Function to select images
    def select_images(self) -> None:
        # Get selected images
        self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        # Call function to update listbox
        self.update_selected_images_listbox()

    # Function to update listbox
    def update_selected_images_listbox(self):
        # Clear listbox
        self.selected_images_listbox.delete(0, tk.END)

        # Add selected images to listbox
        for image_path in self.image_paths:
            # Split file names from full file path
            _, image_path = os.path.split(image_path)

            # Insert filename in listbox
            self.selected_images_listbox.insert(tk.END, image_path)

    # Function to convert selected images to PDF
    def convert_images_to_pdf(self) -> None:
        # Check if user selected images
        if not self.image_paths:
            return
        
        # Get output name from user, if no input from user save as "Output.pdf"
        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "Output.pdf"

        # Create a PDF canvas object
        pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792))

        # Loop thorugh selected images
        for image_path in self.image_paths:
            # Open image
            img = Image.open(image_path)

            # Set available size 
            available_width: int = 540
            available_height: int = 720

            # Determine scale factor
            scale_factor: float = min(available_width / img.width, available_height / img.height)

            # Apply scale factor
            new_width: float = img.width * scale_factor
            new_height: float = img.height * scale_factor

            # Center images in file
            x_centered: float = (612 - new_width) / 2
            y_centered: float = (792 - new_height) / 2

            # Fill with white background
            pdf.setFillColorRGB(255, 255, 255)
            pdf.rect(0, 0, 612, 792, fill=True)
            pdf.drawInlineImage(img, x_centered, y_centered, width=new_width, height=new_height)

            # Move to next page
            pdf.showPage()

        # Save pdf
        pdf.save()

def main():
    # Initialize top level Tk window
    root = tk.Tk()

    # Add window title
    root.title("Image to PDF")

    # Set window default size
    root.geometry("500x600")

    # Make window non-resizable
    root.resizable(False, False)

    # Instantiate converter class
    Image2PDFConverter(root)

    # Run main event loop
    root.mainloop()

if __name__ == "__main__":
    main()