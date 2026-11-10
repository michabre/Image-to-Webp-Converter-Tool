# coding=utf-8
import csv
import os
import shutil
import subprocess

import typer

app = typer.Typer()

RESULTS_FILE = os.path.join("results", "converted_image_list.csv")
RAW_DIR_NAME = "raw"
CONVERTED_DIR_NAME = "converted"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
REPORT_HEADER = [
    "Original",
    "Raw Location",
    "Converted",
    "Converted Location",
    "Quality",
    "Savings %",
]


def finished_message(count, verb):
    if count == 1:
        return f"1 file has been {verb}."
    return f"{count} files have been {verb}."


def require_cwebp():
    if shutil.which("cwebp") is None:
        typer.echo(
            "cwebp was not found on PATH. Install Google's WebP tools and try again."
        )
        raise typer.Exit(code=1)


def webp_path(source, reserved):
    """Return a unique .webp path, replacing the source extension.

    photo.jpg and photo.png share a stem, so the second file keeps its
    old extension in the name (photo.png.webp) instead of overwriting
    the first conversion.
    """
    stem, ext = os.path.splitext(source)
    candidates = [stem + ".webp", stem + ext + ".webp"]
    for candidate in candidates:
        key = os.path.normcase(os.path.abspath(candidate))
        if key not in reserved:
            reserved.add(key)
            return candidate

    counter = 2
    while True:
        candidate = f"{stem}-{counter}.webp"
        key = os.path.normcase(os.path.abspath(candidate))
        if key not in reserved:
            reserved.add(key)
            return candidate
        counter += 1


def command_path(path):
    """Keep paths that start with '-' from being read as cwebp flags."""
    name = os.path.basename(path)
    if path.startswith("-") or name.startswith("-"):
        return os.path.join(os.curdir, path)
    return path


def convert_image_to_webp(source, destination, quality):
    subprocess.run(
        [
            "cwebp",
            "-q",
            str(quality),
            command_path(source),
            "-o",
            command_path(destination),
        ],
        check=True,
    )


def iter_images(directory):
    for root, _dirs, files in os.walk(directory):
        for name in files:
            ext = os.path.splitext(name)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                yield os.path.join(root, name)


def image_dirs(directory):
    return (
        os.path.join(directory, RAW_DIR_NAME),
        os.path.join(directory, CONVERTED_DIR_NAME),
    )


def scan_directory_for_images(raw_dir, converted_dir, quality):
    converted = []
    failures = []
    reserved = set()
    for source in iter_images(raw_dir):
        relative = os.path.relpath(source, raw_dir)
        destination = webp_path(os.path.join(converted_dir, relative), reserved)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        try:
            convert_image_to_webp(source, destination, quality)
        except subprocess.CalledProcessError:
            failures.append(source)
            continue
        converted.append([source, destination])
    return converted, failures


def savings_percent(original, converted):
    original_size = os.path.getsize(original)
    if original_size == 0:
        return "0.00"
    converted_size = os.path.getsize(converted)
    savings = (original_size - converted_size) / original_size * 100
    return f"{savings:.2f}"


def build_report(pairs, quality):
    rows = [REPORT_HEADER]
    for original, converted in pairs:
        rows.append(
            [
                original,
                os.path.dirname(original),
                converted,
                os.path.dirname(converted),
                quality,
                savings_percent(original, converted),
            ]
        )
    return rows


def write_report(rows):
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    with open(RESULTS_FILE, "w", newline="") as csv_file:
        csv.writer(csv_file).writerows(rows)


@app.command()
def convert(
    directory: str = typer.Argument(
        ...,
        help="Images directory. Sources are read from its raw folder.",
    ),
    quality: int = typer.Argument(..., help="WebP quality from 0 to 100."),
):
    """Convert images from a directory's raw folder into its converted folder."""
    if not 0 <= quality <= 100:
        typer.echo("Quality must be an integer from 0 to 100.")
        raise typer.Exit(code=1)
    if not os.path.isdir(directory):
        typer.echo(f"Directory not found: {directory}")
        raise typer.Exit(code=1)

    raw_dir, converted_dir = image_dirs(directory)
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(converted_dir, exist_ok=True)

    require_cwebp()
    typer.echo("//-------------- Converting Images ------------------//")
    typer.echo(f"Raw images: {raw_dir}")
    typer.echo(f"Converted images: {converted_dir}")
    pairs, failures = scan_directory_for_images(raw_dir, converted_dir, quality)
    write_report(build_report(pairs, quality))
    typer.echo(finished_message(len(pairs), "converted"))
    for failed in failures:
        typer.echo(f"Failed to convert: {failed}")
    if failures:
        raise typer.Exit(code=1)


def load_conversion_rows():
    if not os.path.isfile(RESULTS_FILE):
        typer.echo(f"No conversion list at {RESULTS_FILE}. Run convert first.")
        raise typer.Exit(code=1)

    rows = []
    with open(RESULTS_FILE, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames or []
        if "Original" not in fieldnames or "Converted" not in fieldnames:
            typer.echo(
                f"{RESULTS_FILE} is missing Original or Converted columns."
            )
            raise typer.Exit(code=1)
        for row in reader:
            original = (row.get("Original") or "").strip()
            converted = (row.get("Converted") or "").strip()
            if not original:
                continue
            rows.append((original, converted))
    return rows


@app.command()
def cleanup(
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Delete matching originals without a confirmation prompt.",
    ),
):
    """Delete originals listed in the CSV when the WebP file is present."""
    typer.echo("//-------------- Starting Cleanup ------------------//")
    rows = load_conversion_rows()
    deletable = []
    for original, converted in rows:
        if os.path.normcase(os.path.abspath(original)) == os.path.normcase(
            os.path.abspath(converted)
        ):
            typer.echo(f"Skipping {original}: original and converted paths match.")
            continue
        if not os.path.isfile(converted) or os.path.getsize(converted) == 0:
            typer.echo(f"Skipping {original}: converted file is missing or empty.")
            continue
        if not os.path.isfile(original):
            typer.echo(f"Original image not found: {original}")
            continue
        deletable.append(original)

    if not deletable:
        typer.echo("No original files to delete.")
        return

    if not yes and not typer.confirm(
        f"Delete {len(deletable)} original image(s) and keep the WebP files?"
    ):
        typer.echo("Cleanup cancelled.")
        raise typer.Exit(code=1)

    deleted = 0
    for path in deletable:
        try:
            os.remove(path)
        except OSError as exc:
            typer.echo(f"Could not delete {path}: {exc}")
            continue
        deleted += 1
    typer.echo(finished_message(deleted, "deleted"))
    if deleted != len(deletable):
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
