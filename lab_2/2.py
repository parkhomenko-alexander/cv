# Рисуем график "задержанного единичного скачка"
# Код сгенерил chatgpt
import numpy as np
import matplotlib.pyplot as plt

m = 2
x = np.arange(0, 10, 1)

# Устанавливаем масштаб по оси x
plt.vlines(x[x >= m], ymin=0, ymax=1, colors='b', linestyles='solid', label='y=1 при x >= m')
plt.vlines(x[x < m], ymin=0, ymax=0, colors='b', linestyles='solid', label='y=0 при x < m')

# Уменьшаем масштаб по оси x в 2 раза
plt.xlim(0, 10 / 2)

# Дополнительные настройки для красоты
plt.xlabel('x')
plt.ylabel('y')
plt.title('График y=1 при x >= m и y=0 при x < m')
plt.legend()
plt.show()


