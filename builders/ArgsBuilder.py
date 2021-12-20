class ArgsBuilder:

    def __init__(self):
        self.list_of_tuple = []

    def add_arg(self, arg_name, arg_value):
        self.list_of_tuple.append((arg_name, arg_value))
        return self

    def build(self):
        args = ""
        for arg_pair in self.list_of_tuple:
            arg_name = arg_pair[0]
            arg_value = arg_pair[1]
            arg = "%s %s " % (arg_name, arg_value)
            args += arg
        return args
