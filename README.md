# Incident Management Domain (Tau-Bench)

A comprehensive incident management system for testing AI agent capabilities across multiple interfaces and scenarios.

## Structure

```
├── amazon-tau-bench-tasks/           # Main environment
│   └── envs/incident_managment/
│       ├── Interface_1-5_tasks.py    # Task definitions
│       ├── rules.py                  # 200+ business rules
│       ├── wiki.md                   # Domain policy
│       ├── data/                     # 22 JSON databases
│       └── tools/                    # 5 interfaces (35+ APIs each)
└── amazon-tau-bench-utilities/       # Validation tools
    ├── API_sanity_checks/            # API testing (177 tools)
    └── DB_sanity_checks/             # Database validation
```


## Tools & Interfaces

**5 interfaces** with identical functionality but different verb naming:
- **Interface 1**: create/get/manage/update (35 APIs)
- **Interface 2**: build/fetch/administer/construct (35 APIs)  
- **Interface 3**: add/retrieve/handle/produce (35 APIs)
- **Interface 4**: initiate/query/govern/compose (35 APIs)
- **Interface 5**: launch/lookup/supervise/form (35 APIs)

**API Categories**: Incident management, change management, problem management, work orders, user management, knowledge base, reporting, and performance tracking.

**Standards**: All tools use `invoke(data, **kwargs) -> str` with validation-first approach, audit logging, and data integrity checks.

## Data Schema

**22 JSON entities** with full relational integrity:
- **Core**: users, clients, vendors, products
- **Infrastructure**: components, subscriptions, SLAs
- **Incidents**: incidents, reports, updates, escalations
- **Changes**: change_requests, problem_tickets, rollbacks, root_cause_analyses
- **Work**: work_orders, workarounds, communications, performance_metrics
- **Knowledge**: knowledge_base_articles, post_incident_reviews

**Standards**: String IDs, foreign key integrity, timestamp validation, enum constraints.

## Business Rules & Validation

**200+ business rules** in `rules.py` across 10 categories: incident, change, problem, SLA, communication, knowledge, quality, security, performance, and integration.

**Policy documentation** in `wiki.md` covering complete incident management lifecycle, procedures, and standards.

**Validation utilities**:
- **API Testing**: 177 validation tools across all interfaces
- **Database Testing**: Data integrity, enums, relationships, schema validation
- **Reports**: sanity_report.json, tools_info.json, enums.yaml, relationships.yaml

## Usage

1. Navigate to `amazon-tau-bench-tasks/envs/incident_managment-new/`
2. Choose from 5 interfaces based on testing requirements
3. Use Interface_X_tasks.py files for test scenarios
4. Access data from the `data/` directory
