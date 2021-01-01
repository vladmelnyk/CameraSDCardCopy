import os
import shutil
import time
from datetime import date
import pandas as pd

SD_CARD_DIR = "/Volumes/NIKON Z 50 /DCIM"
TARGET_PHOTO_DIR_BASE_PATH = "/Users/vlad/Pictures/"
TARGET_VIDEO_DIR_BASE_PATH = "/Users/vlad/Movies/"
JPG_EXTENSION = "JPG"
RAW_EXTENSION = "NEF"
MOVIE_EXTENSION = "MOV"


def process():
    src_folders = os.listdir(SD_CARD_DIR)

    for folder in src_folders:
        src = SD_CARD_DIR + '/' + folder
        src_files = os.listdir(src)

        file_paths = [os.path.join(src, file_name) for file_name in os.listdir(src)]
        file_sizes = [os.path.getsize(src + '/' + file_path) for file_path in src_files]
        df = pd.DataFrame({'file_path': file_paths, 'file_size': file_sizes}).sort_values('file_size', ascending=True)
        total_size = df['file_size'].sum()
        total_size_readable = sizeof_fmt(total_size)
        processed_size_sum = 0.0
        for index, row in df.iterrows():
            full_file_name = row['file_path']
            file_name = os.path.basename(full_file_name)
            if os.path.isfile(full_file_name):
                extension = os.path.splitext(full_file_name)[1][1:]
                if extension == JPG_EXTENSION:
                    copy_file_fast(file_name, full_file_name, TARGET_PHOTO_DIR_BASE_PATH, '/' + JPG_EXTENSION.lower())
                if extension == RAW_EXTENSION:
                    copy_file_fast(file_name, full_file_name, TARGET_PHOTO_DIR_BASE_PATH, '/' + RAW_EXTENSION.lower())
                if extension == MOVIE_EXTENSION:
                    copy_file_fast(file_name, full_file_name, TARGET_VIDEO_DIR_BASE_PATH, "")

                processed_size_sum += row['file_size']
                print(sizeof_fmt(processed_size_sum) + '/' + total_size_readable)


def copy_file_fast(file_name, full_file_name, base_path, extension):
    timestamp = os.path.getctime(full_file_name)
    file_date = date.fromtimestamp(timestamp).__str__()
    dest = base_path + file_date + extension
    if not os.path.exists(dest):
        os.makedirs(dest)
    if not os.path.exists(dest + "/" + file_name):
        shutil.copyfile(full_file_name, dest + '/' + file_name)


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


if __name__ == '__main__':
    print("start")
    start_time = time.time()
    process()
    elapsed_time = time.time() - start_time
    print("finished")
    print("it took: " + str(round(elapsed_time, 2)) + " seconds")
