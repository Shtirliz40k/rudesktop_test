import enum
from PIL import Image

from direction import Direction, CLOCKWISE_ROTATION, COUNTER_CLOCKWISE_ROTATION


class Color(enum.Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


class GameField:

    def __init__(self, size_x, size_y):
        # Заполняем поле белыми клетками
        # Правила начального заполнения поля можно было бы вынести отдельно,
        # однако условия задачи этого не требуют, поэтому сделаем как проще
        self._field = [[Color.WHITE for _ in range(size_x)] for __ in range(size_y)]
        self.size_x = size_x
        self.size_y = size_y

    def get_color(self, x, y):
        return self._field[x][y]

    def invert_color(self, x, y):
        current_color = self._field[x][y]
        if current_color == Color.BLACK:
            self._field[x][y] = Color.WHITE
        elif current_color == Color.WHITE:
            self._field[x][y] = Color.BLACK

    def get_colored_cells_count(self, color: Color):
        """
        Возвращает количество точек данного цвета
        """
        count = 0
        for l in self._field:
            for cell in l:
                if cell == color:
                    count += 1

        return count

    def save_as_image(self, filename):
        """
        В этом месте будет относительно высокое потребление памяти, т.к. изображение хранится в памяти "дважды"
        в разных форматах. Эта проблема могла бы быть решена путём потоковой записи на диск, чанками.

        Я не нашёл как это сделать в pillow. Громоздить свою реализацию записи bmp файла так же не хотелось.
        Поэтому пропустил.
        """
        img = Image.new('RGB', (self.size_x, self.size_y))
        pixels = img.load()

        for i in range(len(self._field)):
            for j in range(len(self._field[i])):
                pixels[i, j] = self._field[i][j].value

        img.save(filename)
        import time
        time.sleep(3)


class Ant:

    def __init__(self, game_field: GameField, pos_x, pos_y, direction: Direction):
        self._field = game_field

        self.x = pos_x
        self.y = pos_y
        self.direction = direction

    def _rotate_clockwise(self):
        self.direction = CLOCKWISE_ROTATION[self.direction]

    def _rotate_counterclockwise(self):
        self.direction = COUNTER_CLOCKWISE_ROTATION[self.direction]

    def _move_forward(self):
        if self.direction == Direction.TOP:
            self.y -= 1
        elif self.direction == Direction.RIGHT:
            self.x += 1
        elif self.direction == Direction.BOTTOM:
            self.y += 1
        elif self.direction == Direction.LEFT:
            self.x -= 1

        if self.x >= self._field.size_x or \
                self.x < 0 or \
                self.y >= self._field.size_y or \
                self.y < 0:
            # В случае выхода за границу поля - выбрасываем ошибку
            # Обработка таких ситуаций - не задача данного класса
            raise RuntimeError(f"Moving outside a field! \n X: {self.x}, Y: {self.y}")

    def move(self):
        if self._field.get_color(self.x, self.y) == Color.WHITE:
            self._rotate_clockwise()
            self._field.invert_color(self.x, self.y)
            self._move_forward()
        elif self._field.get_color(self.x, self.y) == Color.BLACK:
            self._rotate_counterclockwise()
            self._field.invert_color(self.x, self.y)
            self._move_forward()

    def on_field_end(self):
        """
        Проверяет, находится ли муравей на краю поля

        По условию задачи не уверен, что есть "путь муравья до границы поля",
        Вижу 2 варианта:
            - Муравей стоит на крайней клетке поля, но не вышел за границу,
                направление и возможность следующего хода не учитывается
            - Выход за границу является концом пути

        Предпологаю вариант 1, и работаю с ним
        """
        return (self.x == self._field.size_x - 1 or
                self.y == self._field.size_y - 1 or
                self.x == 0 or
                self.y == 0)
