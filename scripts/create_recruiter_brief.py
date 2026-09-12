"""Build the recruiter-facing FranceScope brief as a compact PDF."""

from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
CHARTS = ROOT / "outputs" / "charts"
PDF_PATH = REPORTS / "FranceScope_AI_Recruiter_Brief.pdf"
QA_DIR = REPORTS / "_brief_qa"
QA_DIR.mkdir(parents=True, exist_ok=True)

GREEN = "#2A9D8F"
AMBER = "#E9C46A"
CORAL = "#E76F51"
INK = "#1F2933"
MUTED = "#59636E"
PALE = "#F4F7F9"
BLUE = "#264653"

plt.rcParams.update({"font.family": "DejaVu Sans", "figure.facecolor": "white"})


def page_base(number: int, section: str):
    fig = plt.figure(figsize=(11.69, 8.27))
    fig.patch.set_facecolor("white")
    fig.text(0.06, 0.955, "FRANCESCOPE AI  ·  BRIEF RECRUTEUR", fontsize=8, color=MUTED, weight="bold")
    fig.text(0.94, 0.955, f"{number:02d}", fontsize=8, color=MUTED, ha="right", weight="bold")
    fig.text(0.06, 0.035, section, fontsize=7.5, color=MUTED)
    fig.text(0.94, 0.035, "V8 · sorties publiques gelées", fontsize=7.5, color=MUTED, ha="right")
    return fig


def title(fig, text: str, subtitle: str | None = None):
    fig.text(0.06, 0.885, text, fontsize=25, color=INK, weight="bold")
    if subtitle:
        fig.text(0.06, 0.845, subtitle, fontsize=11.5, color=MUTED)


def box(fig, x, y, w, h, heading, body, color=BLUE):
    fig.patches.append(
        FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.012",
            transform=fig.transFigure, facecolor=PALE, edgecolor="#D8E0E6", linewidth=0.8,
        )
    )
    fig.text(x + 0.018, y + h - 0.035, heading, fontsize=10, color=color, weight="bold")
    fig.text(x + 0.018, y + h - 0.075, body, fontsize=9.2, color=INK, va="top", linespacing=1.35)


def add_chart(fig, filename, rect):
    ax = fig.add_axes(rect)
    ax.imshow(mpimg.imread(CHARTS / filename))
    ax.axis("off")
    return ax


def page_cover():
    fig = page_base(1, "Présentation rapide")
    fig.text(0.06, 0.78, "FranceScope AI", fontsize=39, color=INK, weight="bold")
    fig.text(0.06, 0.715, "Prévisions macroéconomiques de long terme sur la France, assistées par LLM",
             fontsize=15, color=BLUE)
    fig.text(0.06, 0.605,
             "Un cadre de scénarios centré sur trois résultats :\n"
             "chômage, PIB réel par habitant et niveau de vie médian réel.\n\n"
             "Un cas d’étude sur la manière de rendre des workflows LLM longs\n"
             "plus fiables grâce au context engineering, aux évaluations adversariales,\n"
             "à la provenance des sources et au contrôle human-in-the-loop.",
             fontsize=13, color=INK, va="top", linespacing=1.55)
    for x, label, color in [(0.09, "EMPLOI", GREEN), (0.39, "PRODUCTION", AMBER), (0.73, "NIVEAU DE VIE\nDISTRIBUÉ", CORAL)]:
        fig.text(x, 0.30, label, fontsize=13, color=color, weight="bold", ha="center", va="center")
    fig.text(0.24, 0.30, "+", fontsize=22, color=MUTED, ha="center")
    fig.text(0.61, 0.30, "+", fontsize=22, color=MUTED, ha="center")
    box(fig, 0.06, 0.11, 0.88, 0.095, "Projet itératif multi-semaines",
        "Recherche · data · forecasting · LLM orchestration · évaluation · validation", GREEN)
    fig.text(0.06, 0.25, "Python  ·  Pandas  ·  Matplotlib  ·  VS Code  ·  Git/GitHub  ·  CSV/JSON/Markdown",
             fontsize=9.5, color=MUTED)
    return fig


def page_results():
    fig = page_base(2, "Résultats produits")
    title(fig, "Ce que le projet produit", "Trois cibles · trois scénarios conditionnels · une lecture sans indice composite")
    ax = fig.add_axes([0.06, 0.49, 0.88, 0.30])
    ax.axis("off")
    table = ax.table(
        cellText=[
            ["Chômage", "7,725 %", "12,0 %", "14,0 %", "17,8 %"],
            ["PIB réel par habitant", "38 360 €", "36 500 €", "34 000 €", "30 000 €"],
            ["Niveau de vie médian réel", "25 952,51 €", "24 700 €", "23 300 €", "20 800 €"],
        ],
        colLabels=["Indicateur", "2025", "Faible 2050", "Central 2050", "Forte 2050"],
        colWidths=[0.32, 0.14, 0.18, 0.18, 0.18],
        cellLoc="center", loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.0)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor("#D8E0E6")
        if r == 0:
            cell.set_facecolor(BLUE)
            cell.get_text().set_color("white")
            cell.get_text().set_weight("bold")
        elif c == 0:
            cell.set_facecolor(PALE)
            cell.get_text().set_weight("bold")
        elif c == 2:
            cell.set_facecolor("#E5F3F0")
        elif c == 3:
            cell.set_facecolor("#FFF4D6")
        elif c == 4:
            cell.set_facecolor("#FCE5DE")
    add_chart(fig, "final_scenario_comparison.png", [0.06, 0.09, 0.88, 0.34])
    return fig


def page_institutions():
    fig = page_base(3, "Références institutionnelles")
    title(fig, "Comparer sans mélanger les natures de preuve",
          "Les institutions et FranceScope répondent à des questions différentes")
    add_chart(fig, "institutional_unemployment.png", [0.06, 0.34, 0.88, 0.49])
    box(fig, 0.06, 0.10, 0.27, 0.17, "Références", "2026 : 8,2 %\n2027 : 8,4 %\nBdF 2028 : 7,8 %", BLUE)
    box(fig, 0.365, 0.10, 0.27, 0.17, "CE long terme", "2030 : 7,1 %\n2040 : 6,7 %\n2050 : 6,3 %", MUTED)
    box(fig, 0.67, 0.10, 0.27, 0.17, "Politique de données", "GDPpc : pas de niveau comparable\nMédian : pas de forecast comparable\nNA > fausse précision", CORAL)
    return fig


def page_llm():
    fig = page_base(4, "LLM engineering")
    title(fig, "Le vrai défi : rendre les LLM fiables sur un projet long")
    rows = [
        ("Dérive du modèle", "Objectif explicite + scope"),
        ("Répétition d'échecs", "Anti-loop rules"),
        ("Exploration infinie", "Bounded exploration"),
        ("Gaspillage de tokens", "Targeted reads"),
        ("Perte d'état", "Frozen decisions + handoffs"),
        ("Sorties incohérentes", "Temporal + cross-variable evals"),
        ("Biais d'un modèle", "Adversarial multi-model review"),
        ("Sources mal interprétées", "Provenance gates"),
        ("Over-editing", "Smallest safe change + stop conditions"),
    ]
    ax = fig.add_axes([0.06, 0.29, 0.52, 0.51])
    ax.axis("off")
    table = ax.table(cellText=rows, colLabels=["Problème observé", "Réponse d'ingénierie"],
                     colWidths=[0.47, 0.53], cellLoc="left", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(9.2)
    table.scale(1, 1.65)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor("#D8E0E6")
        if r == 0:
            cell.set_facecolor(BLUE); cell.get_text().set_color("white"); cell.get_text().set_weight("bold")
        elif r % 2 == 0:
            cell.set_facecolor(PALE)
    box(fig, 0.65, 0.56, 0.29, 0.20, "Principe directeur",
        "Le principal défi n'était pas d'obtenir une bonne réponse une fois.\n\n"
        "Il fallait maintenir la cohérence du système pendant plusieurs semaines.", CORAL)
    box(fig, 0.65, 0.29, 0.29, 0.18, "Workflow contrôlé",
        "Données → sources → recherche → forecasts → evals → critique → revision gate → sorties gelées", GREEN)
    return fig


def page_evolution():
    fig = page_base(5, "Évolution de l'architecture")
    title(fig, "De la complexité à la robustesse")
    steps = [
        ("V1–V7", "Simulateur causal large"),
        ("→", "Variables intermédiaires nombreuses"),
        ("→", "Incertitude composée / validation difficile"),
        ("V8", "Trois cibles finales"),
        ("→", "Evals temporelles + cross-variable"),
        ("→", "Revue adversariale multi-modèles"),
        ("→", "Index retiré · benchmark · provenance"),
    ]
    y = 0.73
    for i, (head, body) in enumerate(steps):
        color = [CORAL, MUTED, MUTED, GREEN, MUTED, MUTED, BLUE][i]
        fig.patches.append(FancyBboxPatch((0.12, y), 0.76, 0.075, boxstyle="round,pad=0.01",
                                          transform=fig.transFigure, facecolor="#F4F7F9",
                                          edgecolor="#D8E0E6"))
        fig.text(0.15, y + 0.038, head, fontsize=11, weight="bold", color=color, va="center")
        fig.text(0.30, y + 0.038, body, fontsize=11, color=INK, va="center")
        y -= 0.095
    box(fig, 0.12, 0.12, 0.76, 0.13, "Décision d'architecture",
        "Le projet est devenu meilleur en devenant plus simple.\n"
        "La compétence clé a été de savoir abandonner une complexité devenue indéfendable.", GREEN)
    return fig


def page_role():
    fig = page_base(6, "Responsabilité humaine")
    title(fig, "Mon rôle", "Le workflow est human-directed and machine-accelerated, pas model-autonomous")
    box(fig, 0.06, 0.52, 0.41, 0.27, "J'ai conçu",
        "• l'architecture des scénarios\n• la sélection des trois cibles\n• les critères de cohérence\n"
        "• les règles de context engineering\n• les gates de validation\n• la provenance et les pivots", GREEN)
    box(fig, 0.53, 0.52, 0.41, 0.27, "J'ai décidé",
        "• quelles preuves retenir\n• quand réorienter l'IA\n• quoi geler ou rouvrir\n"
        "• de retirer l'Index composite\n• de refuser les trajectoires institutionnelles non comparables", CORAL)
    box(fig, 0.06, 0.20, 0.41, 0.21, "Les LLM ont accéléré",
        "Recherche · code · extraction de données · critique · synthèse · documentation", BLUE)
    box(fig, 0.53, 0.20, 0.41, 0.21, "Responsabilité conservée",
        "Architecture · jugement sur les sources · cohérence globale · acceptation finale · décisions de risque", AMBER)
    return fig


def page_skills():
    fig = page_base(7, "Compétences et ressources")
    title(fig, "Compétences démontrées")
    skills = [
        ("Context engineering", "scope · contexte · état gelé · handoffs", GREEN),
        ("Agent control", "anti-loop · exploration bornée · stop conditions", CORAL),
        ("Evaluation engineering", "temporal · cross-variable · adversarial review", BLUE),
        ("Multi-model orchestration", "critiques indépendantes · hypothèses", AMBER),
        ("Source / provenance", "sources primaires · typage · horizon · NA", GREEN),
        ("Software / data engineering", "Python · CSV · validation · graphiques", BLUE),
        ("Jugement human-in-the-loop", "architecture · simplification · risques", CORAL),
    ]
    positions = [(0.06, 0.67), (0.53, 0.67), (0.06, 0.51), (0.53, 0.51), (0.06, 0.35), (0.53, 0.35), (0.06, 0.19)]
    for (heading, body, color), (x, y) in zip(skills, positions):
        box(fig, x, y, 0.41, 0.12, heading, body, color)
    fig.text(0.53, 0.27, "Pour aller plus loin", fontsize=12, color=BLUE, weight="bold")
    fig.text(0.53, 0.17,
             "README · rapport technique · workflows LLM fiables\n"
             "évolution du projet · cadre d'évaluation\n"
             "méthodologie institutionnelle",
             fontsize=10, color=INK, linespacing=1.6)
    fig.text(0.06, 0.09,
             "FranceScope n'est pas seulement un projet de forecasting. C'est un cas d'étude sur la transformation de LLM puissants mais imparfaits en workflow contrôlé, auditable et orienté résultat.",
             fontsize=10.5, color=INK, style="italic")
    return fig


def main():
    pages = [page_cover, page_results, page_institutions, page_llm, page_evolution, page_role, page_skills]
    with PdfPages(PDF_PATH) as pdf:
        for index, builder in enumerate(pages, start=1):
            fig = builder()
            pdf.savefig(fig, dpi=180, bbox_inches="tight")
            fig.savefig(QA_DIR / f"page_{index:02d}.png", dpi=120, bbox_inches="tight")
            plt.close(fig)


if __name__ == "__main__":
    main()
