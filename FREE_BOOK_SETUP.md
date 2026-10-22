# Publish the free book with GitHub Pages

The complete PDF, all twelve chapters, answers, and demos are openly accessible.
No email, payment account, Cloudflare, server, or API keys are needed.

## Build

Install Python dependencies, Pandoc, Node.js (for the existing book build), and
LaTeX. Then run:

```powershell
python scripts/build.py all
python scripts/build_pages.py
```

The public files are in `build/public/`. To reuse the already built PDF, only the
second command is needed. Do not publish the entire workspace: it contains local
configuration and older inactive experiments.

## Publish

Repository: https://github.com/FyodorAmanov1/multilinear-algebra-book

Website: https://fyodoramanov1.github.io/multilinear-algebra-book/

In repository Settings > Pages, choose **GitHub Actions** as the source. Push the
book sources and `.github/workflows/pages.yml` to `main` or `master`. The workflow
builds the book and uploads only `build/public/`, then deploys it to GitHub Pages.
No third-party hosting credentials are required. The PDF is generated in Actions
rather than committed to Git.

The homepage describes the free first volume and the planned series explaining
math and science through stories. Future volumes are described as planned paid
releases, without invented titles or dates. Visitors can share feedback through
the repository's Issues page.

## Email collection

This version does not collect email addresses or show a signup form. GitHub Pages
cannot privately save addresses or deliver access emails by itself. A mailing
service can be added later if desired; the first book stays openly accessible.

## Prior experiments

`commerce/`, `functions/`, `wrangler.toml`, and `scripts/build_store.py` are inactive
local experiments. GitHub Pages does not run them, and `build_pages.py` does not
copy their email or payment scripts into the published website.
