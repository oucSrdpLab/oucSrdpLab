import os

# 此文件存储全局相关的变量
import sys

# 项目文件根路径
BASE_DIR = os.path.dirname(__file__)
sys.path.insert(0, BASE_DIR)

# 将app路径加入到环境变量中
APP_PATH = os.path.join(BASE_DIR, "apps")

sys.path.insert(0, APP_PATH)

if __name__ == "__main__":
    print(BASE_DIR)


