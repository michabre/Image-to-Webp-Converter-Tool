# coding=utf-8
import typer
import csv
import os
import subprocess

app = typer.Typer()


def get_image_data(arr, quality):
    count = 0
    collection = [['Original', 'Converted', 'Quality', 'Savings %']]
    for image in arr:
        count += 1
        difference = os.stat(image[0]).st_size - os.stat(image[1]).st_size
        savings = (difference / os.stat(image[0]).st_size) * 100
        total_savings = str(round(savings, 2))
        image_data = [image[0], image[1], quality, total_savings]
        collection.append(image_data)
    print('{count} files have been converted'.format(count=count))
    return collection


# scan directory for any images of the specified type
# https://www.tutorialspoint.com/python3/os_walk.htm
def scan_directory_for_images(directory, quality):
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
def convert(directory, quality):
    print('//-------------- Converting Images ------------------//')
    images = scan_directory_for_images(directory, quality)
    image_list = get_image_data(images, quality)
    results_file = './results/converted_image_list.csv'

    with open(results_file, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(image_list)
    csvFile.close()


@app.command()
def cleanup():
    print('//-------------- Starting Cleanup ------------------//')
    with open('./results/converted_image_list.csv') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        line_count = 0
        for row in reader:
            if line_count > 0:
                if os.path.exists(row[0]):
                    os.remove(row[0])
                else:
                    print("Original image not found.")
            line_count += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app()
