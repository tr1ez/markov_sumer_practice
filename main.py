import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.image = None  # текущее изображение (numpy array)
        self.photo = None  # для отображения в Tkinter

        # Создание элементов интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Кнопки и поля ввода...
        # (опущено для краткости)
        pass

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
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
        # Конвертация BGR (OpenCV) в RGB для отображения
        img_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil.thumbnail((600, 600))
        self.photo = ImageTk.PhotoImage(img_pil)
        # Отображение на Canvas или Label

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
        self.image = img
        self.show_image()

    def increase_brightness(self, value):
        if self.image is None:
            return
        try:
            delta = int(value)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число")
            return
        # Применяем сложение с клиппингом
        self.image = np.clip(self.image.astype(np.int16) + delta, 0, 255).astype(np.uint8)
        self.show_image()

    def sharpen(self):
        if self.image is None:
            return
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        self.image = cv2.filter2D(self.image, -1, kernel)
        self.show_image()

    def draw_rectangle(self, x1, y1, x2, y2):
        if self.image is None:
            return
        try:
            x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
        except ValueError:
            messagebox.showerror("Ошибка", "Координаты должны быть числами")
            return
        h, w = self.image.shape[:2]
        # Ограничиваем координаты
        x1 = max(0, min(x1, w-1))
        x2 = max(0, min(x2, w-1))
        y1 = max(0, min(y1, h-1))
        y2 = max(0, min(y2, h-1))
        cv2.rectangle(self.image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        self.show_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()