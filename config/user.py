DEFAULT_CONFIG = {
    "TeamStatus": False,
    "ZG": True,
    "ZG_COUNT": 2,
    "ZG_WC": None,
    "FB": True,
    "FB_WC": None,
    "NEXT": True,
}

ACCTZU = [
    {
        "status": True,
        # "status": False,
        "config": DEFAULT_CONFIG,
        "acctList": [
            {"account": "h1", "server": "h1-1"},
            {"account": "h2", "server": "h2-1"},
            {"account": "h3", "server": "h3-1"},
            {"account": "h4", "server": "h4-1"},
            {"account": "h5", "server": "h5-1"},
        ],
    },
    {
        "status": True,
        # "status": False,
        "config": DEFAULT_CONFIG,
        "acctList": [
            {"account": "h1", "server": "h1-2"},
            {"account": "h2", "server": "h2-2"},
            {"account": "h3", "server": "h3-2"},
            {"account": "h4", "server": "h4-2"},
            {"account": "h5", "server": "h5-2"},
        ],
    },
]
