import os
import json
import base64
from pydantic import BaseModel
from typing import Optional


class XrayBaseSetting(BaseModel):
    http: Optional[bool] = None
    socks: Optional[bool] = None
    http_port: Optional[int] = None
    socks_port: Optional[int] = None


class ConfigData(BaseModel):
    last_xray_pid: Optional[int] = None
    test_limit: Optional[int] = None
    speed_tolerance: Optional[float] = None
    create_file: Optional[bool] = None
    xray_config: XrayBaseSetting = None


class ConfigManager:
    def __init__(self, filename: str, encode: bool = True):
        self.filename = filename
        self.encode = encode

    def read(self) -> ConfigData:
        if not os.path.exists(self.filename):
            return ConfigData(
                last_xray_pid=0,
                test_limit=10,
                speed_tolerance=0.9,
                create_file=False,
                xray_config=XrayBaseSetting(
                    http=True, socks=True, http_port=1081, socks_port=1080)
            )

        with open(self.filename, 'r') as f:
            data = f.read()

        if self.encode:
            data = base64.b64decode(data).decode()

        data = data.replace("'", '"')
        config = json.loads(data)

        return ConfigData(**config)

    def write(self, data: ConfigData):
        current_data = self.read()

        if data.xray_config:
            for key, value in data.xray_config.dict().items():
                if value is not None:
                    setattr(current_data.xray_config, key, value)

        for key, value in data.dict().items():
            if key != 'xray_config' and value is not None:
                setattr(current_data, key, value)

        d = current_data.dict()
        d = {key: value for key, value in d.items() if value is not None}
        d = json.dumps(d, indent=4)

        if self.encode:
            d = base64.b64encode(d.encode()).decode()

        with open(self.filename, 'w') as f:
            f.write(d)
