import configparser
import os
from pydantic import BaseSettings

config = configparser.RawConfigParser()
config.read(f"{os.path.join(os.path.dirname(__file__))}/config.ini")
ENV = os.environ.get("ENV", "testnet")


class Config(BaseSettings):
    binance_api_key: str = os.getenv(
        "BINANCE_API_KEY", config.get(ENV, "binance_api_key", fallback="")
    )
    binance_secret_key: str = os.getenv(
        "BINANCE_SECRET_KEY", config.get(ENV, "binance_secret_key", fallback="")
    )
    future_stream_uri: str = os.getenv(
        "FUTURE_STREAM_URI", config.get(ENV, "future_stream_uri", fallback="")
    )
    base_url: str = os.getenv(
        "BASE_URL", config.get(ENV, "base_url", fallback="")
    )
