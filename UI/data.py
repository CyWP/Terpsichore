from .framedrawer import (drawHomeFrame,
                         drawMoveFrame,
                         drawTraceFrame,
                         drawViewFrame,
                         drawInputFrame,
                         drawDataFrame,
                         drawTrainFrame)

DRAW_FRAME = {
            '': lambda e: None,
            'Home': drawHomeFrame,
            'Move': drawMoveFrame,
            'Trace': drawTraceFrame,
            'View': drawViewFrame,
            'Input': drawInputFrame,
            'Data': drawDataFrame,
            'Train': drawTrainFrame
            }

TABS = ('Move',
        'Trace',
        'View',
        'Input',
        'Data',
        'Train')

