import json
from PIL import Image
class DataManager:
    def __init__(self):
        pass

    # 同步读取 JSON 文件
    def loadJSON(self, file_path):
        # 使用内置 open 函数读取本地 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    # 同步加载图片
    def loadImg(self, file_path):
        # 使用 PIL 的 Image.open 直接打开本地图片文件
        image = Image.open(file_path)
        image.load()  # 确保图片被加载
        return image
