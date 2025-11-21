# ru-fin-monitoring-helper (русский)

Открытый набор артефактов для технической части финмониторинга/AML в финтехе и крипто. Включает:

- YAML-схемы для событий auth/KYC/txn/AML/санкции;
- примеры пайплайнов ELK и Loki (ingest, normalisation, индексы);
- Grafana-дашборды под финмон сценарии;
- интеграционные обёртки для OpenSanctions и sanctions.network (без ключей и датасетов);
- детерминированные AI-подсказки: минимальный набор событий, draft плейбуков SOC/финмон (оффлайн/noop по умолчанию, без отправки данных наружу).

## Быстрый старт
- Проверка схемы: `ru-fin-helper validate-schema --file schemas/events/transaction_core.yaml`
- Генерация событий: `ru-fin-helper suggest-events --product examples/products/simple_psp_ru.yaml --out /tmp/events.yaml`
- Демостенд ELK: `docker compose -f examples/elk/docker-compose.elk-example.yml up`

## Требования/ограничения
- Лицензия Apache-2.0.
- Не является юридической рекомендацией или заменой финмон-функции.
- Нельзя использовать для обхода санкций/AML-требований; не встраивайте реальные API-ключи/ПДн.

## Контакты и услуги
Развитие проекта: [run-as-daemon.ru](https://run-as-daemon.ru). Консалтинг и внедрение по запросу.
