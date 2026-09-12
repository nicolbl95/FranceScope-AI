"""Render the validated FranceScope technical report Markdown as a PDF."""

from pathlib import Path
import re
import textwrap

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "technical_report.md"
OUTPUT = ROOT / "reports" / "FranceScope_V8_Technical_Report.pdf"
QA_DIR = ROOT / "reports" / "_technical_report_qa"
QA_DIR.mkdir(parents=True, exist_ok=True)

INK = "#1F2933"
MUTED = "#59636E"
BLUE = "#264653"
PALE = "#F4F7F9"

plt.rcParams.update({"font.family": "DejaVu Sans", "figure.facecolor": "white"})


class Renderer:
    def __init__(self, pdf):
        self.pdf = pdf
        self.page = 0
        self.fig = None
        self.y = 0.91
        self.start_page()

    def start_page(self):
        self.page += 1
        self.fig = plt.figure(figsize=(11.69, 8.27))
        self.fig.text(0.06, 0.955, "FRANCESCOPE V8  ·  RAPPORT TECHNIQUE", fontsize=8, color=MUTED, weight="bold")
        self.fig.text(0.94, 0.955, f"{self.page:02d}", fontsize=8, color=MUTED, ha="right", weight="bold")
        self.fig.text(0.06, 0.035, "Cadre final à trois cibles · scénarios conditionnels", fontsize=7.5, color=MUTED)
        self.fig.text(0.94, 0.035, "FranceScope AI", fontsize=7.5, color=MUTED, ha="right")
        self.y = 0.91

    def finish_page(self):
        self.pdf.savefig(self.fig, dpi=180, bbox_inches="tight")
        self.fig.savefig(QA_DIR / f"page_{self.page:02d}.png", dpi=100, bbox_inches="tight")
        plt.close(self.fig)

    def new_page(self):
        self.finish_page()
        self.start_page()

    def ensure(self, height):
        if self.y - height < 0.09:
            self.new_page()

    def write(self, text, size=9.2, color=INK, weight="normal", style="normal", gap=0.018):
        lines = textwrap.wrap(text, width=112, break_long_words=False, break_on_hyphens=False) or [""]
        height = 0.027 * len(lines) + gap
        self.ensure(height)
        self.fig.text(0.06, self.y, "\n".join(lines), fontsize=size, color=color,
                      weight=weight, style=style, va="top", linespacing=1.25)
        self.y -= height

    def heading(self, text, level):
        if level == 1:
            self.ensure(0.08)
            self.fig.text(0.06, self.y, text, fontsize=23, color=INK, weight="bold", va="top")
            self.y -= 0.075
        elif level == 2:
            self.ensure(0.065)
            self.fig.text(0.06, self.y, text, fontsize=16, color=BLUE, weight="bold", va="top")
            self.y -= 0.055
        else:
            self.ensure(0.05)
            self.fig.text(0.06, self.y, text, fontsize=11.5, color=BLUE, weight="bold", va="top")
            self.y -= 0.04

    def image(self, path, caption):
        image = mpimg.imread(path)
        height_ratio = image.shape[0] / image.shape[1]
        height = min(0.36, 0.79 * height_ratio)
        self.ensure(height + 0.07)
        ax = self.fig.add_axes([0.105, self.y - height, 0.79, height])
        ax.imshow(image)
        ax.axis("off")
        self.y -= height + 0.025
        self.write(caption, size=8.5, color=MUTED, style="italic", gap=0.025)


def render():
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    with PdfPages(OUTPUT) as pdf:
        renderer = Renderer(pdf)
        for raw in lines:
            line = raw.strip()
            if not line:
                renderer.y -= 0.012
                continue
            if line.startswith("# "):
                renderer.heading(line[2:], 1)
            elif line.startswith("### "):
                renderer.heading(line[4:], 3)
            elif line.startswith("## "):
                renderer.heading(line[3:], 2)
            elif line.startswith("!["):
                match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
                if match:
                    path = (SOURCE.parent / match.group(2)).resolve()
                    renderer.image(path, match.group(1))
            elif line.startswith("> "):
                renderer.write(line[2:], size=10.5, color=BLUE, style="italic", gap=0.025)
            elif line.startswith("|"):
                renderer.write(line, size=8.1, color=INK, gap=0.006)
            elif line.startswith("- ") or re.match(r"^\d+\.", line):
                renderer.write("• " + re.sub(r"^\d+\.\s*", "", line[2:] if line.startswith("- ") else line), size=9.0, gap=0.006)
            elif line.startswith("```"):
                renderer.write(line, size=8.5, color=MUTED, gap=0.008)
            else:
                renderer.write(line, size=9.2, gap=0.009)
        renderer.finish_page()


if __name__ == "__main__":
    render()
