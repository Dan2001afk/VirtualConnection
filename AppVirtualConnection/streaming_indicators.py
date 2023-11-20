from typing import List, Tuple

import numpy as np
import panel as pn

from awesome_panel import config

STYLE = """
.pn-stats-card div {
  line-height: 1em;
}
"""

ACCENT = config.ACCENT
OK_COLOR = config.PALETTE[2]
ERROR_COLOR = config.PALETTE[3]

HEADER = [config.get_header()]
SIDEBAR_FOOTER = config.menu_fast_html(accent=ACCENT)

if not STYLE in pn.config.raw_css:
    pn.config.raw_css.append(STYLE)


def _increment(value):
    draw = np.random.normal(1, 0.1, 1)[0]
    value *= draw
    value = max(0, value)
    value = min(100, value)
    return int(value)


def _create_callback(cards):
    async def update_card():
        for card in cards:
            card.value = _increment(card.value)

    return update_card


def AppIndicadores(intro_section, sidebar_footer) -> pn.template.FastGridTemplate:
    """Returns an app"""
    template = pn.template.FastGridTemplate(
        title="Streaming Indicators",
        row_height=140,
        accent_base_color=ACCENT,
        header_background=ACCENT,
        prevent_collision=True,
        save_layout=True,
        sidebar_footer=sidebar_footer,
        header=HEADER,
    )
    template.main[0:3, :] = intro_section

    indicators = []
    for row in range(0, 3):
        for col in range(0, 6):
            colors: List[Tuple[float, str]] = [(66, OK_COLOR), (100, ERROR_COLOR)]
            title = "Sensor " + str(row * 6 + col + 1)
            indicator = pn.indicators.Number(
                name=title,
                value=65,
                format="{value}%",
                colors=colors,
                css_classes=["pn-stats-card"],
            )
            template.main[row + 3, 2 * col : 2 * col + 2] = indicator
            indicators.append(indicator)

    for row in range(3, 5):
        for col in range(0, 3):
            title = "Sensor " + str(3 * row + col + 10)
            colors = [(0.7, OK_COLOR), (1, ERROR_COLOR)]
            indicator = pn.indicators.Gauge(
                name=title, value=65, bounds=(0, 100), colors=colors, align="center"
            )
            template.main[2 * row : 2 * row + 2, 4 * col : 4 * col + 4] = pn.Row(
                pn.layout.HSpacer(),
                indicator,
                pn.layout.HSpacer(),
            )
            indicators.append(indicator)

    # Create callback for all indicators
    return template


def serve():
    """Serves the app"""
    app = config.extension(url="streaming_indicators", template=None, intro_section=None)
    intro_section = app.intro_section()
    AppIndicadores(intro_section, SIDEBAR_FOOTER).servable()

    # Guardar la aplicación en un archivo HTML
    pn.panel(AppIndicadores(intro_section, SIDEBAR_FOOTER)).save(filename="panel_app.html", embed=True)

if __name__.startswith("bokeh"):
    serve()