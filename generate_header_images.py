"""
generate_header_images.py
---------------------------------

This script takes a list of blog titles and uses OpenAI’s image generation API to
create cohesive header images.  The goal is to produce illustrations that
harmonise with the Endo Health (Endometriose) brand identity: soft gradients,
pastel purple and teal colours, abstract shapes and gentle healthcare motifs.

For each title the script constructs a prompt by combining a generic style
description with the title itself and a short subject hint.  It then sends
requests to the OpenAI API to generate images.  The resulting images are saved
into an output directory using sanitized filenames.  Before running the script
you must export your OpenAI API key as an environment variable
`OPENAI_API_KEY` or pass it via `--api-key`.

Example:

```bash
export OPENAI_API_KEY=sk-...
python generate_header_images.py --titles-file titles.txt --output-dir generated_images
```

If you prefer to pass titles directly on the command line:

```bash
python generate_header_images.py --titles "Title A" "Title B" "Title C"
```

This script is designed to be self‑contained and straightforward to adapt.  You
can modify the base prompt or colour palette at the top of the file to fine
tune the aesthetic.  The script prints progress messages so you can monitor
generation progress.
"""

import argparse
import os
import re
from typing import Iterable, List, Optional

import openai
import requests


# -----------------------------------------------------------------------------
# Configuration
# Define the brand colour palette and a generic style description.  These
# variables control the look and feel of every generated image.  Adjust
# `BRAND_COLOURS` if you discover more accurate hues from Endo Health’s style
# guide.
BRAND_COLOURS = {
    "purple": "#7B5AA3",  # calm, reassuring purple used in Endo Health’s design
    "teal": "#0FA3B1",    # bright teal accent
    # You can extend this dict with additional shades if desired
}

BASE_STYLE = (
    "A modern, minimalistic header image for the blog title '{title}', "
    "using the Endo Health colour palette of purple ({purple}) and teal "
    "({teal}). Soft gradients and abstract shapes should convey the core "
    "concept of the title – think of gentle curves, flowing waves and "
    "subtle healthcare motifs. Avoid text. The style must be cohesive, calm "
    "and empowering with smooth lines and a digital health feel. Wide "
    "rectangular layout suitable for a website header."
)


def sanitize_filename(name: str) -> str:
    """Sanitise a string to create a safe filename."""
    # Replace non‑word characters with underscores and collapse repeats.
    filename = re.sub(r"\W+", "_", name.strip())
    return filename.strip("_").lower()


def build_prompt(title: str) -> str:
    """Build a descriptive prompt for a given title using the base style."""
    return BASE_STYLE.format(title=title, purple=BRAND_COLOURS["purple"], teal=BRAND_COLOURS["teal"])


def generate_image_for_title(title: str, api_key: str, output_dir: str) -> str:
    """Generate a header image for a single blog title and save it.

    Returns the path to the saved file.
    """
    prompt = build_prompt(title)
    print(f"Generating image for '{title}'…")

    # Use OpenAI’s image creation API (DALL‑E).  We request a single image
    # with a 1792×1024 aspect ratio which fits well for website headers.  See
    # https://platform.openai.com/docs/guides/images for details.
    openai.api_key = api_key
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1792x1024",
        model="dall-e-3"
    )
    # The API returns a URL for each generated image.
    image_url = response["data"][0]["url"]
    # Download the image
    image_data = requests.get(image_url).content

    filename = sanitize_filename(title) + ".png"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "wb") as f:
        f.write(image_data)
    print(f"Saved image to {filepath}")
    return filepath


def load_titles_from_file(filename: str) -> List[str]:
    """Load blog titles from a text file, one title per line."""
    with open(filename, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def main(args: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Generate cohesive header images for blog titles.")
    parser.add_argument(
        "--titles-file", type=str, default=None,
        help="Path to a text file containing blog titles (one per line)."
    )
    parser.add_argument(
        "--titles", nargs="*", default=None,
        help="List of titles passed directly via command line."
    )
    parser.add_argument(
        "--output-dir", type=str, default="generated_images",
        help="Directory to save generated images."
    )
    parser.add_argument(
        "--api-key", type=str, default=os.getenv("OPENAI_API_KEY"),
        help="OpenAI API key.  If not supplied, the environment variable OPENAI_API_KEY is used."
    )
    parsed = parser.parse_args(args)

    if not parsed.titles_file and not parsed.titles:
        parser.error("Please provide either --titles-file or --titles.")

    if not parsed.api_key:
        parser.error("An OpenAI API key is required. Use --api-key or set OPENAI_API_KEY.")

    # Assemble list of titles
    titles: List[str] = []
    if parsed.titles_file:
        titles.extend(load_titles_from_file(parsed.titles_file))
    if parsed.titles:
        titles.extend(parsed.titles)

    # Create output directory
    os.makedirs(parsed.output_dir, exist_ok=True)

    # Generate images
    for title in titles:
        try:
            generate_image_for_title(title, parsed.api_key, parsed.output_dir)
        except Exception as e:
            print(f"Failed to generate image for '{title}': {e}")


if __name__ == "__main__":
    main()