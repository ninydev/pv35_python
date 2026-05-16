class ColorDecor:
    def __init__ (self, color, func):
        self.color = color
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func()