from .framedrawer import (
    drawHomeFrame,
    drawMoveFrame,
    drawTraceFrame,
    drawViewFrame,
    drawInputFrame,
    drawDataFrame,
    drawTrainFrame,
)

DRAW_FRAME = {
    "": lambda e: None,
    "Home": drawHomeFrame,
    "Perform": drawMoveFrame,
    "Record": drawTraceFrame,
    "Train": drawViewFrame,
}

TABS = ("Perform", "Record", "Train")
