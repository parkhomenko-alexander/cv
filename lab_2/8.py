import numpy as np
import matplotlib.pyplot as plt
import os

def generate_white_noise(shape, a=0, b=1, num_frames=1):
    """
    Генерация белого шума с равномерным распределением для каждого момента времени t.

    Parameters:
    - shape: размеры изображения (высота, ширина)
    - a, b: параметры равномерного распределения
    - num_frames: количество моментов времени

    Returns:
    - white_noise: массив с белым шумом (время, высота, ширина)
    """
    return np.random.uniform(a, b, (num_frames,) + shape) * 255

def main():
    # Задаем параметры
    rows, cols = 100, 100  # Размеры изображения
    a, b = float(input("Введите значение a: ")), float(input("Введите значение b: "))  # Параметры равномерного распределения
    num_frames = 10  # Количество моментов времени

    # Генерируем белый шум для каждого момента времени t
    white_noise = generate_white_noise((rows, cols), a, b, num_frames)

    # Визуализируем белый шум для первого момента времени
    plt.imshow(white_noise[0], cmap='gray', interpolation='nearest')
    plt.colorbar()
    plt.title('Белый шум для t=0')

    # Создаем папку "screens", если ее нет
    screens_folder = "screens"
    os.makedirs(screens_folder, exist_ok=True)

    # Сохраняем изображение в папку "screens"
    image_path = os.path.join(screens_folder, f"white_noise_image_t0_a{a}_b{b}.png")
    plt.savefig(image_path)

    plt.show()

if __name__ == "__main__":
    main()
