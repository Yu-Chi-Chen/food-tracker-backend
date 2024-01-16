import os
import uuid


class ImageHandler:
    def save_image(self, file):
        filename = str(uuid.uuid4()) + ".jpg"
        file_path = os.path.join('..\\uploads', filename)
        file.save(file_path)
        return filename, file_path
