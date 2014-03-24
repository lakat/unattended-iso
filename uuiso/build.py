import argparse


class IsoMounter(object):
    def __init__(self, path, file_checker=None, executor=None, tmpmaker=None):
        self.path = path
        self.file_checker = file_checker
        self.executor = executor
        self.tmpmaker = tmpmaker

    def validate(self):
        if self.file_checker(self.path):
            return True
        return False

    def mount(self):
        tempdir = self.tmpmaker()
        self.executor(
            ['fuseiso', self.path, tempdir])
        return tempdir


def get_args_or_die(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('official')
    parser.add_argument('automated')

    return parser.parse_args(args=args)


def main():
    pass
