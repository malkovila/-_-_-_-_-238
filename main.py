import os
from PIL import Image, ImageFilter, ImageOps
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


# Функция для изменения разрешения изображения
def resize_and_optimize(image, target_size=(1920, 1080), fill_mode='blur'):
    original_width, original_height = image.size

    # Проверка на отбраковку
    if (target_size[0] / original_width) > 2 or (target_size[1] / original_height) > 2:
        return None

    # Изменяем размер изображения с сохранением пропорций
    image.thumbnail(target_size, Image.Resampling.LANCZOS)

    # Создаем задний план (фон)
    background = Image.new('RGB', target_size, (255, 255, 255))

    if fill_mode == 'blur':
        # Создаем размытую копию оригинального изображения для фона
        blurred_bg = image.copy().resize(target_size, Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(30))
        background.paste(blurred_bg)

    elif fill_mode == 'color':
        # Используем однотонный фон
        background = Image.new('RGB', target_size, (202, 131, 205))  # Серый цвет

    # Вставляем изображение по центру на задний план
    img_w, img_h = image.size
    offset = ((target_size[0] - img_w) // 2, (target_size[1] - img_h) // 2)
    background.paste(image, offset)

    return background


# Функция обработки изображений
def process_images(input_folder, output_folder, fill_mode):
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_folder, filename)
            image = Image.open(img_path)

            # Обрабатываем изображение
            result_img = resize_and_optimize(image, fill_mode=fill_mode)
            if result_img:
                # Сохраняем оптимизированное изображение
                output_path = os.path.join(output_folder, filename)
                result_img.save(output_path, optimize=True, quality=85)
            else:
                print(f"Изображение {filename} было отбраковано (слишком малое разрешение).")


# Функция для выбора папок
def select_folder(title):
    return filedialog.askdirectory(title=title)


# Основная функция для GUI
def start_processing():
    input_folder = select_folder("Выберите папку с изображениями")
    if not input_folder:
        return

    output_folder = select_folder("Выберите папку для сохранения результатов")
    if not output_folder:
        return

    fill_mode = fill_mode_var.get()

    process_images(input_folder, output_folder, fill_mode)
    messagebox.showinfo("Готово", "Изображения успешно обработаны и сохранены.")


# Создание GUI
root = tk.Tk()
root.title("Оптимизация изображений")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Выбор метода заполнения краев
ttk.Label(frame, text="Метод заполнения краев:").grid(row=0, column=0, padx=5, pady=5)

fill_mode_var = tk.StringVar(value='blur')
ttk.Radiobutton(frame, text="Размытое изображение", variable=fill_mode_var, value='blur').grid(row=1, column=0, padx=5,
                                                                                               pady=5)
ttk.Radiobutton(frame, text="Цветной фон", variable=fill_mode_var, value='color').grid(row=2, column=0, padx=5, pady=5)

# Кнопка для начала обработки
ttk.Button(frame, text="Начать обработку", command=start_processing).grid(row=3, column=0, padx=5, pady=10)

root.mainloop()
