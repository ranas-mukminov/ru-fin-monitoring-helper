# SOC/FinMon Playbook Template

## Триггер
- Правило/алерт: <rule_id>
- Источник: SIEM / AML engine

## Действия аналитика
1. Проверить последние события auth_* и transaction_* пользователя.
2. Сверить санкционные проверки (sanctions_screening).
3. При необходимости запросить у клиента дополнительные документы (kyc_lifecycle).

## Эскалация
- Если score > 80 или санкции = hit → эскалация в L3/DPO.

## Закрытие
- Итог: allow/block/report, обновить case_management.
