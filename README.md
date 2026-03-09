<<<<<<< HEAD
# AI challenge: Header image generator for Endo Health’s blog

## Overview

This repository contains a small project that fulfils the coding challenge from
Endo Health (as described in their AI‑Solutions Engineer job listing).  The
challenge asks for a script that automatically generates suitable header
images for a list of blog titles.  The images should be consistent in style
and match the company’s brand identity.  You are welcome to explore and
extend this project – it’s designed to be transparent and easy to adapt.

## How the solution works

1. **Brand exploration and colours.**  I inspected Endo Health’s public
   website (https://endometriose.app) to understand the tone and colour
   palette.  The site uses soft gradients, pastel purples and teals, and
   minimalistic illustrations that convey a calm, supportive mood.  Based on
   this research I selected two main colours – `#7B5AA3` (purple) and
   `#0FA3B1` (teal) – as the core palette for all generated images【173463903977814†L86-L98】.  These
   colours are injected into the prompts sent to the image generator.

2. **Prompt engineering.**  The module `generate_header_images.py` constructs
   descriptive prompts that combine a base style description with each blog
   title.  The base style emphasises: soft gradients, abstract shapes,
   healthcare motifs, a calm/empowering mood and a wide rectangular layout.
   Only the subject of the blog post changes between prompts – everything else
   remains fixed to ensure stylistic cohesion.  The prompts explicitly
   reference the chosen colour palette and instruct the model to avoid
   embedding text.

3. **Calling the OpenAI API.**  The script uses OpenAI’s image generation
   endpoint (`dall‑e‑3` model) to create one image per title.  You can provide
   titles via a text file or directly on the command line.  The API key is
   passed via the `--api-key` argument or the `OPENAI_API_KEY` environment
   variable.  Each generated image is downloaded and saved to an output
   directory with a sanitized filename.  If you run the script yourself you
   must supply your own API key; the key is never hard‑coded.

4. **Streamlit web app (bonus).**  The file `streamlit_app.py` implements a
   lightweight web app.  Users can enter their API key and a list of titles
   directly in the browser.  The app calls the same prompt‑construction logic
   and displays the generated images inline.  Without an API key the app
   falls back to displaying the example images pre‑generated in this
   repository.  To deploy the app on a free hosting service you can use
   Streamlit Cloud: push the repository to GitHub and then create a new
   Streamlit app pointing at `streamlit_app.py`.

5. **Results.**  In this solution I used an internal image generation tool to
   create example header images for ten illustrative blog titles.  These
   images live in the `generated_images/` directory.  The titles reflect
   typical topics from Endo Health’s blog and knowledge base: understanding
   endometriosis, nutrition, pregnancy, chronic pain, mental health, cutting
   edge research, work–life balance, exercise, hormones and community
   support.  The cohesive look across the images demonstrates how a single
   prompt template and colour palette can produce unified visuals.

## Files in this project

| File | Purpose |
|-----|---------|
| `generate_header_images.py` | Stand‑alone script that takes blog titles and generates header images via the OpenAI API.  Prompts embed a fixed style description and brand colours. |
| `streamlit_app.py` | A Streamlit web application that lets anyone generate header images interactively.  If no API key is supplied it displays example images. |
| `generated_images/` | Folder containing ten example header images created for this challenge.  Use these as a visual reference or as assets in your cover letter. |
| `README.md` | The document you’re reading now – explains the reasoning, workflow and usage instructions. |

## Running the script

1. Ensure you have Python ≥ 3.8 installed.
2. Install dependencies:

   ```bash
   pip install openai requests
   ```

3. Export your OpenAI API key (or pass `--api-key` on the command line):

   ```bash
   export OPENAI_API_KEY=sk-...
   ```

4. Prepare a text file (e.g. `titles.txt`) with one blog title per line.

5. Run the script:

   ```bash
   python generate_header_images.py --titles-file titles.txt --output-dir my_images
   ```

The script will print progress for each title and save the resulting PNG
files into the specified output directory.

## Running the Streamlit app

First install Streamlit:

```bash
pip install streamlit
```

Then launch the app locally:

```bash
streamlit run streamlit_app.py
```

Open the displayed local URL in a web browser.  Enter your blog titles and
OpenAI API key to generate images on the fly.  To host the app publicly for
free, create a GitHub repository with this code and deploy it on
Streamlit Cloud (https://streamlit.io/cloud); the free tier is sufficient
for small prototypes.

## Limitations and future improvements

* **Brand fidelity.**  I approximated the colour palette and style based on
  publicly accessible sections of the Endo Health website【173463903977814†L86-L98】.  If you have access to
  official brand guidelines or a design system, update `BRAND_COLOURS` and
  the `BASE_STYLE` accordingly.
* **API costs and rate limits.**  Each call to DALL‑E consumes credits.  In the
  example run I generated images using a rate‑limited internal tool.  When
  running against the OpenAI API, be mindful of usage limits and the per‑
  image cost.
* **Image post‑processing.**  Some generated images may include extra
  whitespace or minor inconsistencies.  For production use you could add
  automatic cropping or resizing with PIL or a similar library.

## Licence

This code is provided for the purpose of completing the Endo Health AI
challenge.  You are free to reuse and adapt it for educational or personal
projects.  Please ensure compliance with OpenAI’s terms of service when
generating images.
=======
# ImageGenerator
>>>>>>> 4e05210bae8935b5336b90fa533dcf35dbaf2a08
