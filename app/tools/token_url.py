from app.config.settings import DefaultSettings


def get_token_url():
    return DefaultSettings().PATH_PREFIX[1:] + "/auth/login"
