"""Build the FranceScope LLM engineering case study PDF."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
PDF_PATH = REPORTS / "FranceScope_LLM_Engineering_Case_Study.pdf"
QA_DIR = REPORTS / "_case_study_qa"
QA_DIR.mkdir(parents=True, exist_ok=True)

INK = "#1F2933"
MUTED = "#59636E"
PALE = "#F4F7F9"
BLUE = "#264653"
GREEN = "#2A9D8F"
AMBER = "#E9C46A"
CORAL = "#E76F51"

plt.rcParams.update({"font.family": "DejaVu Sans", "figure.facecolor": "white"})


def base(page, section):
    fig = plt.figure(figsize=(11.69, 8.27))
    fig.text(0.06, 0.955, "FRANCESCOPE  ·  ÉTUDE DE CAS LLM ENGINEERING", fontsize=8, color=MUTED, weight="bold")
    fig.text(0.94, 0.955, f"{page:02d}", fontsize=8, color=MUTED, ha="right", weight="bold")
    fig.text(0.06, 0.035, section, fontsize=7.5, color=MUTED)
    fig.text(0.94, 0.035, "V8 · workflow human-directed", fontsize=7.5, color=MUTED, ha="right")
    return fig


def heading(fig, text, subtitle=None):
    fig.text(0.06, 0.885, text, fontsize=25, color=INK, weight="bold")
    if subtitle:
        fig.text(0.06, 0.845, subtitle, fontsize=11.5, color=MUTED)


def box(fig, x, y, w, h, title, text, color=BLUE, size=9.5):
    fig.patches.append(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.012",
                                      transform=fig.transFigure, facecolor=PALE,
                                      edgecolor="#D8E0E6", linewidth=0.8))
    fig.text(x + 0.018, y + h - 0.035, title, fontsize=10, color=color, weight="bold")
    fig.text(x + 0.018, y + h - 0.075, text, fontsize=size, color=INK, va="top", linespacing=1.35)


def table(fig, rect, rows, headers, widths=None, fontsize=9):
    ax = fig.add_axes(rect)
    ax.axis("off")
    t = ax.table(cellText=rows, colLabels=headers, colWidths=widths, cellLoc="left", loc="center")
    t.auto_set_font_size(False)
    t.set_fontsize(fontsize)
    t.scale(1, 1.6)
    for (r, c), cell in t.get_celld().items():
        cell.set_edgecolor("#D8E0E6")
        if r == 0:
            cell.set_facecolor(BLUE)
            cell.get_text().set_color("white")
            cell.get_text().set_weight("bold")
        elif r % 2 == 0:
            cell.set_facecolor(PALE)
    return t


def page_cover():
    fig = base(1, "Présentation")
    fig.text(0.06, 0.77, "FranceScope —\nÉtude de cas LLM Engineering", fontsize=32, color=INK, weight="bold", linespacing=1.15)
    fig.text(0.06, 0.62, "Context engineering, contrôle des agents, évaluation et orchestration humain–IA",
             fontsize=14, color=BLUE)
    fig.text(0.06, 0.49,
             "FranceScope est devenu un laboratoire pratique pour apprendre à transformer\n"
             "des LLM puissants mais imparfaits en un workflow long, contrôlé,\n"
             "traçable et orienté résultat.",
             fontsize=14, color=INK, linespacing=1.6)
    for x, label, color in [(0.12, "CONTEXTE", GREEN), (0.38, "CONTRÔLE", CORAL),
                            (0.64, "ÉVALUATION", AMBER), (0.86, "JUGEMENT\nHUMAIN", BLUE)]:
        fig.text(x, 0.25, label, fontsize=11, color=color, weight="bold", ha="center", va="center")
    fig.text(0.06, 0.12, "Python · Pandas · Matplotlib · CSV/JSON/Markdown · VS Code · Git/GitHub · workflows multi-modèles",
             fontsize=9.5, color=MUTED)
    return fig


def page_problem():
    fig = base(2, "Le problème d'ingénierie")
    heading(fig, "Le problème n'était pas une réponse isolée", "Il fallait maintenir la cohérence sur de nombreuses sessions")
    fig.text(0.06, 0.70,
             "Direction · état · scope · qualité · intégrité des sources · discipline d'exécution",
             fontsize=15, color=BLUE, weight="bold")
    box(fig, 0.06, 0.39, 0.40, 0.20, "Échelle locale", "Une réponse peut être brillante, plausible et utile pour la dernière question.", GREEN)
    box(fig, 0.54, 0.39, 0.40, 0.20, "Échelle projet", "Conserver décisions, définitions et limites pendant plusieurs semaines.", CORAL)
    fig.text(0.06, 0.22,
             "Un LLM peut être très intelligent localement tout en étant peu fiable à l'échelle d'un projet de plusieurs semaines.",
             fontsize=14, color=INK, style="italic")
    return fig


def page_failures():
    fig = base(3, "Échecs observés")
    heading(fig, "Les modes d'échec qui ont changé le workflow")
    rows = [
        ("Dérive du modèle", "La dernière tâche prend le dessus sur l'objectif."),
        ("Perte d'état", "Une décision gelée redevient une question ouverte."),
        ("Approche ratée répétée", "Temps et tokens sans information nouvelle."),
        ("Boucle d'exploration", "Recherche prolongée sans réduction d'incertitude."),
        ("Action hors scope", "Risque de régression sans pouvoir de décision."),
        ("Surédition", "Une modification après validation réintroduit un défaut."),
        ("Plausibilité locale", "Des sorties séparées deviennent globalement incompatibles."),
        ("Confusion de source", "Un taux est pris pour un niveau comparable."),
        ("Forecast / projection", "Des objets méthodologiquement différents sont fusionnés."),
    ]
    table(fig, [0.06, 0.17, 0.88, 0.62], rows, ["Échec", "Risque concret"], [0.28, 0.72], 9)
    return fig


def page_context():
    fig = base(4, "Context engineering")
    heading(fig, "Du prompt au context engineering", "Le prompt est une partie du système, pas le système entier")
    table(fig, [0.06, 0.32, 0.88, 0.42],
          [("Écrire une meilleure instruction", "Contrôler l'état autoritatif"),
           ("Ajouter du contexte", "Sélectionner le contexte pertinent"),
           ("Demander une réponse", "Définir actions, fichiers et scope"),
           ("Continuer jusqu'à satisfaction", "Fixer des gates et des conditions d'arrêt"),
           ("Faire confiance à la sortie", "Tracer la provenance et tester la cohérence")],
          ["Approche initiale", "Pratique mature"], [0.46, 0.54], 10)
    box(fig, 0.06, 0.13, 0.88, 0.12, "Système contrôlé",
        "Etat gelé · scope · fichiers autorisés · provenance · évaluation · handoffs", GREEN)
    return fig


def page_antiloop():
    fig = base(5, "Contrôle opérationnel")
    heading(fig, "Anti-loop, changement de stratégie et exploration bornée")
    box(fig, 0.06, 0.56, 0.88, 0.16, "Règle 1", "Never repeat the exact same failed tool call.", CORAL, 12)
    box(fig, 0.06, 0.34, 0.88, 0.16, "Règle 2",
        "If an approach fails twice without measurable progress, change hypothesis, tool, command, file, or implementation strategy.",
        BLUE, 11)
    box(fig, 0.06, 0.12, 0.27, 0.14, "Exploration bornée", "Sources définies · lectures capées · stop condition", GREEN)
    box(fig, 0.365, 0.12, 0.27, 0.14, "Pertinence", "Chaque appel d'outil doit avancer la tâche", AMBER)
    box(fig, 0.67, 0.12, 0.27, 0.14, "Tokens", "Moins de contexte, mieux sélectionné", BLUE)
    return fig


def page_state():
    fig = base(6, "Etat et discipline")
    heading(fig, "Scope, état gelé, handoffs et arrêt")
    box(fig, 0.06, 0.56, 0.27, 0.20, "Scope", "Workspace actif\nFichiers autorisés\nMode : recherche / édition / validation / présentation", GREEN)
    box(fig, 0.365, 0.56, 0.27, 0.20, "Etat gelé", "Couche validée\nautoritative\nRéouverture seulement via revue formelle", CORAL)
    box(fig, 0.67, 0.56, 0.27, 0.20, "Smallest safe change", "Corriger le problème démontré\nRéduire les régressions\nFaciliter l'audit", AMBER)
    box(fig, 0.06, 0.23, 0.41, 0.18, "Handoff structuré",
        "PROJECT_VERSION · VALUES_CHANGED · FILES_UPDATED\nVALIDATION · VERDICT · NEXT_ACTION", BLUE, 9)
    box(fig, 0.53, 0.23, 0.41, 0.18, "Stop conditions",
        "Pas d'audit après validation\nPas de refactorisation opportuniste\nPas de réouverture d'un sujet gelé", GREEN, 9)
    fig.text(0.06, 0.12, "Les conditions d'arrêt font partie de la spécification.", fontsize=13, color=INK, style="italic")
    return fig


def page_eval():
    fig = base(7, "Evaluation engineering")
    heading(fig, "De la génération à la décision")
    fig.text(0.10, 0.71, "generate  →  accept", fontsize=18, color=MUTED, weight="bold")
    fig.text(0.10, 0.59, "generate  →  test  →  revise / reject / freeze", fontsize=20, color=GREEN, weight="bold")
    box(fig, 0.06, 0.26, 0.26, 0.20, "Intégrité", "Données · valeurs · formats · manifests", BLUE)
    box(fig, 0.37, 0.26, 0.26, 0.20, "Cohérence", "Scénarios · horizons · temporal · cross-variable", GREEN)
    box(fig, 0.68, 0.26, 0.26, 0.20, "Provenance", "Sources · classification · traceabilité · revue adversariale", CORAL)
    fig.text(0.06, 0.15, "Le modèle générait des candidats ; le framework décidait s'ils étaient acceptables.",
             fontsize=13, color=INK, style="italic")
    return fig


def page_multimodel():
    fig = base(8, "Critique et provenance")
    heading(fig, "Revue adversariale et raisonnement orienté provenance")
    fig.text(0.08, 0.72, "candidat", fontsize=12, color=GREEN, weight="bold")
    fig.text(0.23, 0.72, "→", fontsize=20, color=MUTED)
    fig.text(0.30, 0.72, "critique externe", fontsize=12, color=CORAL, weight="bold")
    fig.text(0.49, 0.72, "→", fontsize=20, color=MUTED)
    fig.text(0.56, 0.72, "hypothèse testable", fontsize=12, color=BLUE, weight="bold")
    fig.text(0.75, 0.72, "→  revision gate", fontsize=12, color=AMBER, weight="bold")
    box(fig, 0.06, 0.39, 0.40, 0.20, "Pas un vote", "Des modèles indépendants critiquent.\nLe désaccord est utile lorsqu'il devient un test reproductible.", CORAL)
    box(fig, 0.54, 0.39, 0.40, 0.20, "Taxonomie des sources",
        "OBSERVED · DIRECT_FORECAST\nLONG_RUN_PROJECTION\nSTRUCTURAL_ASSUMPTION · DERIVED_PROXY", BLUE, 8.8)
    box(fig, 0.06, 0.14, 0.88, 0.13, "Champs contrôlés",
        "Source · date · variable exacte · type · horizon · justification · confiance · transformations", GREEN)
    return fig


def page_semantics():
    fig = base(9, "Sémantique des données")
    heading(fig, "Quand un calcul juste produit une conclusion fausse")
    box(fig, 0.06, 0.55, 0.26, 0.20, "Source", "Jalons CE de croissance GDPpc", BLUE)
    box(fig, 0.37, 0.55, 0.26, 0.20, "Transformation", "Composition mathématique possible", AMBER)
    box(fig, 0.68, 0.55, 0.26, 0.20, "Erreur", "Taux constant + niveau\ncomparable jusqu'en 2050", CORAL)
    fig.text(0.06, 0.45, "→ trajectoire EUR/person dérivée retirée", fontsize=15, color=CORAL, weight="bold")
    box(fig, 0.06, 0.20, 0.41, 0.15, "Leçon", "Valider provenance et sémantique\navant transformation.", GREEN)
    box(fig, 0.53, 0.20, 0.41, 0.15, "Politique NA", "GDPpc comparable : non\nMédian comparable : non\nNA conservé.", BLUE)
    fig.text(0.06, 0.12, "Une opération mathématique peut être correcte et son utilisation méthodologiquement fausse.",
             fontsize=13, color=INK, style="italic")
    return fig


def page_human():
    fig = base(10, "Responsabilité humaine")
    heading(fig, "Human-in-the-loop : accélérer sans déléguer l'architecture")
    box(fig, 0.06, 0.45, 0.41, 0.28, "Les LLM ont accéléré",
        "Recherche\nCode\nExtraction\nSynthèse\nCritique\nDocumentation", GREEN, 10)
    box(fig, 0.53, 0.45, 0.41, 0.28, "J'ai conservé la responsabilité de",
        "Objectif et architecture\nSens des scénarios\nConfiance dans les sources\nCritères d'acceptation\nCe qu'il fallait geler ou simplifier", CORAL, 10)
    fig.text(0.06, 0.27, "Human-directed, machine-accelerated — not model-autonomous.", fontsize=15, color=BLUE, weight="bold")
    fig.text(0.06, 0.17,
             "Les modèles n'ont pas décidé seuls de la structure finale, de la confiance accordée aux sources ou de l'acceptation des résultats.",
             fontsize=11.5, color=INK)
    return fig


def page_practice():
    fig = base(11, "Pratique mature")
    heading(fig, "Ce que le projet a changé dans ma pratique")
    rows = [
        ("Ajouter du détail au modèle", "Réduire la surface de prévision"),
        ("Ajouter du raisonnement", "Renforcer les évaluations"),
        ("Ajouter du contexte", "Curater le contexte"),
        ("Réessayer", "Forcer un changement de stratégie"),
        ("Recherche ouverte", "Exploration bornée"),
        ("Etat conversationnel", "Etat gelé et handoffs"),
        ("Confiance dans un modèle", "Revue adversariale"),
        ("Remplir les trous", "Préférer NA"),
        ("Conserver les abstractions", "Retirer l'Index inutile"),
    ]
    table(fig, [0.06, 0.15, 0.88, 0.66], rows, ["Instinct initial", "Pratique mature"], [0.47, 0.53], 9.5)
    return fig


def page_lessons():
    fig = base(12, "Leçons et compétences")
    heading(fig, "Leçons clés et compétences démontrées")
    lessons = ("Capacité ≠ fiabilité · Prompt seul insuffisant · Etat explicite · Evaluation avant acceptation · "
               "Stop conditions · Contexte sélectionné · Revue multi-modèles testable · Provenance · NA · Jugement humain")
    fig.text(0.06, 0.73, lessons, fontsize=12.5, color=INK, linespacing=1.7, wrap=True)
    box(fig, 0.06, 0.38, 0.26, 0.19, "Context engineering", "Scope · état gelé · handoffs", GREEN)
    box(fig, 0.37, 0.38, 0.26, 0.19, "Agent control", "Anti-loop · exploration bornée", CORAL)
    box(fig, 0.68, 0.38, 0.26, 0.19, "Evaluation", "Temporal · cross-variable · adversarial", BLUE)
    box(fig, 0.06, 0.14, 0.26, 0.16, "Provenance", "Typage · horizon · NA", AMBER)
    box(fig, 0.37, 0.14, 0.26, 0.16, "Data / software", "Python · CSV · validation", GREEN)
    box(fig, 0.68, 0.14, 0.26, 0.16, "Human-in-the-loop", "Arbitrage · architecture · gel", CORAL)
    return fig


def page_conclusion():
    fig = base(13, "Limites et conclusion")
    heading(fig, "Ce que cette étude ne prétend pas")
    box(fig, 0.06, 0.58, 0.41, 0.20, "Limites", "Pas une plateforme d'agents autonomes en production.\n"
        "Tous les contrôles ne sont pas imposés par un framework dédié.\n"
        "La revue multi-modèles n'est pas une peer review scientifique.", CORAL, 9.5)
    box(fig, 0.53, 0.58, 0.41, 0.20, "Reste vrai", "Les workflows dépendent des sources, de la discipline d'exécution et du jugement humain.\n"
        "La prévision de long terme reste incertaine.", BLUE, 9.5)
    fig.text(0.06, 0.38,
             "L'ingénierie LLM ne consiste pas seulement à obtenir de bonnes réponses.",
             fontsize=15, color=INK, weight="bold")
    fig.text(0.06, 0.29,
             "Elle consiste à construire un environnement dans lequel les erreurs deviennent détectables,\n"
             "les décisions traçables, le contexte contrôlable et l'arrêt explicite.",
             fontsize=13, color=INK, linespacing=1.5)
    fig.text(0.06, 0.15,
             "Le projet est devenu plus fiable à mesure que le workflow devenait plus contraint, plus testable et plus human-directed.",
             fontsize=13, color=GREEN, style="italic")
    return fig


def main():
    pages = [page_cover, page_problem, page_failures, page_context, page_antiloop, page_state,
             page_eval, page_multimodel, page_semantics, page_human, page_practice, page_lessons,
             page_conclusion]
    with PdfPages(PDF_PATH) as pdf:
        for index, builder in enumerate(pages, start=1):
            fig = builder()
            pdf.savefig(fig, dpi=180, bbox_inches="tight")
            fig.savefig(QA_DIR / f"page_{index:02d}.png", dpi=120, bbox_inches="tight")
            plt.close(fig)


if __name__ == "__main__":
    main()
