import asyncio
from typing import AsyncGenerator

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from constant import event_strip, system
from service import StateService, get_state_service, SvgGeneratorService, get_svg_generator_service

event_router: APIRouter = APIRouter(prefix=event_strip)

async def _svg_stream(
    state_service: StateService,
    svg_generator_service: SvgGeneratorService,
    poll_interval_s: float = 0.5,
    heartbeat_interval_s: float = 15.0,
) -> AsyncGenerator[str, None]:
    """Yield server-sent events with the latest SVG.

    The generator polls for content changes and emits the SVG when it
    changes. It also emits periodic heartbeats to prevent idle timeouts.
    """
    last_heartbeat: float = 0.0

    # A very small initial delay helps avoid a race where the client attaches
    # handlers after the first event has already been sent.
    await asyncio.sleep(0.05)

    while True:
        # Build current SVG (fast if upstream caches by state).
        if state_service.must_react():
            # data must be followed by two newlines per SSE spec
            svg = svg_generator_service.build_svg(
                indent=False, background_rgb=None
            )
            yield f"data: {svg}\n\n"

            # Reset heartbeat so we don't immediately follow with a ping.
            last_heartbeat = asyncio.get_event_loop().time()

        # Heartbeat comment/event to keep intermediaries from closing the TCP.
        now = asyncio.get_event_loop().time()
        if now - last_heartbeat >= heartbeat_interval_s:
            # You can use an SSE event name, or just a comment line.
            # Here we use a named event the client listens to ("ping").
            yield "event: ping\ndata: keep-alive\n\n"
            last_heartbeat = now

        await asyncio.sleep(poll_interval_s)


@event_router.get(path=f"/svg", tags=[system])
async def stream_svg_events(
    state_service: StateService = Depends(get_state_service),
    svg_generator_service: SvgGeneratorService = Depends(get_svg_generator_service),
) -> StreamingResponse:
    """SSE endpoint that streams SVG updates."""
    # Note: to further reduce needless work, you can add a cheap state
    # fingerprint in StateService and only rebuild SVG when it changes.
    # For example, compare a monotonically increasing 'version' attribute.
    generator = _svg_stream(state_service, svg_generator_service)

    return StreamingResponse(
        generator,
        media_type="text/event-stream",
        headers={
            # Recommended headers for SSE
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # Disable proxy buffering (nginx etc.). Harmless elsewhere.
            "X-Accel-Buffering": "no",
        },
    )