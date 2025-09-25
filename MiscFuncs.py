class File:
    @staticmethod
    def Create(filepath, content=''):
        with open(filepath, 'x') as f:
            f.write(content)

    @staticmethod
    def Append(filepath, content):
        with open(filepath, 'a') as f:
            f.write(content)

    @staticmethod
    def Overwrite(filepath, content):
        with open(filepath, 'w') as f:
            f.write(content)

    @staticmethod
    def Read(filepath):
        with open(filepath, 'r') as f:
            return f.read()
