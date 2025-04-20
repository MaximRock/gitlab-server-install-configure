from pathlib import Path

from config_api.logger import Logger


class ConfigProjectGitlab:
    def __init__(self):
        self.base_dir = None
        self.logger = Logger().get_logger(__name__)

    def base_dir_path(self) -> Path:
        if self.base_dir is None:
            self.base_dir = Path(__file__).resolve().parent.parent
        else:
            self.base_dir = Path(self.base_dir).resolve()
        return self.base_dir

    def home_dir_path(self) -> Path:
        return Path.home()

    def path_to_file(self, *args) -> Path:
        return self.home_dir_path().joinpath(*args)

    def project_path_to_file(self, *args) -> Path:
        return self.base_dir_path().joinpath(*args)

    def replace_in_file(self, file_path: Path, old_string: str, new_string: str):
        if file_path.exists():
            with open(file_path, "r") as file:
                file_contents: str = file.read()
            file_contents = file_contents.replace(old_string, new_string)
            #self.logger.info(f"Replacing {old_string} with {new_string} in {file_path}")
            with open(file_path, "w") as file:
                file.write(file_contents)
            #self.logger.info(f"Successfully writed to {file_path}")
        else:
            self.logger.error(f"File {file_path} not found.")
            raise FileNotFoundError(f"File {file_path} not found.")

    def delete_in_file(self, dir_name: str, file_name: str) -> bool:
        file_path = self.project_path_to_file(dir_name, file_name)
        try:
            file_path.unlink(missing_ok=True)
            #self.logger.info(f"Deleted file {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting file: {e}")
            raise Exception(f"Error deleting file: {e}")

