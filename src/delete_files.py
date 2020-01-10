import shutil
import os

class DeleteFiles:

    def __init__(self, path_list = ('logs/', 'plots/')):
        """

        :param path_list:
        """
        self.path_list = []

    def delete(self):
        """

        :return:
        """
        for path in self.path_list:
            if os.path.exists(path):
                shutil.rmtree(path)