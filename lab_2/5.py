# Рисуем «Шахматная доска»
# Код сгенерил chatgpt
from PIL import Image, ImageDraw

def create_chessboard(rows, cell_size):
    # Размеры доски в пикселях
    width = rows * cell_size
    height = rows * cell_size

    # Создаем новое изображение
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Заполняем доску черными и белыми клетками
    for i in range(rows):
        for j in range(rows):
            x = j * cell_size
            y = i * cell_size
            color = "black" if (i + j) % 2 == 1 else "white"
            draw.rectangle([x, y, x + cell_size, y + cell_size], fill=color)

    return image

def main():
    # Задаем количество клеток и размер клетки
    rows = int(input("Введите количество клеток в одном ряду: "))
    cell_size = int(input("Введите размер клетки в пикселах: "))

    # Создаем шахматную доску
    chessboard = create_chessboard(rows, cell_size)

    # Показываем изображение
    chessboard.show()

   
if __name__ == "__main__":
    main()
