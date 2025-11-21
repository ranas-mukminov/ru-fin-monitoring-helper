import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AI_SRC = ROOT / "ai" / "src"
SANCTIONS_OS_SRC = ROOT / "sanctions" / "opensanctions_client" / "src"
SANCTIONS_NET_SRC = ROOT / "sanctions" / "sanctions_network_client" / "src"

for path in (ROOT, AI_SRC, SANCTIONS_OS_SRC, SANCTIONS_NET_SRC):
    sys.path.insert(0, str(path))
