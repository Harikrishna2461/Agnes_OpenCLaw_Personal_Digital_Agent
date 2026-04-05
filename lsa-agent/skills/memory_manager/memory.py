"""
Memory Manager: Stores and retrieves user data for simulation context.
"""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class MemoryManager:
    """Manages user memory with embedding-based retrieval."""

    def __init__(self, data_dir: str = "./data"):
        """
        Initialize Memory Manager.
        
        Args:
            data_dir: Directory to store memory files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.memory_file = self.data_dir / "memories.jsonl"
        self.embeddings_file = self.data_dir / "embeddings.npy"
        self.index_file = self.data_dir / "memory_index.json"
        
        # Load or initialize embeddings model
        try:
            self.embedding_model = SentenceTransformer(
                "all-MiniLM-L6-v2", cache_folder=str(self.data_dir)
            )
        except Exception as e:
            logger.warning(f"Could not load embedding model: {e}. Using fallback.")
            self.embedding_model = None
        
        # Load existing memories
        self.memories: List[Dict] = []
        self.embeddings: Optional[np.ndarray] = None
        self._load_memories()
        
        logger.info(f"Memory Manager initialized. Loaded {len(self.memories)} memories.")

    def add_memory(
        self,
        content: str,
        category: str,
        impact_score: float = 5.0,
        tags: Optional[List[str]] = None,
        context: Optional[Dict] = None,
    ) -> str:
        """
        Add a new memory entry.
        
        Args:
            content: Description of the event/action
            category: Type (study, health, productivity, social, finance, mood)
            impact_score: 0-10 score of impact
            tags: Optional tags for organization
            context: Optional context dict (mood, energy, etc.)
        
        Returns:
            Memory ID
        """
        memory_id = str(uuid.uuid4())
        
        memory = {
            "id": memory_id,
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "content": content,
            "impact_score": impact_score,
            "tags": tags or [],
            "context": context or {},
        }
        
        self.memories.append(memory)
        
        # Add embedding if available
        if self.embedding_model:
            embedding = self.embedding_model.encode(content)
            if self.embeddings is None:
                self.embeddings = embedding.reshape(1, -1)
            else:
                self.embeddings = np.vstack(
                    [self.embeddings, embedding.reshape(1, -1)]
                )
        
        self._save_memories()
        logger.info(f"Memory added: {memory_id} ({category})")
        
        return memory_id

    def get_recent_context(self, days: int = 7) -> List[Dict]:
        """
        Get recent activities for simulation context.
        
        Args:
            days: Number of days to look back
        
        Returns:
            List of recent memory entries
        """
        cutoff = datetime.now() - timedelta(days=days)
        recent = [
            m for m in self.memories
            if datetime.fromisoformat(m["timestamp"]) > cutoff
        ]
        return sorted(recent, key=lambda x: x["timestamp"], reverse=True)

    def get_relevant_memories(
        self, query: str, top_k: int = 5
    ) -> List[Dict]:
        """
        Retrieve memories similar to query using embeddings.
        
        Args:
            query: Search query or context
            top_k: Number of results to return
        
        Returns:
            List of top_k most relevant memories
        """
        if not self.embedding_model or self.embeddings is None:
            # Fallback: keyword search
            return self._keyword_search(query, top_k)
        
        try:
            # Encode query
            query_embedding = self.embedding_model.encode(query)
            
            # Compute similarities
            similarities = np.dot(
                self.embeddings, query_embedding
            ) / (
                np.linalg.norm(self.embeddings, axis=1)
                * np.linalg.norm(query_embedding)
            )
            
            # Get top_k indices
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            return [self.memories[i] for i in top_indices]
        except Exception as e:
            logger.error(f"Embedding search failed: {e}")
            return self._keyword_search(query, top_k)

    def analyze_patterns(self, days: int = 30) -> Dict:
        """
        Analyze behavioral patterns over time.
        
        Args:
            days: Number of days to analyze
        
        Returns:
            Dict with pattern analysis
        """
        cutoff = datetime.now() - timedelta(days=days)
        recent = [
            m for m in self.memories
            if datetime.fromisoformat(m["timestamp"]) > cutoff
        ]
        
        # Count by category
        patterns = {}
        for memory in recent:
            cat = memory["category"]
            if cat not in patterns:
                patterns[cat] = {
                    "count": 0,
                    "avg_impact": 0,
                    "trend": "stable",
                }
            patterns[cat]["count"] += 1
            patterns[cat]["avg_impact"] += memory["impact_score"]
        
        # Calculate averages and trends
        for cat in patterns:
            count = patterns[cat]["count"]
            patterns[cat]["avg_impact"] /= count if count > 0 else 1
            patterns[cat]["frequency"] = count / days
            
            # Simple trend: compare first half vs second half
            first_half = recent[-len(recent)//2:]
            second_half = recent[:len(recent)//2]
            
            first_avg = np.mean([m["impact_score"] for m in first_half if m["category"] == cat]) if first_half else 0
            second_avg = np.mean([m["impact_score"] for m in second_half if m["category"] == cat]) if second_half else 0
            
            if second_avg > first_avg * 1.1:
                patterns[cat]["trend"] = "improving"
            elif second_avg < first_avg * 0.9:
                patterns[cat]["trend"] = "declining"
        
        return patterns

    def _keyword_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Fallback keyword search."""
        query_words = set(query.lower().split())
        
        scored = []
        for memory in self.memories:
            content_words = set(memory["content"].lower().split())
            category_words = set(memory["category"].split())
            
            score = len(query_words & content_words) + len(
                query_words & category_words
            )
            if score > 0:
                scored.append((memory, score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return [m[0] for m in scored[:top_k]]

    def _save_memories(self):
        """Save memories to disk."""
        # Save memories as JSONL
        with open(self.memory_file, "w") as f:
            for memory in self.memories:
                f.write(json.dumps(memory) + "\n")
        
        # Save embeddings
        if self.embeddings is not None:
            np.save(self.embeddings_file, self.embeddings)
        
        logger.debug(f"Saved {len(self.memories)} memories to disk")

    def _load_memories(self):
        """Load memories from disk."""
        if not self.memory_file.exists():
            return
        
        with open(self.memory_file, "r") as f:
            for line in f:
                if line.strip():
                    self.memories.append(json.loads(line))
        
        if self.embeddings_file.exists():
            self.embeddings = np.load(self.embeddings_file)
        
        logger.debug(f"Loaded {len(self.memories)} memories from disk")

    def get_all_memories(self) -> List[Dict]:
        """Get all memories."""
        return self.memories

    def clear_memories(self):
        """Clear all memories (for testing)."""
        self.memories = []
        self.embeddings = None
        self._save_memories()
        logger.info("All memories cleared")
