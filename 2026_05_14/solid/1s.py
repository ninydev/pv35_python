# 1. S — Single Responsibility Principle

# class Report:
#     def __init__(self, data):
#         self.data = data
#
#     def generate(self):
#         return f"Отчет: {self.data}"
#
#     def save_to_file(self, filename):
#         # Если мы захотим сохранять в БД, а не в файл, нам придется менять этот класс
#         with open(filename, 'w') as f:
#             f.write(self.generate())


class Report:
    def __init__(self, data):
        self.data = data

    def generate(self):
        return f"Отчет: {self.data}"


class ReportSaver:
    @staticmethod
    def save_to_file(report, filename):
        with open(filename, 'w') as f:
            f.write(report.generate())