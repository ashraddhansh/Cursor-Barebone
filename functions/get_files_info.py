import os

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory,directory)
        abs_path = os.path.abspath(full_path)

        if not abs_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_path):
            return f'Error: "{directory}" is not a directory'

        list_of_files = os.listdir(abs_path)
        dir_info = []
        for item in list_of_files:
            abs_path_item = os.path.join(full_path,item)
            dir_info.append(f"- {item}: file_size={os.path.getsize(abs_path_item)}, is_dir={os.path.isdir(abs_path_item)}")
        return "\n".join(dir_info)
    except Exception as e:
        return f"Error: {e}"

