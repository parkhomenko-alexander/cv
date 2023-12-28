# Рисуем Модель «Белый шум с равномерным распределением»
# Код сгенерил chatgpt

import numpy as np
import matplotlib.pyplot as plt

def generate_white_noise(shape, a=0, b=1):
    """
    Генерация белого шума с равномерным распределением.

    Parameters:
    - shape: размеры изображения (высота, ширина)
    - a, b: параметры равномерного распределения

    Returns:
    - white_noise: массив с белым шумом
    """
    return np.random.uniform(a, b, shape)

def main():
    # Задаем параметры
    rows, cols = 100, 100  # Размеры изображения
    a, b = 0, 1  # Параметры равномерного распределения

    # Генерируем белый шум
    white_noise = generate_white_noise((rows, cols), a, b)

    # Визуализируем белый шум
    plt.imshow(white_noise, cmap='gray', interpolation='nearest')
    plt.colorbar()
    plt.title('Белый шум с равномерным распределением')
    plt.show()

if __name__ == "__main__":
    main()
