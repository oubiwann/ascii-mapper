import os

def get_top_directory():
    import asciimap
    return os.path.basename(asciimap.__path__[0])


def get_test_module():
    return get_top_directory().replace("/", ".")
