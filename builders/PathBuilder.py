import os


class PathBuilder:

    def __init__(self):
        self.path_to_project = os.getcwd()
        self.build_path = self.path_to_project

    def add_dir(self, name_of_dir):
        self.build_path = self.build_path + '/' + name_of_dir
        return self

    def add_file(self, file_name, extension):
        self.build_path = "%s/%s.%s" % (self.build_path, file_name, extension)
        return self

    def add_file_with_extension(self, file_name_with_extension):
        self.build_path = "%s/%s" % (self.build_path, file_name_with_extension)
        return self

    def create_directory_if_not_exists(self):
        if not os.path.exists(self.build_path):
            os.mkdir(self.build_path)
        return self

    def build(self):
        return self.build_path
