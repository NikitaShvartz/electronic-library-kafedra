# Электронная библиотека кафедры

Учебный командный проект по дисциплине «Методы оптимизации в разработке программных решений».

## О продукте
Сервис для просмотра и поиска книг кафедры, базового учёта выдачи/возврата и контроля доступности экземпляров. Предполагаемый стек: Python + FastAPI + SQLite, интерфейс на первом этапе — Swagger/OpenAPI.

## Документы ЛР1
- [Видение продукта](docs/01-planning/vision.md)
- [Карта историй](docs/01-planning/story-map.md)
- [Бэклог и критерии приёмки](docs/01-planning/backlog.md)
- [Оценки Planning Poker и PERT](docs/01-planning/estimates.md)
- [WSJF и задача о рюкзаке](docs/01-planning/prioritization.md)
- [План релиза, CPM и Монте-Карло](docs/01-planning/release-plan.md)
- [Процесс команды, WIP, DoR/DoD](docs/01-planning/process.md)
- [Рабочее соглашение](docs/01-planning/team-agreement.md)
- [Подготовка к защите: контрольные вопросы](docs/01-planning/defense-notes.md)

## Структура
- `docs/01-planning/` — ЛР1;
- `docs/02-pipeline/` — материалы ЛР2;
- `docs/03-quality/` — материалы ЛР3;
- `docs/04-metrics/` — материалы ЛР4;
- `data/` — исходные CSV и параметры модели;
- `scripts/` — воспроизводимые расчёты и помощник для создания GitHub issues;
- `src/`, `tests/`, `load/` — будущий код, тесты и нагрузочные сценарии.

## Повторить расчёты
Требуется Python 3.9+; сторонние библиотеки не нужны.

```bash
python scripts/release_planner.py
python scripts/pert_cpm.py
python scripts/monte_carlo.py
```

Скрипты читают `data/` и записывают воспроизводимые результаты в CSV; `pert_cpm.py` обновляет рисунок `docs/01-planning/network.svg`.

## Трекер задач

Задачи ведутся в GitHub Issues, доска проекта — GitHub Projects.

Статусы доски: `Backlog → Ready → In Progress → Review → Done`.

**Ссылка на доску:** [GitHub Projects](https://github.com/users/NikitaShvartz/projects/1/views/1)

Для настройки меток и создания задач из `data/issues.csv` используются команды:

```bash
bash scripts/setup_github_labels.sh
python scripts/create_github_issues.py
```

Скрипт создания Issues пропускает задачи с уже существующими заголовками. Перед запуском необходимо проверить CSV и согласованные оценки команды.

## Перед сдачей
1. Проверить актуальность имён участников, ссылки на репозиторий и доску.
2. Подтвердить дату защиты ЛР3; в модели временно принято 28.12.2026.
3. Провести реальный Planning Poker и обновить `data/estimation_rounds.csv`, `data/stories.csv` и документы.
4. Проверить наличие всех Issues, настройки доски и соблюдение WIP-лимитов.
5. Повторить скрипты и убедиться, что результаты совпадают с документами.
6. Проверить критерии приёмки и ограничения MVP с напарником.
7. После проверки создать тег `lab1`:

```bash
git add .
git commit -m "docs: complete lab 1 planning"
git tag lab1
git push origin main --tags
```

## Статус
Документы содержат подготовленную учебную модель. Синтетические данные пропускной способности и предложенные оценки должны быть заменены реальными данными команды по мере их появления.
