# ru-fin-monitoring-helper

## English

Starter kit of schemas, pipelines, dashboards, and AI-assisted helpers for Russian FIU/AML-style monitoring. Provides YAML schemas for logging auth/KYC/transaction/sanctions events, example ELK/Loki pipelines, Grafana dashboards, sanctions-integration stubs, and deterministic AI helpers for drafting event sets and playbooks.

---

## Русский

### Что это

Набор схем логов, пайплайнов, дашбордов и AI-подсказок для финмониторинга в финтех-/крипто-/платёжных сервисах. Фокусируется на технической стороне (DevSecOps/observability) и не является юридической рекомендацией.

### Для кого

- команды ИБ/DevSecOps/платёжных платформ в РФ;
- криптопроекты и малые финтех-компании.

### Что даёт

- готовые схемы: какие события и поля логировать для AML/финмон;
- примеры ELK/Loki-пайплайнов и index templates;
- Grafana-дашборды под финмон сценарии;
- примеры интеграции с открытыми санкционными списками (без ключей/данных);
- генератор минимального набора событий и черновиков плейбуков (off-by-default, без отправки данных наружу).

### Быстрый старт

```bash
pip install -e .[dev]
ru-fin-helper validate-schema --file schemas/events/transaction_core.yaml
ru-fin-helper suggest-events --product examples/products/simple_psp_ru.yaml --out /tmp/events.yaml
docker compose -f examples/elk/docker-compose.elk-example.yml up
```

### Профессиональные услуги – run-as-daemon.ru

Проект развивается инженером DevOps/DevSecOps с сайта [run-as-daemon.ru](https://run-as-daemon.ru).

Если вам нужно:
- выстроить журналирование и мониторинг для финмониторинга;
- настроить дашборды и алерты «под финмон»;
- подготовиться к интеграции с внешними AML/санкционными сервисами,

вы можете заказать консалтинг, внедрение и поддержку.

### Дисклеймер

- проект не является юридической рекомендацией;
- не заменяет официальные требования регуляторов;
- ответственность за соответствие закону и регуляторке лежит на пользователе;
- не содержит API-ключей, реальные списки и персональные данные не включаются.
