# coding=utf-8
import typer
import csv
import os
import subprocess
import math
import sys

from PIL import Image
from PIL.ExifTags import TAGS

app = typer.Typer()


# https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def get_jpg_data(arr, quality):
    count = 0
    collection = [['Original', 'Converted', 'Quality', 'Savings']]
    for image in arr:
        count += 1
        difference = convert_size(os.stat(image[0]).st_size - os.stat(image[1]).st_size)
        image_data = [image[0], image[1], quality, difference]
        collection.append(image_data)
    print('Files checked: ')
    print(count)
    return collection


# scan directory for any images of the specified type
# https://www.tutorialspoint.com/python3/os_walk.htm
def scan_directory(directory, quality):
    arr = []
    for root, dirs, files in os.walk(directory, topdown=False):
        for fileW in files:
            split_tup = os.path.splitext(fileW)
            file_extension = split_tup[1].lower()

            if file_extension == '.jpg' \
                    or file_extension == '.jpeg' \
                    or file_extension == '.png' \
                    or file_extension == '.tiff':
                raw_image = os.path.join(root, fileW)
                converted_image = raw_image + ".webp"
                convert_image_to_webp(
                    raw_image,
                    converted_image,
                    quality
                )
                arr.append([raw_image, converted_image])
    return arr


def convert_image_to_webp(image, converted_image, quality):
    call = "cwebp -q " + quality + " " + image + " -o " + converted_image
    subprocess.run(call, shell=True, check=True, text=True)


@app.command()
def scan(directory, quality):
    print('//-------------- Scanning For Images ------------------//')
    images = scan_directory(directory, quality)
    image_list = get_jpg_data(images, quality)
    results_file = './results/image_list.csv'

    with open(results_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(image_list)
    csvFile.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app()
