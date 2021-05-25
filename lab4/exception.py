class CompileError(Exception):
    def __init__(self, message="Compile error"):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return self.message