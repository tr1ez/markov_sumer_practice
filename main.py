import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.image = None
        self.photo = None

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.LabelFrame(main_frame, text="Управление", padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        ttk.Button(control_frame, text="Загрузить изображение", command=self.load_image).pack(fill=tk.X, pady=2)
        ttk.Button(control_frame, text="Снимок с камеры", command=self.capture_from_camera).pack(fill=tk.X, pady=2)

        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=5)

        ttk.Label(control_frame, text="Показать канал:").pack(anchor=tk.W, pady=(5,0))
        channel_frame = ttk.Frame(control_frame)
        channel_frame.pack(fill=tk.X, pady=2)
        ttk.Button(channel_frame, text="R", command=lambda: self.show_channel('R')).pack(side=tk.LEFT, padx=2)
        ttk.Button(channel_frame, text="G", command=lambda: self.show_channel('G')).pack(side=tk.LEFT, padx=2)
        ttk.Button(channel_frame, text="B", command=lambda: self.show_channel('B')).pack(side=tk.LEFT, padx=2)

        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=5)

        ttk.Label(control_frame, text="Изменение яркости:").pack(anchor=tk.W, pady=(5,0))
        brightness_frame = ttk.Frame(control_frame)
        brightness_frame.pack(fill=tk.X, pady=2)
        self.brightness_entry = ttk.Entry(brightness_frame, width=10)
        self.brightness_entry.pack(side=tk.LEFT, padx=(0,5))
        self.brightness_entry.insert(0, "30")
        ttk.Button(brightness_frame, text="Применить", 
                   command=lambda: self.increase_brightness(self.brightness_entry.get())).pack(side=tk.LEFT)

        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=5)

        ttk.Button(control_frame, text="Увеличить резкость", command=self.sharpen).pack(fill=tk.X, pady=2)

        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=5)

        ttk.Label(control_frame, text="Координаты прямоугольника:").pack(anchor=tk.W, pady=(5, 0))
        coord_frame = ttk.Frame(control_frame)
        coord_frame.pack(fill=tk.X, pady=2)
        ttk.Label(coord_frame, text="x1:").pack(side=tk.LEFT)
        self.x1_entry = ttk.Entry(coord_frame, width=5)
        self.x1_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.x1_entry.insert(0, "50")
        ttk.Label(coord_frame, text="y1:").pack(side=tk.LEFT)
        self.y1_entry = ttk.Entry(coord_frame, width=5)
        self.y1_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(coord_frame, text="x2:").pack(side=tk.LEFT)
        self.x2_entry = ttk.Entry(coord_frame, width=5)
        self.x2_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(coord_frame, text="y2:").pack(side=tk.LEFT)
        self.y2_entry = ttk.Entry(coord_frame, width=5)
        self.y2_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(coord_frame, text="Нарисовать", 
                   command=self.draw_rectangle_from_entries).pack(side=tk.LEFT, padx=(5, 0))

        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=5)

        self.image_label = ttk.Label(main_frame, relief=tk.SUNKEN, anchor=tk.CENTER, background='#f0f0f0')
        self.image_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.image_label.config(text="Загрузите изображение или сделайте снимок")

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        )
        if file_path:
            self.image = cv2.imread(file_path)
            if self.image is None:
                messagebox.showerror("Ошибка", "Не удалось загрузить изображение")
            else:
                self.show_image()

    def capture_from_camera(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Ошибка", "Не удалось подключиться к веб-камере")
            return
        ret, frame = cap.read()
        cap.release()
        if ret:
            self.image = frame
            self.show_image()
        else:
            messagebox.showerror("Ошибка", "Не удалось сделать снимок")

    def show_image(self):
        if self.image is None:
            self.image_label.config(image='', text="Изображение не загружено")
            self.photo = None
            return

        img_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)

        display_size = (600, 600)
        img_pil.thumbnail(display_size, Image.LANCZOS)

        self.photo = ImageTk.PhotoImage(img_pil)
        self.image_label.config(image=self.photo, text='')
        self.image_label.image = self.photo

    def show_channel(self, channel):
        if self.image is None:
            messagebox.showwarning("Предупреждение", "Изображение не загружено")
            return
        b, g, r = cv2.split(self.image)
        if channel == 'R':
            img = cv2.merge([np.zeros_like(b), np.zeros_like(g), r])
        elif channel == 'G':
            img = cv2.merge([np.zeros_like(b), g, np.zeros_like(r)])
        elif channel == 'B':
            img = cv2.merge([b, np.zeros_like(g), np.zeros_like(r)])
        else:
            return
        self.image = img
        self.show_image()

    def increase_brightness(self, value):
        if self.image is None:
            messagebox.showwarning("Предупреждение", "Изображение не загружено")
            return
        try:
            delta = int(value)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число")
            return
        self.image = np.clip(self.image.astype(np.int16) + delta, 0, 255).astype(np.uint8)
        self.show_image()

    def sharpen(self):
        if self.image is None:
            messagebox.showwarning("Предупреждение", "Изображение не загружено")
            return
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        self.image = cv2.filter2D(self.image, -1, kernel)
        self.show_image()

    def draw_rectangle_from_entries(self):
        if self.image is None:
            messagebox.showwarning("Предупреждение", "Изображение не загружено")
            return
        try:
            x1 = int(self.x1_entry.get())
            y1 = int(self.y1_entry.get())
            x2 = int(self.x2_entry.get())
            y2 = int(self.y2_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Все координаты должны быть целыми числами")
            return
        self.draw_rectangle(x1, y1, x2, y2)

    def draw_rectangle(self, x1, y1, x2, y2):
        h, w = self.image.shape[:2]
        x1 = max(0, min(x1, w - 1))
        x2 = max(0, min(x2, w - 1))
        y1 = max(0, min(y1, h - 1))
        y2 = max(0, min(y2, h - 1))
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        cv2.rectangle(self.image, (x1, y1), (x2, y2), (255, 0, 0), -1)
        self.show_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()