import os
import numpy as np
from PIL import Image
import pymysql

# Вказуємо шлях до папки з зображеннями на диску E
images_folder = "E:/Blood_Vessels_Images"
output_folder = "E:/Blood_Vessels_FractalImages"

# Отримуємо список усіх зображень у папці
image_files = [f for f in os.listdir(images_folder) if f.endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]

# Перевіряємо, чи є зображення в папці
if len(image_files) == 0:
    print("У папці немає зображень.")
    exit()

# Виводимо список зображень та даємо можливість вибору
print("Доступні зображення:")
for i, image_file in enumerate(image_files):
    print(f"{i + 1}. {image_file}")

# Запитуємо у користувача вибір зображення
while True:
    try:
        selected_index = int(input("Виберіть зображення за номером (1, 2, 3, ...): ")) - 1
        if 0 <= selected_index < len(image_files):
            selected_image_file = image_files[selected_index]
            break
        else:
            print("Невірний номер. Спробуйте ще раз.")
    except ValueError:
        print("Будь ласка, введіть коректний номер.")

# Відкриваємо зображення
image_path = os.path.join(images_folder, selected_image_file)
image = Image.open(image_path).convert('L')  # Перетворюємо в чорно-біле зображення

# Виводимо інформацію про вибране зображення
print(f"Вибрано зображення: {selected_image_file}")

# Перетворюємо зображення в масив numpy
image_array = np.array(image)

# Функція генерації фрактала Мандельброта
def mandelbrot(c, max_iter=1000):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return max_iter

# Розміри зображення
height, width = image_array.shape

# Створення порожнього масиву для фрактального зображення
fractal_image = np.zeros((height, width))

# Проходимо по кожному пікселю зображення і генеруємо відповідний фрактал
for y in range(height):
    for x in range(width):
        # Мапуємо значення пікселя в комплексне число
        c = complex((x - width / 2) / (width / 4), (y - height / 2) / (height / 4))
        fractal_value = mandelbrot(c)
        # Присвоюємо значення фрактала відповідно до інтенсивності пікселя
        fractal_image[y, x] = fractal_value

# Нормалізація значень для відображення
fractal_image = Image.fromarray(np.uint8(fractal_image / fractal_image.max() * 255))

# Зберігаємо фрактальне зображення в папку
output_path = os.path.join(output_folder, f"fractal_{selected_image_file}")
fractal_image.save(output_path)

# Виведення фрактального зображення
fractal_image.show()

# Функція адаптивної бінаризації
def adaptive_threshold(image, block_size=15, offset=10):
    # Створюємо масив для бінаризованого зображення
    binary_image = np.zeros_like(image)
    
    # Встановлюємо поріг для кожного блоку
    for i in range(0, image.shape[0], block_size):
        for j in range(0, image.shape[1], block_size):
            # Визначаємо межі блоку
            block = image[i:i+block_size, j:j+block_size]
            
            # Обчислюємо середнє значення блоку
            block_mean = np.mean(block)
            
            # Встановлюємо поріг для цього блоку
            threshold = block_mean - offset
            
            # Бінаризуємо блок
            binary_image[i:i+block_size, j:j+block_size] = (block > threshold).astype(int)
    
    return binary_image

# Застосовуємо адаптивну бінаризацію
binary_image = adaptive_threshold(image_array)

# Перетворюємо бінаризоване зображення в формат PIL для збереження
binary_image_pil = Image.fromarray(binary_image * 255)  # Перетворюємо 0-1 в 0-255

# Зберігаємо бінаризоване зображення
binary_output_path = os.path.join(output_folder, f"binary_{selected_image_file}")
binary_image_pil.save(binary_output_path)

# Розрахунок площі покриття судинами
covered_pixels = np.sum(binary_image == 1)  # Рахуємо пікселі, що належать до судин
total_pixels = binary_image.size  # Загальна кількість пікселів
coverage_percentage = (covered_pixels / total_pixels) * 100  # Площа покриття в відсотках

# Округлення значень площі покриття
covered_pixels = round(covered_pixels, 2)
coverage_percentage = round(coverage_percentage, 2)

# Виведення результатів
print(f"Площа покриття судинами: {covered_pixels} пікселів ({coverage_percentage:.2f}%)")

# Фрактальна розмірність
def box_count(image, box_size):
    # Функція для підрахунку кількості коробок (box count)
    count = 0
    for y in range(0, image.shape[0], box_size):
        for x in range(0, image.shape[1], box_size):
            if np.sum(image[y:y+box_size, x:x+box_size]) > 0:
                count += 1
    return count

# Розрахунок фрактальної розмірності
sizes = []
counts = []
for box_size in range(1, min(image_array.shape) // 2, 2):
    count = box_count(binary_image, box_size)
    sizes.append(box_size)
    counts.append(count)

# Лінійна регресія для визначення фрактальної розмірності
sizes = np.array(sizes)
counts = np.array(counts)
log_sizes = np.log(sizes)
log_counts = np.log(counts)

# Пошук коефіцієнтів лінійної регресії
slope, intercept = np.polyfit(log_sizes, log_counts, 1)
fractal_dimension = -slope

# Округлення фрактальної розмірності
fractal_dimension = round(fractal_dimension, 2)

print(f"Фрактальна розмірність: {fractal_dimension:.2f}")

# Підключення до бази даних
db_config = {
    "host": "localhost",
    "user": "root",  # Змініть на вашого користувача
    "password": "orbita1o",  # Вставте ваш пароль
    "database": "blood_vessel_diseases"  # Назва бази даних
}

try:
    # Підключення до бази даних
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # Запит для отримання даних з таблиці діагнозів
    query = "SELECT disease_name, fractal_dimension_min, fractal_dimension_max FROM DISEASES;"
    cursor.execute(query)
    diagnoses = cursor.fetchall()

    # Перевірка фрактальної розмірності
    diagnosis_result = None
    for disease_name, min_dim, max_dim in diagnoses:
        # Округлюємо значення для порівняння
        min_dim = round(min_dim, 2)
        max_dim = round(max_dim, 2)
        
        if min_dim <= fractal_dimension <= max_dim:
            diagnosis_result = disease_name
            break

    # Виведення результату
    if diagnosis_result:
        print(f"Ваш результат: {fractal_dimension:.2f}. Ймовірний діагноз: {diagnosis_result}.")
    else:
        print(f"Ваш результат: {fractal_dimension:.2f}. Діапазон не визначено.")

except pymysql.MySQLError as e:
    print("Помилка підключення до бази даних:", e)

finally:
    # Закриття з'єднання
    if 'connection' in locals() and connection.open:
        connection.close()

# Зберігаємо результати
result = {
    "coverage_pixels": covered_pixels,
    "coverage_percentage": coverage_percentage,
    "fractal_dimension": fractal_dimension
}

print(result)
