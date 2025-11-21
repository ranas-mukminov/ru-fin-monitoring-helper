from textwrap import dedent
from typing import Iterable

from .product_profile import ProductProfile


def generate_playbook(profile: ProductProfile, events: Iterable[str], risk_level: str = "medium") -> str:
    events_list = ", ".join(sorted(events))
    header = f"# Плейбук финмон ({profile.product_type})\n"
    body = dedent(
        f"""
        ## Контекст
        - Тип продукта: {profile.product_type}
        - Каналы: {", ".join(profile.channels)}
        - География: {profile.geography}
        - Риск-профиль: {risk_level}

        ## Логирование
        Отслеживаем обязательные события: {events_list}.

        ## Пороговые значения
        - Страновые лимиты: усиливать проверку для high-risk стран.
        - Объемные лимиты: >3 транзакций за минуту по новому клиенту → ручная проверка.
        - Санкции: любые совпадения со score > 70 → стоп и эскалация.

        ## Проверки
        - Подтянуть историю KYC/EDD и последние три аутентификации.
        - Сопоставить устройства/гео, применить risk_bucket.
        - Для крипто: анализировать цепочку входящих/исходящих адресов.

        ## Эскалация
        - Средний риск: передать в финмон аналитикам в течение 2 часов.
        - Высокий риск или санкции: срочная эскалация в L3 / DPO.
        - Оформить case в системе и зафиксировать принятое решение.

        ## Закрытие кейса
        - Добавить итоговый статус (SAR/STR отправлен/не отправлен).
        - Сохранить ссылки на исходные события и артефакты проверки.
        """
    ).strip()
    return header + "\n" + body + "\n"
