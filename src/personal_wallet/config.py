import configparser


def configure(ctx, param, file):
    """Reads from .ini config gile and sets other parameters’ default values."""
    cfg = configparser.ConfigParser()
    cfg.read(file)
    try:
        options = dict(cfg["options"])
    except KeyError:
        options = {}
    ctx.default_map = options
