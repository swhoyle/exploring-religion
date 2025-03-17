RELIGIOUS_COLORS = {
    "Christianity": "#1f77b4",
    "Judaism": "#ff7f0e",
    "Islam": "#2ca02c",
    "Buddhism": "#d62728",
    "Hinduism": "#9467bd",
    "Sikhism": "#8c564b",
    "Shinto": "#e377c2",
    "Baha’i": "#7f7f7f",
    "Taoism": "#bcbd22",
    "Jainism": "#17becf",
    "Confucianism": "#ff9896",
    "Zoroastrianism": "#c5b0d5",
    "Syncretism": "#c49c94",
    "Animism": "#f7b6d2",
    "No Religion": "#d9d9d9",
    "Other Religion": "#aec7e8"
}

RELIGIOUS_COLORS_LIGHT = {
    "Christianity": "#a3cbe1",
    "Judaism": "#ffbf80",
    "Islam": "#80c89d",
    "Buddhism": "#f2a5a5",
    "Hinduism": "#b59ed6",
    "Sikhism": "#b68a72",
    "Shinto": "#f3a2d7",
    "Baha’i": "#bfbfbf",
    "Taoism": "#e0e38f",
    "Jainism": "#a0d9db",
    "Confucianism": "#ffd8d0",
    "Zoroastrianism": "#d3b2e0",
    "Syncretism": "#e4d0c1",
    "Animism": "#f9d3e2",
    "No Religion": "#f0f0f0",
    "Other Religion": "#c1d9e9"
}

def format_followers(n):
    if n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.2f} Billion"
    elif n >= 1_000_000:
        return f"{n / 1_000_000:.2f} Million"
    elif n >= 100_000:
        return f"{n / 1_000:.0f}K"
    else:
        return f"{n:,}"

def format_percent(n):
    if n is None:
        return None
    n = n * 100
    if n >= 99:
        return f"{n:.2f}%"
    elif n < 1:
        return f"{n:.2f}%"
    else:
        return f"{n:.0f}%"
    
def format_percent_change(n):
    
    if n is None:
        return None
    n = n * 100
    if n < 0:
        if n > -1:
            return f"{n:.1f}%"
        return f"{n:.0f}%"
    if n > 0:
        if n < 1:
            return f"+{n:.1f}%"
        return f"+{n:.0f}%"
    else:
        return "0%"