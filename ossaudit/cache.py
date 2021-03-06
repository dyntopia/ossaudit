# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

import json
import time
from typing import Dict, Optional

from . import const


def get(coordinate: str) -> Optional[Dict]:
    if const.CACHE.exists():
        with const.CACHE.open() as f:
            try:
                entry = next(
                    (
                        e for e in json.load(f)
                        if e["coordinates"] == coordinate
                    ),
                    {},
                )
                if _is_valid(entry):
                    return entry
            except json.JSONDecodeError:
                pass
    return None


def save(entry: Dict) -> None:
    entries = []  # type: list

    if const.CACHE.exists():
        with const.CACHE.open() as f:
            try:
                entries = [
                    e for e in json.load(f) if _is_valid(e)
                    and e.get("coordinates") != entry.get("coordinates")
                ]
            except json.JSONDecodeError:
                pass
    else:
        const.CACHE.parent.mkdir(parents=True, exist_ok=True)

    with const.CACHE.open("w") as f:
        entry["time"] = time.time()
        json.dump(entries + [entry], f)


def reset() -> None:
    if const.CACHE.exists():
        const.CACHE.unlink()


def _is_valid(entry: Dict) -> bool:
    then = entry.get("time", float("inf"))
    now = time.time()
    return not then > now + const.CACHE_TIME
