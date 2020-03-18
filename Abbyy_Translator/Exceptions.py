class DBNotFoundException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return f'DBNotFoundException, {self.message}'
        else:
            return 'DBNotFoundException has been raised'


class WordAlreadyInDatabaseException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return f'WordAlreadyInDatabaseException, {self.message}'
        else:
            return 'WordAlreadyInDatabaseException has been raised'

class WordNotFoundInDatabaseException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return f'WordNotFoundInDatabaseException, {self.message}'
        else:
            return 'WordNotFoundInDatabaseException has been raised'

class AbbyyCharLimitReachedException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return f'AbbyyCharLimitReachedException, {self.message}'
        else:
            return 'AbbyyCharLimitReachedException has been raised. Likely solution - wait until next calendar day and retry.'
