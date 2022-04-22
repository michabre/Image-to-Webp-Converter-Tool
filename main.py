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
        # im = Image.open(image[0])
        # info = im._getexif()
        # if info is not None:
        #     for tag, value in info.items():
        difference = convert_size(os.stat(image[0]).st_size - os.stat(image[1] + ".webp").st_size)
        image_data = [image[0], image[1], quality, difference]
        # key = TAGS.get(tag, tag)
        collection.append(image_data)
    print('Files checked: ')
    print(count)
    return collection


# scan directory for any images of the specified type
# https://www.tutorialspoint.com/python3/os_walk.htm
def scan_directory(directory, image_type, quality):
    arr = []
    image_extension = '.' + image_type
    for root, dirs, files in os.walk(directory, topdown=False):
        for fileW in files:
            if image_extension in fileW:
                raw_image = os.path.join(root, fileW)
                converted_image = "D:/PycharmProjects/webpCommandProject/images/web/" + fileW
                convert_image_to_webp(
                    raw_image,
                    converted_image,
                    quality
                )

                # arr.append(os.path.join(root, fileW))
                arr.append([raw_image, converted_image])
    return arr


def convert_image_to_webp(image, converted_image, quality):
    call = "cwebp -q " + quality + " " + image + " -o " + converted_image + ".webp"
    subprocess.run(call, shell=True, check=True, text=True)


@app.command()
def scan(filetype, directory, quality):
    print('//-------------- Scanning ' + filetype + ' Files ------------------//')
    images = scan_directory(directory, filetype, quality)
    image_list = get_jpg_data(images, quality)
    results_file = './results/' + filetype + '-image_list.csv'

    with open(results_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(image_list)
    csvFile.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app()
