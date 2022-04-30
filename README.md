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

Using the **convert** command, it will walk through a specified directory and convert all applicable images to webp at the quality level specified.


```sh
# convert all applicable images 
# in the images directory
#
# python main.py convert [directory] [image quality]
python main.py convert "./images/" 75

```


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


<!-- REFERENCES -->
## References & Resources

* [An image format for the Web](https://developers.google.com/speed/webp)

