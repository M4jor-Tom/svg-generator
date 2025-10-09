"""SVG routes with Server-Sent Events (SSE).

This module adds an SSE endpoint that continuously streams the latest SVG.
The HTML page connects via EventSource and swaps in the streamed SVG
without page reloads.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from starlette.responses import HTMLResponse

from constant import svg_strip, master, event_strip
from service import (
    SvgGeneratorService,
    get_svg_generator_service,
    StateService,
    get_state_service,
)
from util import DomUtil

svg_router: APIRouter = APIRouter()


@svg_router.get(path=svg_strip, tags=[master], response_class=HTMLResponse)
def get_web_svg(
    state_service: StateService = Depends(get_state_service),
    svg_generator_service: SvgGeneratorService = Depends(get_svg_generator_service),
) -> HTMLResponse:
    """Serve an HTML shell that live-updates SVG using SSE."""
    background_rgb: tuple[float, float, float] = (
        state_service.get_state().background_color
    )

    # Minimal shell with an EventSource client that swaps in streamed SVG.
    # If SSE is unavailable, it falls back to keeping the last rendered SVG.
    html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width,initial-scale=1" />
        <title>Live SVG</title>
        <style>
          html, body {{
            height: 100%;
            margin: 0;
            background: {DomUtil.build_str_color(background_rgb)};
          }}
          #svg-root {{
            display: grid;
            place-items: center;
            height: 100%;
          }}
        </style>
      </head>
      <body>
        <div id="svg-root">
          {svg_generator_service.build_svg(indent=False, background_rgb=None)}
        </div>

        <script>
          (function () {{
            var target = document.getElementById("svg-root");
            var es = new EventSource("{event_strip}/svg");

            es.onmessage = function (ev) {{
              try {{
                // We stream raw SVG markup in the 'data' field.
                location.reload();
                // target.innerHTML = ev.data;
              }} catch (e) {{
                console.error("Failed to apply SVG:", e);
              }}
            }};

            es.addEventListener("ping", function () {{
              // Heartbeat — nothing to do, just keep the pipe warm.
            }});

            es.onerror = function (err) {{
              console.error("SSE error:", err);
              // Let the browser auto-reconnect; no manual close.
            }};
          }})();
        </script>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
