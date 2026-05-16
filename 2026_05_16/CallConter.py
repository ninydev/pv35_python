class CallCounter:
    def __init__(self):
        self.count = 0
    
    
    def __call__(self, *args, **kwargs):
        self.count += 1


    def doClick(self):
        self.count += 1

    def getCount(self):
        return self.count