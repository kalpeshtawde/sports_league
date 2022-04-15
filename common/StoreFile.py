from datetime import datetime
from pathlib import Path
from sports_league import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class StoreFile:

    def __init__(self):
        pass

    def get_current_datetime_string(self):
        """ Function to get current datetime string """
        return datetime.now().strftime("%Y_%m_%d_%H%M%S%f")[:-3]

    def get_file_ext(self, filename):
        """ Function to get file extension """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower()

    def get_file_name(self, filename):
        """ Function to get file name """
        return '.' in filename and \
               filename.rsplit('.', 1)[0].lower()

    def store_files(self, file, file_name=None, ext=None, file_directory=None):
        """ Function to store files """
        if file_name is None:
            file_name = self.get_file_name(file.name)
        if ext is None:
            ext = self.get_file_ext(file.name)
        if file_directory is None:
            file_directory = str(settings.BASE_DIR) + str(Path('/uploadedFiles/'))
        file_name = file_directory + '/' + file_name + '_' + self.get_current_datetime_string() + '.' + ext
        fileUrl = default_storage.save(file_name, file)
        fileResponse = {}
        fileResponse['fileName'] = file_name
        fileResponse['fileUrl'] = fileUrl
        fileResponse['fileExtension'] = ext
        return fileResponse