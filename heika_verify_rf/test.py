
class MyTest(object):
    def __enter__(self):
        print 'In __enter__'
        return MyTest()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print 'In __exit__'

    def haha(self):
        print 'haha'

if __name__ == "__main__":
    with MyTest() as myTest:
        print 'In with block'
        a='abc'
        myTest.haha()

    print a

