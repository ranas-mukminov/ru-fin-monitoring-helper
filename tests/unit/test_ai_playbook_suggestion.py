from ru_fin_ai_helper.playbook_suggester import generate_playbook
from ru_fin_ai_helper.product_profile import ProductProfile


def test_playbook_contains_sections():
    profile = ProductProfile(
        product_type="psp",
        channels=["web"],
        geography="RU",
        features=["cards"],
    )
    playbook = generate_playbook(
        profile=profile,
        events={"auth_login", "transaction_core", "transaction_aml_flags"},
        risk_level="medium",
    )
    assert "Пороговые значения" in playbook
    assert "Эскалация" in playbook
    assert "Логирование" in playbook
