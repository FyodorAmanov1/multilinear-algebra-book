# An Introduction to Multilinear Algebra: The Intuitive Way

# Get the book here:
# https://fyodoramanov1.github.io/multilinear-algebra-book/
A friendly, illustrated, story-driven introduction to multilinear algebra for readers with high-school mathematics.

This repository contains:

- A complete LaTeX book.
- A static website with one interactive demo per chapter.
- QR codes in the book linking to the live demos.
- Original storybook diagrams and an animated, accessible website design.
- 56 geometric teaching illustrations, with matching worked calculations.
- Twelve Victorian-style pen-and-ink chapter-opening story illustrations, using a shared character reference cast.
- Explicit real scalar conventions and marked introductions to complex numbers.
- A hints-and-answers section for every exercise.
- A reproducible build pipeline.

## Quick start

```bash
python -m pip install -r requirements.txt
python scripts/build.py all
```

The generated PDF is written to:

```text
build/book/main.pdf
```

The generated website is written to:

```text
site/
```

Preview the site locally with:

```bash
python scripts/serve.py
```

## Free first book and the planned series

The complete first book is free and openly accessible. All twelve
chapters, answers, interactive demos, and the complete PDF are hosted on
**GitHub Pages**. The homepage introduces the planned series of story-based
mathematics and science books; future volumes are intended to be paid releases.

```bash
python scripts/build.py all
python scripts/build_pages.py
```

The deployment directory is `build/public/`. The GitHub Actions workflow builds
and publishes it on pushes to `main` or `master`, using GitHub Pages as the
repository's publishing source. The existing `content/book.json` supplies the
website URL and repository path. See [FREE_BOOK_SETUP.md](FREE_BOOK_SETUP.md)
for publication details and [LINKEDIN_LAUNCH.md](LINKEDIN_LAUNCH.md) for draft
posts.

## Structure

The build regenerates all SVG and PDF illustrations before building the book
and website. To regenerate just the illustrations, run
`python scripts/make_figures.py`. To validate a completed build, run
`python scripts/build.py check`.

```text
content/        Chapter, demo, and answer source
templates/      LaTeX and HTML templates
filters/        Pandoc filters for custom boxes and demos
assets/         Images, CSS, JavaScript, and demo fragments
scripts/        Build and validation scripts
site/           Generated static website output
build/          Generated book and temporary artifacts
```

## Licence

- Book text and original illustrations: **Creative Commons BY-NC 4.0**
- Build scripts, website code, and demo code: **MIT**

See `LICENSE.md` and `LICENSE-CODE.md` for details.
