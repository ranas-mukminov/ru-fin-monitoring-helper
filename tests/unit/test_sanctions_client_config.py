import pytest

from sanctions.opensanctions_client.config import OpenSanctionsConfig


def test_default_config_validates():
    cfg = OpenSanctionsConfig()
    cfg.validate()
    assert cfg.base_url.startswith(("https://", "http://")), "base_url should be URL-like"
    assert cfg.timeout > 0


def test_negative_timeout_rejected():
    cfg = OpenSanctionsConfig(timeout=-1)
    with pytest.raises(ValueError):
        cfg.validate()


def test_localhost_url_allowed():
    cfg = OpenSanctionsConfig(base_url="http://localhost:8080", timeout=5)
    cfg.validate()
