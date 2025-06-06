from typing import List, Tuple, TypedDict

class ASGIScopeInterface(TypedDict):
    type: str
    http_version: str
    server: Tuple[str, int]
    client: Tuple[str, int]
    scheme: str
    method: str
    path: str
    root_path: str
    raw_path: bytes
    query_string: str
    headers: List[Tuple[bytes, bytes]]
