"""
streamlit_app.py
------------------

This Streamlit application provides a simple interface to generate cohesive
header images for a list of blog titles.  It leverages the same prompt
construction logic as the standalone script in ``generate_header_images.py``,
but runs interactively in a web browser.  Users can enter their own list of
titles (one per line), optionally specify an OpenAI API key, and click a
button to generate images.  The resulting images are displayed directly in
the interface and can be downloaded.

Streamlit Cloud can host this app for free (with minor usage limits).  To
deploy it yourself, push the code into a public Git repository and then
create a new Streamlit Cloud project (see https://streamlit.io/cloud for
details).  Alternatively, run it locally with:

```bash
streamlit run streamlit_app.py
```

If you don’t have an API key or prefer not to make calls to OpenAI, the
application will fall back to displaying example images bundled in the
``generated_images`` directory.
"""

import os
import re
from typing import List

import openai
import requests
import streamlit as st


# Reuse the palette and prompt template defined in the script
BRAND_COLOURS = {
    "purple": "#7B5AA3",
    "teal": "#0FA3B1",
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
    filename = re.sub(r"\W+", "_", name.strip())
    return filename.strip("_").lower()


def build_prompt(title: str) -> str:
    return BASE_STYLE.format(
        title=title, purple=BRAND_COLOURS["purple"], teal=BRAND_COLOURS["teal"]
    )


def generate_images(titles: List[str], api_key: str) -> List[str]:
    """Generate images for a list of titles and return local filepaths."""
    paths = []
    openai.api_key = api_key
    for title in titles:
        prompt = build_prompt(title)
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1792x1024",
            model="dall-e-3",
        )
        url = response["data"][0]["url"]
        img_data = requests.get(url).content
        filename = sanitize_filename(title) + ".png"
        filepath = os.path.join("generated_images", filename)
        os.makedirs("generated_images", exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(img_data)
        paths.append(filepath)
    return paths


def load_example_images() -> List[str]:
    """Load example images from the bundled generated_images directory."""
    example_dir = "generated_images"
    if not os.path.isdir(example_dir):
        return []
    return [os.path.join(example_dir, f) for f in sorted(os.listdir(example_dir)) if f.lower().endswith((".png", ".jpg"))]


def main() -> None:
    st.set_page_config(page_title="Endo Blog Header Image Generator", layout="wide")
    st.title("Endo Blog Header Image Generator")
    st.markdown(
        "This app generates cohesive header images for your blog posts using "
        "OpenAI’s DALL‑E model.  Enter one title per line, provide your API key, "
        "and click **Generate** to receive brand‑aligned illustrations."
    )

    with st.expander("Instructions"):
        st.markdown(
            "* **API key**: Enter your OpenAI API key in the field below.  If "
            "left blank, the app will display example images instead of making API calls.\n"
            "* **Titles**: Provide one blog title per line.  The generator will "
            "create one image per title using a consistent style and colour scheme.\n"
            "* **Example images**: Without an API key you can explore the pre‑generated "
            "example images packaged with this project."
        )

    api_key = st.text_input("OpenAI API key (hidden)", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    titles_input = st.text_area(
        "Blog titles (one per line)",
        value="Was ist Endometriose? Symptome und Diagnose\n"
              "Ernährung bei Endometriose: Tipps für eine schmerzfreie Ernährung\n"
              "Schwangerschaft mit Endometriose: Was du wissen solltest\n"
              "Chronische Schmerzen bei Endometriose: Umgang und Bewältigung\n"
              "Psychologische Unterstützung bei Endometriose: Mental Health\n"
              "Innovative Therapien gegen Endometriose: Neueste Forschungsergebnisse\n"
              "Endometriose und Beruf: Wie du Arbeit und Gesundheit in Balance bringst\n"
              "Sport und Bewegung bei Endometriose: Vorteile und Empfehlungen\n"
              "Hormone und Endometriose: Verstehen und Behandeln\n"
              "Unterstützung aus der Community: Erfahrungen mit der Endo-App",
        height=200,
    )

    titles = [t.strip() for t in titles_input.split("\n") if t.strip()]

    if st.button("Generate"):
        if api_key:
            with st.spinner("Generating images… this may take a few seconds per title."):
                try:
                    image_paths = generate_images(titles, api_key)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    image_paths = []
        else:
            st.warning("No API key provided – displaying example images.")
            image_paths = load_example_images()

        if not image_paths:
            st.info("No images to display.")
        else:
            for title, path in zip(titles, image_paths):
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.write(f"**{title}**")
                with col2:
                    st.image(path, use_column_width=True)

    else:
        # Show example images when the app loads if available
        example_images = load_example_images()
        if example_images:
            st.markdown("### Example images")
            for path in example_images:
                st.image(path, use_column_width=True)


if __name__ == "__main__":
    main()