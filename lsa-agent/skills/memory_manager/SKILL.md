# MEMORY MANAGER SKILL

## PURPOSE
Store and retrieve user data over time to build a comprehensive life model.

## CAPABILITIES

### add_memory(entry)
- **Input**: Dict with keys: `timestamp`, `category`, `content`, `impact_score`
- **Categories**: study, health, productivity, social, finance, mood
- **Storage**: Vector DB with FAISS + JSON backup
- **Function**: Stores user actions, habits, decisions for future retrieval

### get_recent_context(days=7)
- **Output**: Last N days of activities, formatted for simulation
- **Use**: Provides context for scenario modeling
- **Returns**: List of {category, content, impact} tuples

### get_relevant_memories(query, top_k=5)
- **Input**: Query string (e.g., "productivity struggles")
- **Process**: Embeddings search in FAISS
- **Output**: Most similar past entries
- **Use**: Ground recommendations in user history

### analyze_patterns(days=30)
- **Output**: Dict with pattern analysis
- **Includes**: frequency, consistency, trend direction
- **Example**: {"study": {"frequency": 5/7, "trend": "declining"}}

## STORAGE SCHEMA

```json
{
  "id": "uuid",
  "timestamp": "2024-04-05T14:30:00Z",
  "category": "study",
  "content": "Completed algorithms session, 60 min focused work",
  "impact_score": 8.5,
  "tags": ["productivity", "learning"],
  "context": {
    "mood_before": 6,
    "mood_after": 8,
    "energy_level": "high"
  }
}
```

## EMBEDDINGS

- Model: sentence-transformers (lightweight)
- Dimension: 384
- Index: FAISS (fast similarity search)
- Fallback: JSON search if vector DB fails

## INTEGRATION POINTS

- **Input**: Telegram messages, manual logging
- **Output**: Context for Simulation Engine
- **Used By**: Intervention Engine (pattern detection)
