import os
import json
import base64
from pydantic import BaseModel, Field
from typing import Optional


class XrayBaseSetting(BaseModel):
    http: Optional[bool] = None
    socks: Optional[bool] = None
    http_port: Optional[int] = None
    socks_port: Optional[int] = None


class ConfigData(BaseModel):
    last_xray_pid: Optional[int] = 0
    test_limit: Optional[int] = 10
    speed_tolerance: Optional[float] = 0.9
    location: Optional[str] = "auto"
    create_file: Optional[bool] = False
    xray_config: XrayBaseSetting = Field(default_factory=lambda: XrayBaseSetting(
        http=True, socks=True, http_port=1081, socks_port=1080))


class ConfigManager:
    def __init__(self, filename: str, encode: bool = True):
        self.filename = filename
        self.encode = encode

    def _load_file(self) -> dict:
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = f.read()

            if self.encode:
                data = base64.b64decode(data).decode()

            data = data.replace("'", '"')
            return json.loads(data)
        return {}

    def read(self) -> ConfigData:
        config_data = self._load_file()
        return ConfigData(**config_data) if config_data else ConfigData()

    def write(self, data: ConfigData):
        current_data = self._load_file()
        updated_data = {**current_data, **data.dict(exclude_unset=True)}
        updated_data['xray_config'] = {
            **current_data.get('xray_config', {}), **data.xray_config.dict(exclude_unset=True)}

        serialized_data = json.dumps(updated_data, indent=4)

        if self.encode:
            serialized_data = base64.b64encode(
                serialized_data.encode()).decode()

        with open(self.filename, 'w') as f:
            f.write(serialized_data)
