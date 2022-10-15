DEFAULT_CONFIG = {
    "TeamStatus": False,
    "ZG": False,
    "ZG_COUNT": 2,
    "ZG_WC": None,
    "FB": True,
    "FB_WC": None,
    "NEXT": False,
}

ACCTZU = [
    {
        "status": False,
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
        "config": {
            "TeamStatus": False,
            "ZG": False,
            "ZG_COUNT": 2,
            "ZG_WC": None,
            "FB": False,
            "FB_WC": None,
            "NEXT": False,
        },
        "acctList": [
            {"account": "h1", "server": "h1-2"},
            {"account": "h2", "server": "h2-2"},
            {"account": "h3", "server": "h3-2"},
            {"account": "h4", "server": "h4-2"},
            {"account": "h5", "server": "h5-2"},
        ],
    },
]
