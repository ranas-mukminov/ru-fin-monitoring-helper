from ru_fin_ai_helper.event_minimum_set_suggester import suggest_minimum_events
from ru_fin_ai_helper.product_profile import ProductProfile


def test_psp_profile_minimum_events():
    profile = ProductProfile(
        product_type="psp",
        channels=["web", "api"],
        geography="RU",
        features=["cards"],
    )
    events = suggest_minimum_events(profile)
    assert {"auth_login", "transaction_core", "sanctions_screening"}.issubset(events)


def test_crypto_profile_requires_aml_flags():
    profile = ProductProfile(
        product_type="crypto_exchange",
        channels=["web", "mobile"],
        geography="RU",
        features=["p2p", "aml_strict"],
    )
    events = suggest_minimum_events(profile)
    assert "transaction_aml_flags" in events
    assert "kyc_lifecycle" in events
