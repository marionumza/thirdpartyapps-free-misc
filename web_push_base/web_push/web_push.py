# -*- coding: UTF-8 -*-
# Copyright 2022 Solvve, Inc. <sales@solvve.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

import json

from dataclasses import dataclass, field, asdict
from hashlib import md5


@dataclass(frozen=True)
class Subscription:
    endpoint: str = field()
    expirationTime: int = field()
    keys: dict = field(default_factory=dict)

    @classmethod
    def from_string(cls, data: str) -> 'Subscription':
        return cls(**json.loads(data))

    @classmethod
    def from_dict(cls, data: dict) -> 'Subscription':
        return cls(**data)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, **kwargs) -> str:
        return json.dumps(self.to_dict(), **kwargs)

    def to_md5_digest(self) -> bytes:
        data = self.to_json(sort_keys=True).encode()
        return md5(data).digest()
