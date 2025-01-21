import os
import uuid
from PIL import Image
from exceptions.system.file_error import FileError

class FileService:
    def __init__(self, upload_folder, allowed_extensions, max_file_size):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions
        self.max_file_size = max_file_size

        # Ensure the upload folder exists
        os.makedirs(self.upload_folder, exist_ok=True)

    def save_file(self, file):
        """
        Securely save the uploaded file to the upload folder.
        :param file: The uploaded file object.
        :return: The path to the saved file.
        """
        try:
            file_path = os.path.join(self.upload_folder, f"{uuid.uuid4()}__{file.filename}")
            file.save(file_path)
            return file_path
        except Exception as e:
            raise FileError(f"Failed to save file: {str(e)}")

    def validate_and_resize_image(self, file_path, output_size=(300, 300)):
        """
        Validate and resize an image file.
        :param file_path: The path to the image file.
        :param output_size: Desired output size (width, height).
        """
        try:
            with Image.open(file_path) as img:
                img.verify()  # Ensure it's a valid image

                # Open and resize the image
                img = Image.open(file_path)
                img = img.resize(output_size, Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
                img.save(file_path)
        except Exception as e:
            os.remove(file_path)  # Delete the invalid file
            raise FileError(f"Invalid image file: {str(e)}")
