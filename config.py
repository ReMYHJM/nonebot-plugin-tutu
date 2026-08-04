from pydantic import BaseModel


class Config(BaseModel):
    """插件配置类"""
    tutu_max_count: int = 15
    tutu_default_count: int = 1
    tutu_orientation: str = "random"  # random / pc / pe
    tutu_api_timeout: int = 10
    tutu_headers_json: str = (
        '{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", '
        '"Accept": "application/json"}'
    )
