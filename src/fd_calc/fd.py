class FD:
    left_side:tuple
    right_side:list
    unique:bool
    def __init__(self, left_side, right_side, unique):
        self.left_side=left_side
        self.right_side=right_side
        self.unique=unique

    def to_string(self):
        return f"{self.left_side} -> {self.right_side}    ({"unique" if self.unique else "repeating"})"