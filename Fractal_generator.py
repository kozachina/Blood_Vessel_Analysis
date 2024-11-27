import matplotlib
matplotlib.use('Agg')  # Використовуємо безпечний бекенд, що не потребує графічного інтерфейсу

import numpy as np
import matplotlib.pyplot as plt

# Розміри зображення
width, height = 800, 800
# Обмеження на координати
x_min, x_max = -2, 2
y_min, y_max = -2, 2

# Генерація фрактала Мандельброта
def mandelbrot(c, max_iter=256):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

# Створення зображення
image = np.zeros((height, width))
for x in range(width):
    for y in range(height):
        c = complex(x_min + (x / width) * (x_max - x_min), 
                    y_min + (y / height) * (y_max - y_min))
        image[y, x] = mandelbrot(c)

# Візуалізація
plt.imshow(image, cmap="inferno", extent=(x_min, x_max, y_min, y_max))
plt.colorbar()
plt.title("Фрактал Мандельброта")

# Збереження зображення без відкриття вікна
plt.savefig("mandelbrot_fractal.png")
