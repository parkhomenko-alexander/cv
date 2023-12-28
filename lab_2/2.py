# Рисуем график "задержанного единичного скачка"
# Код сгенерил chatgpt
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

m = 2
x = np.arange(0, 10, 1)

# Устанавливаем масштаб по оси x
plt.vlines(x[x >= m], ymin=0, ymax=1, colors='b', linestyles='solid', label='y=1 при x >= {}'.format(m))
plt.vlines(x[x < m], ymin=0, ymax=0, colors='b', linestyles='solid', label='y=0 при x < {}'.format(m))

# Уменьшаем масштаб по оси x в 2 раза
plt.xlim(0, 10 / 2)

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