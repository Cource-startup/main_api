class Helper:

    @staticmethod
    def to_snake_case(string):
        return ''.join(['_' + c.lower() if c.isupper() else c for c in string]).lstrip('_')
    
    @staticmethod
    def to_camel_case(string):
        return ''.join(word.capitalize() for word in string.split('_'))