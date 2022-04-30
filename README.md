<div id="top"></div>

<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="./logo.png" alt="Logo" width="300" height="150">
  </a>
  <h3 align="center">Image to Webp Conversion Helper Tool</h3>
  <p align="center">
    A simple tool written in Python for converting a directory of images into the webp format using Google's WebP Converter.
  </p>
</div>


<!-- GETTING STARTED -->
## Getting Started

In order to use this tool, you will need to have [Google's WebP Converter](https://developers.google.com/speed/webp/docs/precompiled) installed.

Without it, python will be unable to call the `cwebp` command from the CLI and convert applicable images.

<!-- USAGE EXAMPLES -->
## Usage

### Convert 

The **convert** command will walk through a specified directory and convert all applicable images to webp at the quality level specified.

```sh
# convert all applicable images 
# in the supplied images directory
#
# python main.py convert [directory] [image quality]
python main.py convert "./images/" 75
```

The directory can be the _images_ folder or it can be any directory locally accessible.

```sh
# convert all applicable images 
# in a system directory with a lower quality set
#
python main.py convert "C://Users/bob/web_images/" 50
```

### Cleanup

Once images have been converted, they are added to a CSV file in the _results_ directory (/results/converted_image_list.csv'). 

The CSV file is overwritten every time the **convert** command is run.

The **cleanup** command will look through the converted_image_list.csv and delete the original images and keep the webp ones.

```sh
# delete all the original images and keep the webp ones
#
python main.py cleanup
```


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


<!-- REFERENCES -->
## References & Resources

* [An image format for the Web](https://developers.google.com/speed/webp)

