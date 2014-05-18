class TmpMaker(object):
    def __init__(self, mkdtemp, rmtree):
        self.mkdtemp = mkdtemp
        self.rmtree = rmtree
        self.created_directories = []

    def __call__(self):
        tmp_dir = self.mkdtemp()
        self.created_directories.append(tmp_dir)
        return tmp_dir

    def remove_all(self):
        for tmp_dir in reversed(self.created_directories):
            self.rmtree(tmp_dir)


def tempdirmaker():
    counter = []

    def tmpmaker():
        result = 'tempdir%s' % len(counter)
        counter.append('l')
        return result

    return tmpmaker
