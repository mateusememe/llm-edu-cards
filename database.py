"""
Database Module - SQLite Persistence
Handles storage and retrieval of card generation history
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class CardDatabase:
    """Manages SQLite database for card history"""

    def __init__(self, db_path: str = "cards_history.db"):
        """
        Initialize database connection and create tables if needed

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Create database tables if they don't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS cards (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        topic TEXT NOT NULL,
                        summary TEXT NOT NULL,
                        subtopics TEXT NOT NULL,
                        model TEXT NOT NULL,
                        language TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        temperature REAL,
                        max_tokens INTEGER
                    )
                """
                )

                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_timestamp 
                    ON cards(timestamp DESC)
                """
                )

                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_topic 
                    ON cards(topic)
                """
                )

                conn.commit()
                logger.info("Database initialized successfully")

        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise

    def save_card(
        self,
        topic: str,
        summary: str,
        subtopics: List[str],
        model: str,
        language: str,
        temperature: float = 0.3,
        max_tokens: int = 800,
    ) -> int:
        """
        Save a generated card to database

        Args:
            topic: The main topic
            summary: Generated summary
            subtopics: List of subtopics
            model: Model name used
            language: Language code (pt/en)
            temperature: Temperature parameter used
            max_tokens: Max tokens parameter used

        Returns:
            ID of the inserted card
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                subtopics_json = json.dumps(subtopics, ensure_ascii=False)

                cursor.execute(
                    """
                    INSERT INTO cards 
                    (topic, summary, subtopics, model, language, temperature, max_tokens)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        topic,
                        summary,
                        subtopics_json,
                        model,
                        language,
                        temperature,
                        max_tokens,
                    ),
                )

                conn.commit()
                card_id = cursor.lastrowid

                logger.info(f"Card saved with ID: {card_id}")
                return card_id

        except sqlite3.Error as e:
            logger.error(f"Error saving card: {e}")
            raise

    def get_all_cards(self, limit: int = 100) -> List[Dict]:
        """
        Retrieve all cards from database

        Args:
            limit: Maximum number of cards to retrieve

        Returns:
            List of card dictionaries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT id, topic, summary, subtopics, model, language, 
                           timestamp, temperature, max_tokens
                    FROM cards
                    ORDER BY timestamp DESC
                    LIMIT ?
                """,
                    (limit,),
                )

                rows = cursor.fetchall()

                cards = []
                for row in rows:
                    card = {
                        "id": row[0],
                        "topic": row[1],
                        "summary": row[2],
                        "subtopics": json.loads(row[3]),
                        "model": row[4],
                        "language": row[5],
                        "timestamp": row[6],
                        "temperature": row[7],
                        "max_tokens": row[8],
                    }
                    cards.append(card)

                logger.info(f"Retrieved {len(cards)} cards from database")
                return cards

        except sqlite3.Error as e:
            logger.error(f"Error retrieving cards: {e}")
            return []

    def search_cards(self, query: str, limit: int = 50) -> List[Dict]:
        """
        Search cards by topic

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of matching cards
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                search_pattern = f"%{query}%"

                cursor.execute(
                    """
                    SELECT id, topic, summary, subtopics, model, language, 
                           timestamp, temperature, max_tokens
                    FROM cards
                    WHERE topic LIKE ? OR summary LIKE ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """,
                    (search_pattern, search_pattern, limit),
                )

                rows = cursor.fetchall()

                cards = []
                for row in rows:
                    card = {
                        "id": row[0],
                        "topic": row[1],
                        "summary": row[2],
                        "subtopics": json.loads(row[3]),
                        "model": row[4],
                        "language": row[5],
                        "timestamp": row[6],
                        "temperature": row[7],
                        "max_tokens": row[8],
                    }
                    cards.append(card)

                logger.info(f"Found {len(cards)} cards matching '{query}'")
                return cards

        except sqlite3.Error as e:
            logger.error(f"Error searching cards: {e}")
            return []

    def delete_card(self, card_id: int) -> bool:
        """
        Delete a card by ID

        Args:
            card_id: ID of the card to delete

        Returns:
            True if deleted successfully
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
                conn.commit()

                deleted = cursor.rowcount > 0
                if deleted:
                    logger.info(f"Card {card_id} deleted successfully")
                else:
                    logger.warning(f"Card {card_id} not found")

                return deleted

        except sqlite3.Error as e:
            logger.error(f"Error deleting card: {e}")
            return False

    def clear_all_cards(self) -> bool:
        """
        Delete all cards from database

        Returns:
            True if cleared successfully
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("DELETE FROM cards")
                conn.commit()

                logger.info("All cards cleared from database")
                return True

        except sqlite3.Error as e:
            logger.error(f"Error clearing cards: {e}")
            return False

    def get_statistics(self) -> Dict:
        """
        Get database statistics

        Returns:
            Dictionary with statistics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT COUNT(*) FROM cards")
                total_cards = cursor.fetchone()[0]

                cursor.execute(
                    """
                    SELECT model, COUNT(*) 
                    FROM cards 
                    GROUP BY model
                """
                )
                by_model = dict(cursor.fetchall())


                cursor.execute(
                    """
                    SELECT language, COUNT(*) 
                    FROM cards 
                    GROUP BY language
                """
                )
                by_language = dict(cursor.fetchall())

                cursor.execute(
                    """
                    SELECT COUNT(*) 
                    FROM cards 
                    WHERE timestamp >= datetime('now', '-7 days')
                """
                )
                recent_cards = cursor.fetchone()[0]

                stats = {
                    "total_cards": total_cards,
                    "by_model": by_model,
                    "by_language": by_language,
                    "recent_cards": recent_cards,
                }

                logger.info(f"Statistics retrieved: {stats}")
                return stats

        except sqlite3.Error as e:
            logger.error(f"Error getting statistics: {e}")
            return {
                "total_cards": 0,
                "by_model": {},
                "by_language": {},
                "recent_cards": 0,
            }

    def close(self):
        """Close database connection (for cleanup)"""
        logger.info("Database connection closed")
