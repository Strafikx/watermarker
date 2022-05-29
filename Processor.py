from concurrent.futures import ThreadPoolExecutor
from PIL import Image


class Processor:
    def __init__(self, watermark_path, temp_folder):
        print(watermark_path)
        self.watermark = Image.open(watermark_path)
        self.temp_folder = temp_folder
        self.save_folder = temp_folder
        self.watermark_position = 0, 0
        self.watermark_size = 201, 201
        
    
        # batch process
        self.pool = ThreadPoolExecutor()

    def __add_watermark(self, img):
        watermark = self.watermark.copy()
        watermark = watermark.resize(self.watermark_size)
        img.paste(watermark,
                  self.watermark_position,
                  mask=watermark.convert('RGBA'))

        return img

    def __add_watermark_and_save(self, img, path):
        img = self.__add_watermark(img)
        img.save(path)

    def generate_preview(self, path):
        img = Image.open(path)
        img = self.__add_watermark(img)
        img = img.resize((201, 201))

        path = f"{self.temp_folder}/preview.png"
        img.save(path)

    def start_batch_process(self, files, callback: callable = None):
        count = 0
        if callback:
            callback(f'{count}/{len(files)}')

        for file in files:
            img = Image.open(file)
            name = file.split('/')[-1]
            self.__batch_process(img, name)

            if callback:
                count += 1
                callback(f'{count}/{len(files)}')

        if callback:
            callback('START')

    def __batch_process(self, img, name):
        path = f"{self.save_folder}/{name}"
        self.__add_watermark_and_save(img, path)


