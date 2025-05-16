import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

class ImageComparer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Comparison Viewer")

        self.canvas1 = tk.Label(root)
        self.canvas1.grid(row=0, column=0)

        self.canvas2 = tk.Label(root)
        self.canvas2.grid(row=0, column=1)

        self.btn_prev = tk.Button(root, text="← Prev", command=self.prev_image)
        self.btn_prev.grid(row=1, column=0, sticky='ew')

        self.btn_next = tk.Button(root, text="Next →", command=self.next_image)
        self.btn_next.grid(row=1, column=1, sticky='ew')

        self.btn_save = tk.Button(root, text="Save Screenshot", command=self.save_screenshot)
        self.btn_save.grid(row=2, column=0, columnspan=2, sticky='ew')

        self.index = 0
        self.folder1 = filedialog.askdirectory(title="Select Folder 1 (e.g. GOP frames)")
        self.folder2 = filedialog.askdirectory(title="Select Folder 2 (e.g. I frames)")

        self.folder1_name = os.path.basename(self.folder1.rstrip("/\\"))
        self.folder2_name = os.path.basename(self.folder2.rstrip("/\\"))
        self.output_dir = os.path.join("comparisons", f"{self.folder1_name}_vs_{self.folder2_name}")
        os.makedirs(self.output_dir, exist_ok=True)

        self.images1 = sorted([f for f in os.listdir(self.folder1) if f.lower().endswith(('.jpg', '.jpeg', '.tif', '.tiff'))])
        self.images2 = sorted([f for f in os.listdir(self.folder2) if f.lower().endswith(('.jpg', '.jpeg', '.tif', '.tiff'))])
        
        self.root.bind("<Right>", lambda e: self.next_image())
        self.root.bind("<Left>", lambda e: self.prev_image())

        self.show_images()

    def show_images(self):
        if self.index < 0 or self.index >= len(self.images1):
            return

        img1_path = os.path.join(self.folder1, self.images1[self.index])
        img2_path = os.path.join(self.folder2, self.images2[self.index])

        img1 = Image.open(img1_path).convert("RGB")
        img2 = Image.open(img2_path).convert("RGB")

        img1 = img1.resize((400, 400))
        img2 = img2.resize((400, 400))

        self.tk_img1 = ImageTk.PhotoImage(img1)
        self.tk_img2 = ImageTk.PhotoImage(img2)

        self.canvas1.config(image=self.tk_img1)
        self.canvas2.config(image=self.tk_img2)

        self.root.title(f"{self.images1[self.index]} vs {self.images2[self.index]}")

    def next_image(self):
        if self.index < len(self.images1) - 1:
            self.index += 1
            self.show_images()

    def prev_image(self):
        if self.index > 0:
            self.index -= 1
            self.show_images()

    def save_screenshot(self):
        img1_path = os.path.join(self.folder1, self.images1[self.index])
        img2_path = os.path.join(self.folder2, self.images2[self.index])

        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)

        if img1 is None or img2 is None:
            print("Error loading image(s). Skipping screenshot.")
            return

        img1 = cv2.resize(img1, (400, 400))
        img2 = cv2.resize(img2, (400, 400))

        combined = cv2.hconcat([img1, img2])

        filename = f"{self.folder1_name}_vs_{self.folder2_name}_{self.index:03d}.png"
        save_path = os.path.join(self.output_dir, filename)
        cv2.imwrite(save_path, combined)
        print(f"Saved screenshot: {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    viewer = ImageComparer(root)
    root.mainloop()
