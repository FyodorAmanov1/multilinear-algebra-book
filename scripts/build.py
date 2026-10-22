#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import yaml
import matplotlib.pyplot as plt
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_M
from qrcode.image.pil import PilImage
from teaching_figures import FIGURE_NAMES, generate_all


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
SITE = ROOT / "site"
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
FILTERS = ROOT / "filters"
ASSETS = ROOT / "assets"
BACKMATTER = CONTENT / "backmatter"
MANIFEST = BUILD / "build-manifest.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"Missing front matter in {path}")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"Invalid front matter in {path}")
    return data


def find_pandoc() -> Path:
    exe = shutil.which("pandoc")
    if exe:
        return Path(exe)

    fallback = Path.home() / "AppData" / "Local" / "Pandoc" / "pandoc.exe"
    if fallback.exists():
        return fallback

    raise RuntimeError("Pandoc was not found. Install Pandoc 3.x or later.")


def run(command: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    print(">>", " ".join(str(part) for part in command))
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, command)
    return result


def ensure_clean(path: Path) -> None:
    resolved = path.resolve()
    if resolved not in {BUILD.resolve(), SITE.resolve()} or resolved.parent != ROOT.resolve():
        raise ValueError(f"Refusing to clear an unexpected build directory: {resolved}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def copy_assets(book: dict[str, Any]) -> None:
    site_assets = SITE / "assets"
    if site_assets.exists():
        if not site_assets.resolve().is_relative_to(SITE.resolve()):
            raise ValueError("Site assets resolve outside the generated site.")
        shutil.rmtree(site_assets)
    shutil.copytree(ASSETS, site_assets)

    book_assets = BUILD / "book" / "assets"
    if book_assets.exists():
        if not book_assets.resolve().is_relative_to(BUILD.resolve()):
            raise ValueError("Book assets resolve outside the build directory.")
        shutil.rmtree(book_assets)
    shutil.copytree(ASSETS, book_assets)

    qr_dir = book_assets / "qr"
    qr_dir.mkdir(parents=True, exist_ok=True)

    demos = load_json(CONTENT / "demos.json")
    for demo in demos:
        url = f"{book['base_url']}demos/{demo['id']}/"
        qr = QRCode(error_correction=ERROR_CORRECT_M, box_size=12, border=3)
        qr.add_data(url)
        qr.make(fit=True)
        image = qr.make_image(image_factory=PilImage)
        image.save(qr_dir / f"{demo['id']}.png")


def make_cover(book: dict[str, Any]) -> None:
    fig = plt.figure(figsize=(8.5, 12.75), facecolor="#002147")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 15)
    ax.axis("off")

    ax.fill_between([0, 10], [15, 15], [8.4, 9.1], color="#0f766e", alpha=.55)
    ax.fill_between([0, 10], [8.4, 9.1], [0, 0], color="#002147")
    for i in range(18):
        x = i * .62
        ax.plot([x, x + 3.2], [15, 6.5], color="#ffffff", alpha=.10, linewidth=1.4)

    ax.add_patch(plt.Circle((8.1, 11.8), 1.35, facecolor="none", edgecolor="#c9a227", linewidth=7))
    ax.add_patch(plt.Circle((2.2, 11.2), .95, facecolor="none", edgecolor="#ffffff", linewidth=4))
    ax.plot([1.2, 5.2], [7.1, 9.6], color="#ffffff", linewidth=9, solid_capstyle="round")
    ax.plot([1.2, 2.8], [7.1, 5.4], color="#c9a227", linewidth=8, solid_capstyle="round")
    ax.plot([1.2, 3.4], [7.1, 7.4], color="#8fd3c6", linewidth=8, solid_capstyle="round")

    ax.text(.7, 4.55, "An Introduction to", fontsize=21, color="#ffffff", va="center")
    ax.text(.7, 3.65, "Multilinear Algebra", fontsize=38, color="#ffffff", weight="bold", va="center")
    ax.text(.7, 2.85, "The Intuitive Way", fontsize=25, color="#c9a227", weight="bold", va="center")
    ax.text(.7, 2.05, book["subtitle"], fontsize=16, color="#e8f0f6", va="center")
    ax.text(.7, .75, book["author"], fontsize=17, color="#ffffff", va="center")

    output_dir = BUILD / "book" / "assets" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / "cover.pdf", facecolor=fig.get_facecolor())
    plt.close(fig)


def chapter_paths() -> list[Path]:
    return sorted((CONTENT / "chapters").glob("*.md"))


def chapter_metadata() -> list[dict[str, Any]]:
    result = []
    for path in chapter_paths():
        data = load_front_matter(path)
        data["path"] = path
        result.append(data)
    return result


def pandoc_base_args(book: dict[str, Any], pandoc: Path) -> list[str]:
    return [
        str(pandoc),
        "--from",
        "markdown+pipe_tables+fenced_divs+tex_math_dollars",
        "--metadata-file",
        str(CONTENT / "book.json"),
        "--metadata",
        f"base_path={book['base_path']}",
        "--metadata",
        f"base_url={book['base_url']}",
        "--lua-filter",
        str(FILTERS / "blocks.lua"),
    ]


def generate_chapter_tex(
    book: dict[str, Any],
    pandoc: Path,
    chapter: dict[str, Any],
) -> None:
    output_dir = BUILD / "book" / "chapters"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{chapter['slug']}.tex"

    command = pandoc_base_args(book, pandoc) + [
        "--to",
        "latex",
        "--template",
        str(TEMPLATES / "chapter.tex"),
        "--top-level-division=chapter",
        "-o",
        str(output),
        str(chapter["path"]),
    ]
    run(command)


def control_specs() -> dict[str, list[dict[str, Any]]]:
    return {
        "vector-playground": [
            {"id": "vector-a-x", "label": "u_x", "min": -3, "max": 3, "step": 0.1, "value": 1},
            {"id": "vector-a-y", "label": "u_y", "min": -3, "max": 3, "step": 0.1, "value": 2},
            {"id": "vector-b-x", "label": "v_x", "min": -3, "max": 3, "step": 0.1, "value": 3},
            {"id": "vector-b-y", "label": "v_y", "min": -3, "max": 3, "step": 0.1, "value": -1},
            {"id": "scale", "label": "scale", "min": -2, "max": 3, "step": 0.1, "value": 1},
        ],
        "basis-explorer": [
            {"id": "basis-a-angle", "label": "angle of b1", "min": 0, "max": 360, "step": 1, "value": 15},
            {"id": "basis-a-length", "label": "length of b1", "min": 0.2, "max": 3, "step": 0.05, "value": 1},
            {"id": "basis-b-angle", "label": "angle of b2", "min": 0, "max": 360, "step": 1, "value": 105},
            {"id": "basis-b-length", "label": "length of b2", "min": 0.2, "max": 3, "step": 0.05, "value": 1},
            {"id": "point-x", "label": "point x", "min": -4, "max": 4, "step": 0.1, "value": 2},
            {"id": "point-y", "label": "point y", "min": -4, "max": 4, "step": 0.1, "value": 1},
        ],
        "linear-map-theater": [
            {"id": "matrix-a", "label": "a", "min": -3, "max": 3, "step": 0.1, "value": 1},
            {"id": "matrix-b", "label": "b", "min": -3, "max": 3, "step": 0.1, "value": 0},
            {"id": "matrix-c", "label": "c", "min": -3, "max": 3, "step": 0.1, "value": 0},
            {"id": "matrix-d", "label": "d", "min": -3, "max": 3, "step": 0.1, "value": 1},
        ],
        "inner-product-lab": [
            {"id": "u-angle", "label": "angle of u", "min": 0, "max": 360, "step": 1, "value": 25},
            {"id": "u-length", "label": "length of u", "min": 0, "max": 4, "step": 0.1, "value": 3},
            {"id": "v-angle", "label": "angle of v", "min": 0, "max": 360, "step": 1, "value": 95},
            {"id": "v-length", "label": "length of v", "min": 0, "max": 4, "step": 0.1, "value": 2},
        ],
        "determinant-volume": [
            {"id": "matrix-a", "label": "a", "min": -3, "max": 3, "step": 0.1, "value": 1.5},
            {"id": "matrix-b", "label": "b", "min": -3, "max": 3, "step": 0.1, "value": 0.5},
            {"id": "matrix-c", "label": "c", "min": -3, "max": 3, "step": 0.1, "value": 0.5},
            {"id": "matrix-d", "label": "d", "min": -3, "max": 3, "step": 0.1, "value": 1.2},
        ],
        "eigenvector-dance": [
            {"id": "matrix-a", "label": "a", "min": -2, "max": 2, "step": 0.05, "value": 1.4},
            {"id": "matrix-d", "label": "d", "min": -2, "max": 2, "step": 0.05, "value": 0.8},
            {"id": "iterations", "label": "iterations", "min": 1, "max": 12, "step": 1, "value": 4},
            {"id": "speed", "label": "speed", "min": 0.1, "max": 3, "step": 0.1, "value": 1},
        ],
        "bilinear-form-lab": [
            {"id": "form-a", "label": "a", "min": -3, "max": 3, "step": 0.1, "value": 1},
            {"id": "form-b", "label": "b", "min": -2, "max": 2, "step": 0.1, "value": 0.5},
            {"id": "form-c", "label": "c", "min": -3, "max": 3, "step": 0.1, "value": 1},
        ],
        "wedge-areas": [
            {"id": "u-angle", "label": "angle of u", "min": 0, "max": 360, "step": 1, "value": 25},
            {"id": "u-length", "label": "length of u", "min": 0, "max": 4, "step": 0.1, "value": 3},
            {"id": "v-angle", "label": "angle of v", "min": 0, "max": 360, "step": 1, "value": 110},
            {"id": "v-length", "label": "length of v", "min": 0, "max": 4, "step": 0.1, "value": 2},
        ],
        "tensor-product-builder": [
            {"id": "u-x", "label": "u_x", "min": -3, "max": 3, "step": 0.1, "value": 2},
            {"id": "u-y", "label": "u_y", "min": -3, "max": 3, "step": 0.1, "value": 1},
            {"id": "v-x", "label": "v_x", "min": -3, "max": 3, "step": 0.1, "value": 1},
            {"id": "v-y", "label": "v_y", "min": -3, "max": 3, "step": 0.1, "value": 3},
            {"id": "basis-size", "label": "basis size", "min": 1, "max": 5, "step": 1, "value": 3},
        ],
        "component-transformer": [
            {"id": "angle", "label": "basis angle", "min": 0, "max": 360, "step": 1, "value": 30},
            {"id": "tensor-type", "label": "type", "type": "select", "options": ["vector", "covector", "bilinear form"]},
            {"id": "covariance", "label": "index", "type": "select", "options": ["upper", "lower"]},
        ],
        "tensor-applications": [
            {"id": "stress-a", "label": "mean stress", "min": 0, "max": 3, "step": 0.05, "value": 1.5},
            {"id": "stress-b", "label": "anisotropy", "min": -2, "max": 2, "step": 0.05, "value": 0.7},
            {"id": "diffusion-ratio", "label": "diffusion ratio", "min": 0.1, "max": 3, "step": 0.05, "value": 1},
        ],
        "forms-and-fields": [
            {"id": "form-a", "label": "dx coefficient", "min": -3, "max": 3, "step": 0.1, "value": 1},
            {"id": "form-b", "label": "dy coefficient", "min": -3, "max": 3, "step": 0.1, "value": 0.5},
            {"id": "show-area", "label": "show area form", "type": "checkbox", "value": True},
        ],
    }


def render_controls(specs: list[dict[str, Any]]) -> str:
    output = []
    for spec in specs:
        control_id = spec["id"]
        label = spec["label"]
        if spec.get("type") == "select":
            options = "".join(
                f'<option value="{option}">{option}</option>'
                for option in spec.get("options", [])
            )
            output.append(
                f'<div class="control"><label for="{control_id}">{label}</label>'
                f'<select id="{control_id}">{options}</select></div>'
            )
        elif spec.get("type") == "checkbox":
            output.append(
                f'<div class="control"><label for="{control_id}">{label}</label>'
                f'<input type="checkbox" id="{control_id}" checked></div>'
            )
        else:
            output.append(
                f'<div class="control"><label for="{control_id}">{label}</label>'
                f'<input type="range" id="{control_id}" min="{spec.get("min", 0)}" '
                f'max="{spec.get("max", 1)}" step="{spec.get("step", 0.1)}" value="{spec.get("value", 0)}"></div>'
            )
    return "\n".join(output)


def generate_chapter_html(
    book: dict[str, Any],
    pandoc: Path,
    chapter: dict[str, Any],
    chapters: list[dict[str, Any]],
) -> None:
    output_dir = SITE / "chapters" / chapter["slug"]
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / "index.html"

    command = pandoc_base_args(book, pandoc) + [
        "--to",
        "html5",
        "--standalone",
        "--template",
        str(TEMPLATES / "chapter.html"),
        "--mathjax",
        "-o",
        str(output),
        str(chapter["path"]),
    ]
    run(command)

    template = output.read_text(encoding="utf-8")
    index = chapters.index(chapter)
    previous = chapters[index - 1] if index > 0 else None
    next_chapter = chapters[index + 1] if index + 1 < len(chapters) else None
    replacements = {
        "__BOOK_TITLE__": book["title"],
        "__BOOK_SUBTITLE__": book["subtitle"],
        "__BOOK_AUTHOR__": book["author"],
        "__BOOK_YEAR__": str(book["year"]),
        "__BOOK_LICENSE__": book["license"],
        "__BASE_PATH__": book["base_path"],
        "__PREVIOUS_URL__": (
            f'{book["base_path"]}chapters/{previous["slug"]}/'
            if previous else f'{book["base_path"]}chapters/'
        ),
        "__PREVIOUS_LABEL__": f'← {previous["title"]}' if previous else "Start",
        "__NEXT_URL__": (
            f'{book["base_path"]}chapters/{next_chapter["slug"]}/'
            if next_chapter else f'{book["base_path"]}answers/'
        ),
        "__NEXT_LABEL__": f'{next_chapter["title"]} →' if next_chapter else "Hints and answers →",
        "__CHAPTER_POSITION__": f"Room {index + 1} of {len(chapters)}",
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    template = template.replace(
        'src="/assets/',
        f'src="{book["base_path"]}assets/'
    )
    output.write_text(template, encoding="utf-8")


def generate_answers_tex(book: dict[str, Any], pandoc: Path) -> None:
    output_dir = BUILD / "book" / "backmatter"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / "answers.tex"

    command = pandoc_base_args(book, pandoc) + [
        "--to",
        "latex",
        "--template",
        str(TEMPLATES / "chapter.tex"),
        "--top-level-division=chapter",
        "-o",
        str(output),
        str(BACKMATTER / "answers.md"),
    ]
    run(command)


def generate_answers_html(book: dict[str, Any], pandoc: Path) -> None:
    output_dir = SITE / "answers"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / "index.html"

    command = pandoc_base_args(book, pandoc) + [
        "--to",
        "html5",
        "--standalone",
        "--template",
        str(TEMPLATES / "chapter.html"),
        "--mathjax",
        "-o",
        str(output),
        str(BACKMATTER / "answers.md"),
    ]
    run(command)

    template = output.read_text(encoding="utf-8")
    replacements = {
        "__BOOK_TITLE__": book["title"],
        "__BOOK_SUBTITLE__": book["subtitle"],
        "__BOOK_AUTHOR__": book["author"],
        "__BOOK_YEAR__": str(book["year"]),
        "__BOOK_LICENSE__": book["license"],
        "__BASE_PATH__": book["base_path"],
        "__PREVIOUS_URL__": f'{book["base_path"]}chapters/12-forms/',
        "__PREVIOUS_LABEL__": "← Alice’s Dream Map",
        "__NEXT_URL__": f'{book["base_path"]}chapters/',
        "__NEXT_LABEL__": "All chapters →",
        "__CHAPTER_POSITION__": "Backmatter",
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    output.write_text(template, encoding="utf-8")


def generate_demo_pages(book: dict[str, Any], chapters: list[dict[str, Any]]) -> None:
    demos = load_json(CONTENT / "demos.json")
    specs = control_specs()

    for demo in demos:
        chapter = next(c for c in chapters if c["demo"] == demo["id"])
        output_dir = SITE / "demos" / demo["id"]
        output_dir.mkdir(parents=True, exist_ok=True)
        output = output_dir / "index.html"

        controls = render_controls(specs[demo["id"]])
        template = (TEMPLATES / "demo.html").read_text(encoding="utf-8")
        replacements = {
            "__BOOK_TITLE__": book["title"],
            "__BOOK_SUBTITLE__": book["subtitle"],
            "__BOOK_AUTHOR__": book["author"],
            "__BOOK_YEAR__": str(book["year"]),
            "__BOOK_LICENSE__": book["license"],
            "__BASE_PATH__": book["base_path"],
            "$title$": demo["title"],
            "$summary$": demo["summary"],
            "$id$": demo["id"],
            "$controls$": controls,
            "$chapter-slug$": chapter["slug"],
        }
        for key, value in replacements.items():
            template = template.replace(key, value)
        output.write_text(template, encoding="utf-8")


def chapter_card(book: dict[str, Any], chapter: dict[str, Any]) -> str:
    return (
        f'<a class="card" href="{book["base_path"]}chapters/{chapter["slug"]}/">'
        f'<span class="part">{chapter["part"]}</span>'
        f'<h3>{chapter["title"]}</h3>'
        f'<p>{chapter["summary"]}</p></a>'
    )


def demo_card(book: dict[str, Any], demo: dict[str, Any]) -> str:
    return (
        f'<a class="card" href="{book["base_path"]}demos/{demo["id"]}/">'
        f'<span class="part">Demo</span>'
        f'<h3>{demo["title"]}</h3>'
        f'<p>{demo["summary"]}</p></a>'
    )


def generate_static_pages(
    book: dict[str, Any],
    chapters: list[dict[str, Any]],
) -> None:
    demos = load_json(CONTENT / "demos.json")
    chapter_cards = "\n".join(chapter_card(book, c) for c in chapters)
    demo_cards = "\n".join(demo_card(book, d) for d in demos)

    pages = {
        "index.html": TEMPLATES / "index.html",
        "chapters/index.html": TEMPLATES / "chapters.html",
        "demos/index.html": TEMPLATES / "demos.html",
        "about/index.html": TEMPLATES / "about.html",
        "glossary/index.html": TEMPLATES / "glossary.html",
    }

    for relative, source in pages.items():
        output = SITE / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        text = source.read_text(encoding="utf-8")
        replacements = {
            "__BOOK_TITLE__": book["title"],
            "__BOOK_SUBTITLE__": book["subtitle"],
            "__BOOK_AUTHOR__": book["author"],
            "__BOOK_DESCRIPTION__": book["description"],
            "__BOOK_YEAR__": str(book["year"]),
            "__BOOK_LICENSE__": book["license"],
            "__REPO_URL__": book["repo_url"],
            "__BASE_PATH__": book["base_path"],
            "__CHAPTER_CARDS__": chapter_cards,
            "__DEMO_CARDS__": demo_cards,
        }
        for key, value in replacements.items():
            text = text.replace(key, value)
        output.write_text(text, encoding="utf-8")

    robots = SITE / "robots.txt"
    robots.write_text(
        "User-agent: *\nAllow: /\n",
        encoding="utf-8",
    )

    sitemap_entries = [
        f"<url><loc>{book['base_url']}</loc></url>",
        f"<url><loc>{book['base_url']}chapters/</loc></url>",
        f"<url><loc>{book['base_url']}demos/</loc></url>",
        f"<url><loc>{book['base_url']}about/</loc></url>",
        f"<url><loc>{book['base_url']}glossary/</loc></url>",
        f"<url><loc>{book['base_url']}answers/</loc></url>",
    ]
    for chapter in chapters:
        sitemap_entries.append(
            f"<url><loc>{book['base_url']}chapters/{chapter['slug']}/</loc></url>"
        )
    for demo in demos:
        sitemap_entries.append(
            f"<url><loc>{book['base_url']}demos/{demo['id']}/</loc></url>"
        )

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(sitemap_entries)
        + "\n</urlset>\n"
    )
    (SITE / "sitemap.xml").write_text(sitemap, encoding="utf-8")

    nojekyll = SITE / ".nojekyll"
    nojekyll.write_text("", encoding="utf-8")


def compile_book(book: dict[str, Any], chapters: list[dict[str, Any]]) -> None:
    book_dir = BUILD / "book"
    main_tex = book_dir / "main.tex"

    chapter_inputs = "\n".join(
        f"\\input{{chapters/{chapter['slug']}.tex}}"
        for chapter in chapters
    )

    template = (TEMPLATES / "book.tex").read_text(encoding="utf-8")
    replacements = {
        "__BOOK_TITLE__": book["title"],
        "__BOOK_SUBTITLE__": book["subtitle"],
        "__BOOK_AUTHOR__": book["author"],
        "__BOOK_DATE__": str(book["year"]),
        "__BOOK_SUBJECT__": book["description"],
        "__BOOK_KEYWORDS__": ", ".join(book["keywords"]),
        "__BOOK_URL__": book["base_url"],
        "__CHAPTER_INPUTS__": chapter_inputs,
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    main_tex.write_text(template, encoding="utf-8")

    pdflatex = shutil.which("pdflatex")
    if not pdflatex:
        raise RuntimeError("pdflatex was not found. Please install a LaTeX distribution.")

    for _ in range(3):
        result = run(
            [pdflatex, "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
            cwd=book_dir,
            check=False,
        )
        if result.returncode != 0:
            log = (book_dir / "main.log")
            if log.exists():
                tail = log.read_text(encoding="utf-8", errors="replace")[-5000:]
                print(tail)
            raise RuntimeError("LaTeX build failed. See the log above.")

    output_pdf = book_dir / "main.pdf"
    download_dir = SITE / "downloads"
    download_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(output_pdf, download_dir / "book.pdf")


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def _directory_hashes(root: Path, patterns: list[str]) -> dict[str, str]:
    files: set[Path] = set()
    for pattern in patterns:
        files.update(path for path in root.glob(pattern) if path.is_file())
    return {
        path.relative_to(root).as_posix(): _hash_file(path)
        for path in sorted(files)
    }


def current_hashes() -> dict[str, dict[str, str]]:
    return {
        "sources": _directory_hashes(ROOT, [
            "content/**/*",
            "templates/**/*",
            "filters/**/*",
            "assets/figures/**/*",
            "assets/story/**/*",
            "assets/css/**/*",
            "assets/js/**/*",
            "scripts/build.py",
            "scripts/make_figures.py",
            "scripts/teaching_figures.py",
        ]),
        "generated": _directory_hashes(ROOT, [
            "site/**/*.html",
            "site/**/*.css",
            "site/**/*.js",
            "site/**/*.svg",
            "site/assets/story/*.png",
            "site/downloads/*.pdf",
            "build/book/main.tex",
            "build/book/backmatter/*.tex",
        ]),
    }


def write_manifest() -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(
        json.dumps(current_hashes(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def verify_manifest() -> None:
    if not MANIFEST.exists():
        raise RuntimeError("No fresh build manifest found. Run: python scripts/build.py all")
    saved = load_json(MANIFEST)
    current = current_hashes()
    for group in ("sources", "generated"):
        if saved.get(group) != current.get(group):
            changed = {
                key
                for key in set(saved.get(group, {})) | set(current.get(group, {}))
                if saved.get(group, {}).get(key) != current.get(group, {}).get(key)
            }
            sample = ", ".join(sorted(changed)[:8])
            raise RuntimeError(
                f"Build is stale ({group}: {len(changed)} changed paths: {sample}). "
                "Run: python scripts/build.py all"
            )


class LocalLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        wanted = {"a": "href", "img": "src", "script": "src", "link": "href", "source": "src"}
        attribute = wanted.get(tag)
        if not attribute:
            return
        value = dict(attrs).get(attribute)
        if value:
            self.urls.append(value)


def validate_local_links(book: dict[str, Any]) -> None:
    broken: list[str] = []
    for page in sorted(SITE.rglob("*.html")):
        parser = LocalLinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for url in parser.urls:
            if url.startswith(("http://", "https://", "mailto:", "data:", "#")):
                continue
            clean = url.split("#", 1)[0].split("?", 1)[0]
            if not clean:
                continue
            if clean.startswith(book["base_path"]):
                target = SITE / clean[len(book["base_path"]):]
            elif clean.startswith("/"):
                target = SITE / clean.lstrip("/")
            else:
                target = (page.parent / clean).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                broken.append(f"{page.relative_to(SITE)} -> {url}")

    if broken:
        raise ValueError("Broken local links:\n" + "\n".join(broken[:30]))


def validate_latex_log() -> None:
    log_path = BUILD / "book" / "main.log"
    if not log_path.exists():
        raise FileNotFoundError("LaTeX log is missing.")
    log = log_path.read_text(encoding="utf-8", errors="replace")
    problems = []
    for pattern, message in [
        ("Overfull \\hbox", "overfull horizontal box"),
        ("Float too large", "float too large"),
        ("multiply-defined labels", "duplicate LaTeX labels"),
        ("LaTeX Warning: Label", "LaTeX label warning"),
        ("destination with the same identifier", "duplicate PDF destination"),
    ]:
        if pattern.lower() in log.lower():
            problems.append(message)
    if problems:
        raise ValueError("LaTeX quality check failed: " + ", ".join(problems))


def validate(book: dict[str, Any], chapters: list[dict[str, Any]]) -> None:
    demos = load_json(CONTENT / "demos.json")
    demo_ids = {d["id"] for d in demos}
    chapter_demos = {c["demo"] for c in chapters}

    if demo_ids != chapter_demos:
        raise ValueError("Chapter demos and demo metadata do not match.")

    answer_source = (BACKMATTER / "answers.md").read_text(encoding="utf-8")
    answer_sections = {
        int(number): body for number, body in re.findall(
            r"## Chapter (\d+):[^\n]*\n(.*?)(?=\n## Chapter |\Z)",
            answer_source, flags=re.DOTALL,
        )
    }
    for number, chapter in enumerate(chapters, 1):
        source = chapter["path"].read_text(encoding="utf-8")
        exercises = re.search(r"::: \{\.trythis\}\n(.*?)\n:::", source, re.DOTALL)
        if not exercises:
            raise ValueError(f"No exercises in {chapter['slug']}")
        exercise_numbers = re.findall(r"^(\d+)\. ", exercises.group(1), re.MULTILINE)
        answer_body = answer_sections.get(number, "")
        answer_numbers = re.findall(r"^### Exercise (\d+)$", answer_body, re.MULTILINE)
        expected = [str(i) for i in range(1, len(exercise_numbers) + 1)]
        if exercise_numbers != expected or answer_numbers != expected:
            raise ValueError(f"Exercise/answer numbering mismatch in chapter {number}")
        if answer_body.count("::: {.hint}") != len(expected) or answer_body.count("::: {.answer}") != len(expected):
            raise ValueError(f"Missing hint or answer in chapter {number}")

    for chapter in chapters:
        path = SITE / "chapters" / chapter["slug"] / "index.html"
        story_path = f"assets/story/{chapter['slug']}.png"
        if chapter.get("story-image") != story_path or not chapter.get("story-alt"):
            raise ValueError(f"Missing chapter-opening artwork metadata in {chapter['slug']}")
        story = ROOT / story_path
        if not story.exists() or not story.stat().st_size:
            raise FileNotFoundError(f"Missing chapter-opening artwork: {story}")
        source = chapter["path"].read_text(encoding="utf-8")
        references = re.findall(r"assets/figures/([a-z0-9-]+)\.svg", source)
        expected = set(FIGURE_NAMES[chapter["slug"]])
        if len(references) != len(set(references)) or not expected.issubset(references):
            raise ValueError(f"Missing or duplicate teaching figures in {chapter['slug']}")
        for name in references:
            for suffix in (".svg", ".pdf"):
                figure = ASSETS / "figures" / (name + suffix)
                if not figure.exists() or not figure.stat().st_size:
                    raise FileNotFoundError(f"Missing figure: {figure}")
        if not path.exists():
            raise FileNotFoundError(f"Missing chapter page: {path}")
        html = path.read_text(encoding="utf-8")
        if f'src="{book["base_path"]}{story_path}"' not in html:
            raise ValueError(f"Chapter-opening artwork missing from {path}")
        if chapter["title"] not in html:
            raise ValueError(f"Chapter title missing from {path}")
        if "mathjax" not in html.lower():
            raise ValueError(f"MathJax missing from {path}")
        if "<figure" not in html and "<img" not in html:
            raise ValueError(f"Chapter figure missing from {path}")
        if f'href="{book["base_path"]}answers/"' not in html:
            raise ValueError(f"Answers link missing from {path}")

    for demo in demos:
        path = SITE / "demos" / demo["id"] / "index.html"
        if not path.exists():
            raise FileNotFoundError(f"Missing demo page: {path}")
        html = path.read_text(encoding="utf-8")
        if demo["title"] not in html:
            raise ValueError(f"Demo title missing from {path}")
        if f'id="{demo["id"]}"' not in html:
            raise ValueError(f"Demo canvas missing from {path}")

    answers_path = SITE / "answers" / "index.html"
    if not answers_path.exists():
        raise FileNotFoundError("Missing answers page.")
    answers_html = answers_path.read_text(encoding="utf-8")
    if "Hints and Answers" not in answers_html:
        raise ValueError("Answers title missing from answers page.")
    if "mathjax" not in answers_html.lower():
        raise ValueError("MathJax missing from answers page.")

    pdf = SITE / "downloads" / "book.pdf"
    if not pdf.exists() or pdf.stat().st_size == 0:
        raise FileNotFoundError("Generated book PDF is missing or empty.")

    for demo in demos:
        qr = BUILD / "book" / "assets" / "qr" / f"{demo['id']}.png"
        if not qr.exists():
            raise FileNotFoundError(f"Missing QR code: {qr}")

    oxford_mentions = sum(
        len(re.findall(r"\bOxford\b", path.read_text(encoding="utf-8"), flags=re.IGNORECASE))
        for path in CONTENT.rglob("*.md")
    )
    if oxford_mentions != 4:
        raise ValueError(f"Expected exactly four Oxford flashbacks, found {oxford_mentions}.")

    node = shutil.which("node")
    if not node:
        raise RuntimeError("node was not found. Node.js is required for JavaScript syntax checks.")
    for script in [ASSETS / "js" / "demos.js", ASSETS / "js" / "site.js"]:
        run([node, "--check", str(script)], check=True)

    validate_local_links(book)
    validate_latex_log()

    print("Build and validation passed.")


def build_all(book: dict[str, Any]) -> None:
    generate_all()
    ensure_clean(BUILD)
    ensure_clean(SITE)

    copy_assets(book)
    make_cover(book)

    chapters = chapter_metadata()
    pandoc = find_pandoc()

    generate_answers_tex(book, pandoc)
    for chapter in chapters:
        generate_chapter_tex(book, pandoc, chapter)
        generate_chapter_html(book, pandoc, chapter, chapters)

    generate_answers_html(book, pandoc)
    generate_demo_pages(book, chapters)
    generate_static_pages(book, chapters)
    compile_book(book, chapters)
    validate(book, chapters)
    write_manifest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the book and website.")
    parser.add_argument(
        "target",
        choices=["all", "check"],
        nargs="?",
        default="all",
    )
    args = parser.parse_args()

    book = load_json(CONTENT / "book.json")

    if args.target == "check":
        verify_manifest()
        chapters = chapter_metadata()
        validate(book, chapters)
        return 0

    build_all(book)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
