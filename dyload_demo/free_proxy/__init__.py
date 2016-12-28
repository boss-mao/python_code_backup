class Dynload():
    def __init__(self, package, imp_list):
        self.package = package
        self.imp = imp_list

    def getobject(self):
        return __import__(self.package, globals(), locals(), self.imp, -1)

    def getClassInstance(self, classstr, *args):
        return getattr(self.getobject(), classstr)(*args)

    def execfunc(self, method, *args):
        return getattr(self.getobject(), method)(*args)

    def execMethod(self, instance, method, *args):
        return getattr(instance, method)(*args)