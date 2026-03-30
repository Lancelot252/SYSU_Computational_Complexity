import json
from pathlib import Path
from typing import Any, Dict, Union

from core.errors import ValidationError


def load_json_object(path: Union[str, Path]) -> Dict[str, Any]:
    json_path = Path(path)
    try:
        with json_path.open("r", encoding="utf-8-sig") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        raise ValidationError(f"找不到 JSON 文件: {json_path}") from error
    except json.JSONDecodeError as error:
        raise ValidationError(f"JSON 解析失败: {json_path} ({error})") from error

    if not isinstance(data, dict):
        raise ValidationError("JSON 顶层必须是对象。")
    return data