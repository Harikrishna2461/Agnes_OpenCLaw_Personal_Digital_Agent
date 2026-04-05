# Project Structure

```
lsa-agent/
├── config/
│   ├── SOUL.md                 # Agent personality & behavior rules
│   └── __init__.py
├── skills/
│   ├── __init__.py
│   ├── memory_manager/
│   │   ├── __init__.py
│   │   ├── SKILL.md           # Memory Manager skill documentation
│   │   └── memory.py          # Memory storage & retrieval engine
│   ├── simulation_engine/
│   │   ├── __init__.py
│   │   ├── SKILL.md           # Simulation skill documentation
│   │   └── simulation.py      # Multi-scenario generator
│   └── intervention_engine/
│       ├── __init__.py
│       ├── SKILL.md           # Intervention skill documentation
│       └── intervention.py    # Alert & Telegram integration
├── data/                       # Memory storage (created at runtime)
│   ├── memories.jsonl          # User events and logs
│   ├── embeddings.npy          # Embedding vectors
│   ├── memory_index.json       # Index metadata
│   └── lsa_export_*.json       # Periodic backups
├── main.py                     # Main orchestration + demo
├── scheduler.py                # Cron job scheduler for autonomous operation
├── telegram_daemon.py          # Telegram bot integration daemon
├── test_lsa.py                 # Component test suite
├── config_helper.py            # Configuration utilities
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
├── GETTING_STARTED.md          # Quick start guide
└── README.md                   # Full documentation
```

## File Descriptions

### Core Files
- **main.py**: Main `LifeSimulationAgent` class orchestrating all subsystems
- **scheduler.py**: APScheduler setup for autonomous daily/weekly operations
- **telegram_daemon.py**: Telegram bot integration for real-time alerts

### Skills Packages
Each skill is a self-contained Python module:

- **memory_manager/**: User data storage, retrieval, pattern analysis
- **simulation_engine/**: Multi-scenario generation for decision analysis
- **intervention_engine/**: Alert generation and Telegram integration

### Configuration
- **config/SOUL.md**: Agent personality and behavioral rules
- **config_helper.py**: Configuration loading and validation

### Documentation
- **README.md**: Full documentation with examples
- **GETTING_STARTED.md**: Quick start guide
- ***/SKILL.md**: Each skill has detailed documentation

### Testing & Release
- **test_lsa.py**: Component unit tests
- **requirements.txt**: Python package dependencies
- **.env.example**: Environment variable template
