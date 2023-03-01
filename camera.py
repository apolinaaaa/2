class Camera:
    SPEED_COEFF = 0.1

    # зададим начальный сдвиг камеры
    def __init__(self, width, height, width_map, height_map):
        self.dx = 0
        self.dy = 0
        self.x = width // 2
        self.y = height // 2
        self.observers = []
        self.width_map = width_map
        self.height_map = height_map

    def add(self, observer):
        self.observers.append(observer)

    def add_group(self, group):
        for sprite in group:
            self.add(sprite)

    # сдвинуть объект obj на смещение камеры
    def _apply(self):
        for observer in self.observers:
            observer.move_ip(
                self.dx * self.SPEED_COEFF,
                self.dy * self.SPEED_COEFF,
                self.width_map, self.height_map
            )


    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.x)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.y)
        self._apply()
