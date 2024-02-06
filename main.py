"""
Тестовое задание: На белом поле размером 1024x1024 клеток, в позиции 512,512
находится “муравей” Муравей двигается по следующим правилам:
На белой клетке - поворачивает на 90° по часовой стрелке,инвертирует пиксель и перемещается вперед на одну клетку
На черной клетке - поворачивать на 90° против часовой стрелки, инвертирует пиксель и перемещается вперед на одну клетку
Изначально муравей находится на белой клетке и смотрит вверх.
Пришлите изображение пути муравья до границы поля в виде BMP или PNG файла глубиной цвета 1 бит и
число черных клеток на нем. Программа должна минимизировать использование RAM.
"""
from direction import Direction
from objects import GameField, Ant, Color

FIELD_SIZE = (1024, 1024)

START_ANT_POS = (512, 512)
START_ANT_DIR = Direction.TOP

OUTFILE_NAME = "output.bmp"


field = GameField(*FIELD_SIZE)
ant = Ant(field, *START_ANT_POS, START_ANT_DIR)
while not ant.on_field_end():
    ant.move()

field.save_as_image(OUTFILE_NAME)

white_cells_count = field.get_colored_cells_count(Color.WHITE)
black_cells_count = field.get_colored_cells_count(Color.BLACK)
print(f"Успешно. \n"
      f"Всего белых точек: {white_cells_count}\n"
      f"Всего чёрных точек: {black_cells_count}\n"
      f"Изображение пути муравья сохраненно в {OUTFILE_NAME}")
