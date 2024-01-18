import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

m = 2
x = np.arange(0, 10, 1)

# Рисуем график для y=1 при x >= m
plt.fill_between(x, 0, 1, where=(x >= m), color='b', alpha=0.3, label='y=1 при x >= {}'.format(m))

# Рисуем график для y=0 при x < m
plt.fill_between(x, 0, 0, where=(x < m), color='b', alpha=0.1, label='y=0 при x < {}'.format(m))

# Получаем размеры графика по обеим осям
x_half_size = (plt.xlim()[1] - plt.xlim()[0]) / 2
y_half_size = (plt.ylim()[1] - plt.ylim()[0]) / 2

# Смещаем начало координат в центр графика
plt.xlim(-x_half_size, x_half_size)
plt.ylim(-y_half_size, y_half_size)

# Нарисовать оси x и y через центр графика
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)

# Дополнительные настройки для красоты
plt.xlabel('x')
plt.ylabel('y')
plt.title('График y=1 при x >= {} и y=0 при x < {}'.format(m, m))
plt.legend()

# Создаем папку "screens", если ее нет
screens_folder = "screens"
os.makedirs(screens_folder, exist_ok=True)

# Сохраняем изображение в папку "screens"
fig = plt.gcf()
fig.canvas.draw()
data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
img = Image.fromarray(data)

img_path = os.path.join(screens_folder, "graph_image2.png")
img.save(img_path)
print(f"График сохранен в {img_path}")
plt.show()