def make_x264_defaults():

    return {
        'fps':           '24000/1001',
        'profile':       'high10',
        'bframes':       '8',
        'b-adapt':       '2',
        'b-pyramid':     'normal',
        'ref':           '9',
        'crf':           '16',
        'rc-lookahead':  '60',
        'aq-mode':       '2',
        'qcomp':         '0.70',
        'aq-strength':   '0.8',
        'partitions':    'all',
        'direct':        'auto',
        'me':            'umh',
        'merange':       '24',
        'subme':         '10',
        'trellis':       '2',
        'no-fast-pskip': '',
        'psy-rd':        '0.6:0.1'
    }


def make_avs4x26x_defaults():

    defaults = make_x264_defaults()
    # This needs to be wrapped in parentheses because it is a generic argument
    defaults['x26x-binary'] = '"Programs\\x264.exe"'
    defaults['input-depth'] = '16'
    return defaults
