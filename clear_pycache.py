"""清除 __pycache__ 缓存"""
import shutil
import os


def purge_cache(dir_path):
    # 遍历目录下所有文件
    for file_name in os.listdir(dir_path):
        abs_path = os.path.join(dir_path, file_name)
        if file_name == "__pycache__" :
            print(abs_path)
            # 删除 `__pycache__` 目录及其中的所有文件
            shutil.rmtree(abs_path)
        elif os.path.isdir(abs_path):
            purge_cache(abs_path)


if __name__ == "__main__":
    purge_cache(os.path.dirname(os.path.abspath(__file__)))
