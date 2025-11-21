from typing import Optional, Set

from .product_profile import ProductProfile

COMMON_EVENTS = {"auth_login", "auth_mfa", "kyc_lifecycle", "sanctions_screening"}

TYPE_SPECIFIC = {
    "psp": {"transaction_core", "transaction_aml_flags", "case_management"},
    "p2p_wallet": {"transaction_core", "transaction_aml_flags"},
    "crypto_exchange": {"transaction_core", "transaction_aml_flags", "case_management"},
    "neobank": {"transaction_core", "transaction_aml_flags", "case_management"},
}


def suggest_minimum_events(profile: ProductProfile, notes: Optional[str] = None) -> Set[str]:
    events: Set[str] = set(COMMON_EVENTS)
    events.update(TYPE_SPECIFIC.get(profile.product_type, set()))

    feature_flags = set(profile.features or [])
    if "aml_strict" in feature_flags or "sanctions" in feature_flags:
        events.add("transaction_aml_flags")
        events.add("sanctions_screening")
    if "p2p" in feature_flags:
        events.add("transaction_core")
    if "cards" in feature_flags:
        events.add("transaction_core")
        events.add("auth_mfa")
    if "case_mgmt" in feature_flags:
        events.add("case_management")

    # notes can hint at additional auditability requirements
    if notes and "ops" in notes.lower():
        events.add("case_management")
    return events
