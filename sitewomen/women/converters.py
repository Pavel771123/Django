# converters.py
class FourDigityearConverter:
    regex = r'\d{4}'  # Соответствует четырёхзначному году

    def to_python(self, value):
        # Преобразует строку в число
        return int(value)

    def to_url(self, value):
        # Преобразует число в строку для использования в URL
        return str(value)
