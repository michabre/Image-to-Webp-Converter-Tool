<div id="top"></div>

<br />
<div align="center">
  <a href="https://github.com/michabre/Image-to-Webp-Converter-Tool">
    <img src="./logo.png" alt="Logo" width="300" height="150">
  </a>
  <h3 align="center">Image to Webp Conversion Helper Tool</h3>
  <p align="center">
    A simple tool written in Python for converting a directory of images into the webp format using Google's WebP Converter.
  </p>
</div>


<!-- GETTING STARTED -->
## Getting Started

In order to use this tool, you will need to have [Google's WebP Converter](https://developers.google.com/speed/webp/docs/precompiled) installed and `cwebp` available on your PATH.

Without it, Python will be unable to convert images. Install the Python dependency with:

```sh
pip install -r requirements.txt

# start Python 
source .venv/Scripts/activate
```

<!-- USAGE EXAMPLES -->
## Usage

### Convert 

Place source images in the `raw` folder. The **convert** command reads that folder and writes WebP files to the sibling `converted` folder. Subfolders under `raw` are recreated under `converted`.

```text
images/
  raw/photo.jpg
  converted/photo.webp
```

Applicable files are `.jpg`, `.jpeg`, `.png`, `.tif`, and `.tiff`. Quality is an integer from 0 to 100. `photo.jpg` is written to `photo.webp`. When two files share a stem (`photo.jpg` and `photo.png`), the second keeps its old extension in the name so it does not overwrite the first.

```sh
# convert images from images/raw into images/converted
#
# python main.py convert [directory] [image quality]
python main.py convert "./images/" 75
```

The directory can be the _images_ folder or any directory you can read. Paths with spaces are fine. Pass the directory that contains `raw`, not the `raw` folder itself.

```sh
# convert images from a system directory with a lower quality set
#
python main.py convert "C:/Users/bob/web images/" 50
```

A missing directory is reported and nothing is written. When the directory exists, `raw` and `converted` are created if they are missing. Each file is converted on its own, so one failure does not discard the rest. `results/` is created if it is missing.

### Cleanup

Once images have been converted, they are added to a CSV file in the _results_ directory (`results/converted_image_list.csv`).

Each row lists the original file, the raw folder it was read from, the WebP file, the converted folder it was written to, the quality, and the savings. The CSV file is overwritten every time the **convert** command is run, and it lists only the files that converted.

The **cleanup** command reads that CSV and deletes an original from `raw` only when its WebP file exists and is not empty. Files in `converted` are left in place. It asks for confirmation first. Pass `--yes` to skip the prompt.

```sh
# delete the original images and keep the webp ones
python main.py cleanup

# same deletion, without the prompt
python main.py cleanup --yes
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


<!-- REFERENCES -->
## References & Resources

* [An image format for the Web](https://developers.google.com/speed/webp)
