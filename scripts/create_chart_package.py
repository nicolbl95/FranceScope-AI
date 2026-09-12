"""Generate the public FranceScope V8 chart package from canonical CSV files."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter, MultipleLocator


ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "data" / "final"
INSTITUTIONAL = ROOT / "data" / "institutional"
OUT = ROOT / "outputs" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

COLORS = {
    "OPTIMISTIC": "#2A9D8F",
    "CENTRAL": "#E9C46A",
    "PESSIMISTIC": "#E76F51",
}
LABELS = {
    "OPTIMISTIC": "Dégradation faible",
    "CENTRAL": "Dégradation centrale",
    "PESSIMISTIC": "Dégradation forte",
}
SCENARIO_ORDER = ["OPTIMISTIC", "CENTRAL", "PESSIMISTIC"]
YEARS = [2025, 2030, 2040, 2050]

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#D9E1E8",
        "grid.linewidth": 0.7,
        "grid.alpha": 0.8,
        "axes.titleweight": "bold",
        "figure.facecolor": "white",
        "axes.facecolor": "#FCFDFE",
    }
)


def euro(value: float) -> str:
    return f"{value:,.0f}".replace(",", " ").replace(".", ",") + " €"


def integer(value: float) -> str:
    return f"{value:,.0f}".replace(",", " ")


def percent(value: float) -> str:
    return f"{value:.1f}".replace(".", ",") + " %"


def load_forecasts(variable: str) -> pd.DataFrame:
    data = pd.read_csv(FINAL / "final_three_target_forecasts.csv")
    return data[data["variable"].eq(variable)].copy()


def baseline(data: pd.DataFrame) -> float:
    return float(data.loc[data["scenario"].eq("2025_ACTUAL"), "point_forecast"].iloc[0])


def save(fig: plt.Figure, filename: str) -> None:
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=180, bbox_inches="tight")
    plt.close(fig)


def scenario_chart(
    variable: str,
    filename: str,
    title: str,
    ylabel: str,
    formatter: FuncFormatter,
    annotation_formatter,
    note: str,
    y_locator: MultipleLocator | None = None,
) -> None:
    data = load_forecasts(variable)
    actual = baseline(data)
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    ax.axvline(2025, color="#59636E", linewidth=1.2, linestyle="--", alpha=0.75)
    ax.scatter([2025], [actual], color="#263238", marker="o", s=58, zorder=5, label="Observation 2025")

    for scenario in SCENARIO_ORDER:
        rows = data[data["scenario"].eq(scenario)].sort_values("year")
        x = [2025] + rows["year"].astype(int).tolist()
        y = [actual] + rows["point_forecast"].astype(float).tolist()
        ax.plot(
            x,
            y,
            color=COLORS[scenario],
            linewidth=2.8,
            marker="o",
            markersize=5.5,
            label=LABELS[scenario],
        )
        endpoint = float(rows.loc[rows["year"].eq(2050), "point_forecast"].iloc[0])
        ax.annotate(
            annotation_formatter(endpoint),
            (2050, endpoint),
            xytext=(7, 0),
            textcoords="offset points",
            color=COLORS[scenario],
            fontsize=9,
            va="center",
            fontweight="bold",
        )

    ax.set_title(title, loc="left", fontsize=16, pad=18)
    ax.text(
        0,
        1.02,
        "2025 = baseline observé · 2030, 2040, 2050 = scénarios conditionnels FranceScope",
        transform=ax.transAxes,
        fontsize=9.5,
        color="#59636E",
    )
    ax.set_xlabel("Année")
    ax.set_ylabel(ylabel)
    ax.set_xticks(YEARS)
    ax.set_xlim(2024, 2054)
    ax.yaxis.set_major_formatter(formatter)
    if y_locator:
        ax.yaxis.set_major_locator(y_locator)
    ax.legend(loc="upper left", frameon=False, ncol=2)
    ax.text(0, -0.18, note, transform=ax.transAxes, fontsize=9, color="#59636E")
    save(fig, filename)


def institutional_unemployment() -> None:
    data = load_forecasts("unemployment_rate")
    long_run = pd.read_csv(INSTITUTIONAL / "institutional_long_run_reference.csv")
    consensus = pd.read_csv(INSTITUTIONAL / "institutional_near_term_consensus.csv")
    fig, ax = plt.subplots(figsize=(11.2, 6.6))

    actual = baseline(data)
    ax.scatter([2025], [actual], color="#263238", s=58, zorder=6, label="Observation 2025")

    for scenario in SCENARIO_ORDER:
        rows = data[data["scenario"].eq(scenario)].sort_values("year")
        ax.plot(
            [2025] + rows["year"].tolist(),
            [actual] + rows["point_forecast"].tolist(),
            color=COLORS[scenario],
            linewidth=2.4,
            marker="o",
            markersize=4.5,
            label=f"FranceScope — {LABELS[scenario].lower()}",
        )

    near = consensus[consensus["target_variable"].eq("unemployment_rate")]
    ax.plot(
        near["year"],
        near["median"],
        color="#264653",
        marker="D",
        linewidth=2,
        markersize=5,
        label="Consensus institutionnel court terme",
    )
    direct = long_run[
        long_run["target_variable"].eq("unemployment_rate")
        & long_run["classification"].eq("DIRECT_FORECAST")
    ]
    ax.plot(
        direct["year"].astype(int),
        direct["value"].astype(float),
        color="#457B9D",
        marker="s",
        linestyle=":",
        linewidth=2,
        markersize=5,
        label="Banque de France — prévision directe",
    )
    ec = long_run[
        long_run["target_variable"].eq("unemployment_rate")
        & long_run["classification"].eq("LONG_RUN_PROJECTION")
    ]
    ax.plot(
        ec["year"].astype(int),
        ec["value"].astype(float),
        color="#6C757D",
        marker="^",
        linestyle="--",
        linewidth=2,
        markersize=5,
        label="Référence CE long terme",
    )
    ax.axvline(2028.5, color="#ADB5BD", linestyle="--", linewidth=1)
    ax.text(2028.7, 7.35, "Changement de nature\ninstitutionnelle", fontsize=8.5, color="#59636E")
    ax.set_title("Chômage — FranceScope et références institutionnelles", loc="left", fontsize=16, pad=18)
    ax.text(
        0,
        1.02,
        "Les références court terme et la projection CE long terme ne forment pas une série homogène",
        transform=ax.transAxes,
        fontsize=9.5,
        color="#59636E",
    )
    ax.set_xlabel("Année")
    ax.set_ylabel("Taux de chômage (%)")
    ax.set_xticks([2025, 2026, 2027, 2028, 2030, 2040, 2050])
    ax.tick_params(axis="x", labelrotation=30)
    ax.set_xlim(2024, 2054)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0f} %"))
    ax.yaxis.set_major_locator(MultipleLocator(2))
    ax.legend(loc="upper left", frameon=False, fontsize=8.5, ncol=2)
    ax.text(
        0,
        -0.18,
        "Banque de France : prévisions directes. CE : projection structurelle âge 20–64, non directement comparable.",
        transform=ax.transAxes,
        fontsize=9,
        color="#59636E",
    )
    save(fig, "institutional_unemployment.png")


def institutional_gdp() -> None:
    scenario_chart(
        "real_gdp_per_capita",
        "institutional_real_gdp_per_capita.png",
        "PIB réel par habitant — scénarios FranceScope",
        "€ constants par personne",
        FuncFormatter(lambda value, _: integer(value) + " €"),
        euro,
        "Aucun niveau institutionnel de long terme directement comparable. Les jalons CE de croissance restent séparés.",
        MultipleLocator(2_000),
    )


def institutional_median() -> None:
    scenario_chart(
        "real_median_living_standard",
        "institutional_real_median_living_standard.png",
        "Niveau de vie médian réel — scénarios FranceScope",
        "€ constants par personne et par an",
        FuncFormatter(lambda value, _: integer(value) + " €"),
        euro,
        "Pas de prévision institutionnelle de long terme directement comparable identifiée.",
        MultipleLocator(1_000),
    )


def dashboard() -> None:
    data = pd.read_csv(FINAL / "final_three_target_forecasts.csv")
    actuals = {
        "Chômage": ("unemployment_rate", "%", 7.725),
        "PIB réel par habitant": ("real_gdp_per_capita", "€", 38360),
        "Niveau de vie médian réel": ("real_median_living_standard", "€", 25952.514017),
    }
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 5.2))
    for ax, (title, (variable, unit, actual)) in zip(axes, actuals.items()):
        rows = data[(data["variable"].eq(variable)) & (data["year"].eq(2050))]
        values = [
            float(rows.loc[rows["scenario"].eq(s), "point_forecast"].iloc[0])
            for s in SCENARIO_ORDER
        ]
        bars = ax.bar(
            ["Faible", "Centrale", "Forte"],
            values,
            color=[COLORS[s] for s in SCENARIO_ORDER],
            width=0.65,
        )
        ax.axhline(actual, color="#263238", linestyle="--", linewidth=1.5, label="2025")
        for bar, value in zip(bars, values):
            label = percent(value) if unit == "%" else euro(value)
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), label, ha="center", va="bottom", fontsize=8.5)
        ax.set_title(title, fontsize=11.5, pad=12)
        ax.set_ylabel("Taux" if unit == "%" else "Euros constants")
        ax.yaxis.set_major_formatter(
            FuncFormatter(
                lambda value, _, display_unit=unit: (
                    f"{value:.0f} %" if display_unit == "%" else integer(value)
                )
            )
        )
        ax.grid(axis="x", visible=False)
    fig.suptitle("FranceScope — résultats des scénarios en 2050", x=0.03, ha="left", fontsize=17, fontweight="bold")
    fig.text(0.03, 0.91, "Comparaison rapide des trois cibles · aucune note composite", fontsize=10, color="#59636E")
    fig.text(0.03, 0.02, "La ligne pointillée indique le niveau observé en 2025 ; les barres montrent les scénarios conditionnels FranceScope.",
             fontsize=9, color="#59636E")
    save(fig, "final_scenario_comparison.png")


def main() -> None:
    scenario_chart(
        "unemployment_rate",
        "unemployment.png",
        "Chômage — scénarios FranceScope jusqu’en 2050",
        "Taux de chômage (%)",
        FuncFormatter(lambda value, _: f"{value:.0f} %"),
        percent,
        "Le chômage augmente lorsque les chocs persistants et le scarring s’accumulent.",
        MultipleLocator(2),
    )
    scenario_chart(
        "real_gdp_per_capita",
        "real_gdp_per_capita.png",
        "PIB réel par habitant — scénarios FranceScope jusqu’en 2050",
        "€ constants par personne",
        FuncFormatter(lambda value, _: integer(value) + " €"),
        euro,
        "Mesure de production moyenne ; elle ne décrit pas à elle seule la distribution des revenus.",
        MultipleLocator(2_000),
    )
    scenario_chart(
        "real_median_living_standard",
        "real_median_living.png",
        "Niveau de vie médian réel — scénarios FranceScope jusqu’en 2050",
        "€ constants par personne et par an",
        FuncFormatter(lambda value, _: integer(value) + " €"),
        euro,
        "Mesure distribuée distincte du PIB réel par habitant, après impôts, transferts et redistribution.",
        MultipleLocator(1_000),
    )
    institutional_unemployment()
    institutional_gdp()
    institutional_median()
    dashboard()


if __name__ == "__main__":
    main()
