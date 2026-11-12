"""
CyberShield Database Management Module
Handles SQLite schema creation, user progress tracking, quiz scores, scan logs, and badges.
"""

import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "cybershield.db")


def get_connection() -> sqlite3.Connection:
    """Returns a connection to the SQLite database with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initializes the SQLite database tables if they do not exist."""
    os.makedirs(DB_DIR, exist_ok=True)
    with get_connection() as conn:
        cursor = conn.cursor()

        # Users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                role TEXT DEFAULT 'general',
                preferred_language TEXT DEFAULT 'en',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Completed lessons table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS completed_lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                lesson_id TEXT NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, category, lesson_id),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
            """
        )

        # Quiz attempts table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                difficulty TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                percentage REAL NOT NULL,
                passed INTEGER NOT NULL,
                attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
            """
        )

        # Scam check log
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS scam_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                sample_title TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                detected_triggers TEXT,
                scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
            """
        )

        # Badges table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS badges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                badge_key TEXT NOT NULL,
                badge_title TEXT NOT NULL,
                description TEXT,
                earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, badge_key),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
            """
        )

        conn.commit()

        # Ensure default demo user exists
        cursor.execute("SELECT id FROM users WHERE username = 'Default User'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (username, role, preferred_language) VALUES (?, ?, ?)",
                ("Default User", "general", "en"),
            )
            conn.commit()


def get_or_create_user(
    username: str, role: str = "general", preferred_language: str = "en"
) -> Dict[str, Any]:
    """Retrieves an existing user or creates a new user record."""
    init_db()
    clean_username = username.strip() if username.strip() else "Default User"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (clean_username,))
        row = cursor.fetchone()
        if row:
            return dict(row)

        cursor.execute(
            "INSERT INTO users (username, role, preferred_language) VALUES (?, ?, ?)",
            (clean_username, role, preferred_language),
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return dict(cursor.fetchone())


def list_users() -> List[Dict[str, Any]]:
    """Returns a list of all registered users."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]


def update_user_preference(
    user_id: int, preferred_language: Optional[str] = None, role: Optional[str] = None
) -> None:
    """Updates user language or role preferences."""
    with get_connection() as conn:
        cursor = conn.cursor()
        if preferred_language:
            cursor.execute(
                "UPDATE users SET preferred_language = ? WHERE id = ?",
                (preferred_language, user_id),
            )
        if role:
            cursor.execute(
                "UPDATE users SET role = ? WHERE id = ?",
                (role, user_id),
            )
        conn.commit()


def mark_lesson_completed(user_id: int, category: str, lesson_id: str) -> bool:
    """
    Marks a lesson as completed for the given user.
    Returns True if newly completed, False if already completed.
    """
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO completed_lessons (user_id, category, lesson_id) VALUES (?, ?, ?)",
                (user_id, category, lesson_id),
            )
            conn.commit()
            check_and_update_achievements(user_id)
            return True
        except sqlite3.IntegrityError:
            return False


def get_completed_lessons(user_id: int) -> List[Dict[str, Any]]:
    """Retrieves all completed lessons for a user."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM completed_lessons WHERE user_id = ? ORDER BY completed_at DESC",
            (user_id,),
        )
        return [dict(row) for row in cursor.fetchall()]


def is_lesson_completed(user_id: int, category: str, lesson_id: str) -> bool:
    """Checks whether a specific lesson has been completed by the user."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM completed_lessons WHERE user_id = ? AND category = ? AND lesson_id = ?",
            (user_id, category, lesson_id),
        )
        return cursor.fetchone() is not None


def record_quiz_attempt(
    user_id: int, difficulty: str, score: int, total_questions: int
) -> Dict[str, Any]:
    """Records a quiz attempt and updates badges."""
    init_db()
    percentage = (score / total_questions * 100) if total_questions > 0 else 0.0
    passed = 1 if percentage >= 60.0 else 0
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO quiz_attempts (user_id, difficulty, score, total_questions, percentage, passed)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, difficulty, score, total_questions, round(percentage, 1), passed),
        )
        conn.commit()
        attempt_id = cursor.lastrowid
        check_and_update_achievements(user_id)
        cursor.execute("SELECT * FROM quiz_attempts WHERE id = ?", (attempt_id,))
        return dict(cursor.fetchone())


def get_quiz_attempts(user_id: int) -> List[Dict[str, Any]]:
    """Returns all quiz attempts for a user."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM quiz_attempts WHERE user_id = ? ORDER BY attempted_at DESC",
            (user_id,),
        )
        return [dict(row) for row in cursor.fetchall()]


def record_scam_scan(
    user_id: int,
    sample_title: str,
    risk_level: str,
    risk_score: int,
    detected_triggers: str,
) -> None:
    """Logs a scan performed in the Online Scam Checker."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO scam_scans (user_id, sample_title, risk_level, risk_score, detected_triggers)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                sample_title[:120],
                risk_level,
                risk_score,
                detected_triggers[:300],
            ),
        )
        conn.commit()
        award_badge_if_not_present(
            user_id,
            "scam_spotter",
            "Scam Spotter",
            "Analyzed a suspicious message with the Scam Checker.",
        )


def get_scam_scans(user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """Returns recent scam scans performed by the user."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM scam_scans WHERE user_id = ? ORDER BY scanned_at DESC LIMIT ?",
            (user_id, limit),
        )
        return [dict(row) for row in cursor.fetchall()]


def award_badge_if_not_present(
    user_id: int, badge_key: str, badge_title: str, description: str
) -> bool:
    """Awards an achievement badge if not already earned."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO badges (user_id, badge_key, badge_title, description)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, badge_key, badge_title, description),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def get_user_badges(user_id: int) -> List[Dict[str, Any]]:
    """Returns all badges earned by the user."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM badges WHERE user_id = ? ORDER BY earned_at ASC", (user_id,)
        )
        return [dict(row) for row in cursor.fetchall()]


def check_and_update_achievements(user_id: int) -> None:
    """Evaluates user milestones and awards corresponding badges."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()

        # Count completed lessons
        cursor.execute(
            "SELECT COUNT(*) as count FROM completed_lessons WHERE user_id = ?",
            (user_id,),
        )
        lesson_count = cursor.fetchone()["count"]

        # Count by category
        cursor.execute(
            "SELECT category, COUNT(*) as count FROM completed_lessons WHERE user_id = ? GROUP BY category",
            (user_id,),
        )
        cat_counts = {row["category"]: row["count"] for row in cursor.fetchall()}

        # Count quiz attempts & highest score
        cursor.execute(
            "SELECT COUNT(*) as count, MAX(percentage) as best_pct, SUM(passed) as passes FROM quiz_attempts WHERE user_id = ?",
            (user_id,),
        )
        quiz_stats = cursor.fetchone()
        quiz_count = quiz_stats["count"] or 0
        best_pct = quiz_stats["best_pct"] or 0.0
        quiz_passes = quiz_stats["passes"] or 0

    # Milestone 1: First Shield (First lesson completed)
    if lesson_count >= 1:
        award_badge_if_not_present(
            user_id,
            "first_shield",
            "First Shield",
            "Completed your first digital safety lesson.",
        )

    # Milestone 2: Quiz Novice (Completed first quiz)
    if quiz_count >= 1:
        award_badge_if_not_present(
            user_id,
            "quiz_novice",
            "Quiz Explorer",
            "Completed your first interactive cybersecurity quiz.",
        )

    # Milestone 3: Cyber Sentinel (Scored 80%+ on any quiz)
    if best_pct >= 80.0:
        award_badge_if_not_present(
            user_id,
            "cyber_sentinel",
            "Cyber Sentinel",
            "Achieved an outstanding score of 80% or higher in the quiz.",
        )

    # Milestone 4: Elder Guardian (Senior citizen module explored)
    if cat_counts.get("senior_citizen", 0) >= 2:
        award_badge_if_not_present(
            user_id,
            "elder_guardian",
            "Elder Guardian",
            "Explored senior citizen banking safety and anti-fraud modules.",
        )

    # Milestone 5: Scholar Shield (Student zone lessons completed)
    if cat_counts.get("student_zone", 0) >= 2:
        award_badge_if_not_present(
            user_id,
            "scholar_shield",
            "Scholar Shield",
            "Mastered student cybersecurity and social media protection topics.",
        )

    # Milestone 6: Master Defender (Completed 10+ lessons & 3 quizzes)
    if lesson_count >= 8 and quiz_passes >= 2:
        award_badge_if_not_present(
            user_id,
            "master_defender",
            "Cyber Master Defender",
            "Demonstrated exceptional mastery across all digital safety disciplines.",
        )


def get_user_dashboard_stats(user_id: int) -> Dict[str, Any]:
    """Aggregates all stats for the user progress dashboard."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()

        # Lessons count
        cursor.execute(
            "SELECT COUNT(*) as count FROM completed_lessons WHERE user_id = ?",
            (user_id,),
        )
        total_lessons = cursor.fetchone()["count"]

        # Lessons per category
        cursor.execute(
            "SELECT category, COUNT(*) as count FROM completed_lessons WHERE user_id = ? GROUP BY category",
            (user_id,),
        )
        category_breakdown = {
            row["category"]: row["count"] for row in cursor.fetchall()
        }

        # Quiz stats
        cursor.execute(
            """
            SELECT 
                COUNT(*) as attempts,
                AVG(percentage) as avg_score,
                MAX(percentage) as high_score,
                SUM(passed) as total_passed
            FROM quiz_attempts 
            WHERE user_id = ?
            """,
            (user_id,),
        )
        q_row = cursor.fetchone()
        attempts = q_row["attempts"] or 0
        avg_score = round(q_row["avg_score"] or 0.0, 1)
        high_score = round(q_row["high_score"] or 0.0, 1)
        total_passed = q_row["total_passed"] or 0

        # Scans count
        cursor.execute(
            "SELECT COUNT(*) as count FROM scam_scans WHERE user_id = ?", (user_id,)
        )
        scans_count = cursor.fetchone()["count"]

        # Badges
        cursor.execute(
            "SELECT COUNT(*) as count FROM badges WHERE user_id = ?", (user_id,)
        )
        badges_count = cursor.fetchone()["count"]

    # Calculate rank tier
    if total_lessons >= 10 and total_passed >= 3:
        rank_tier = "Cyber Master"
        rank_icon = "👑"
    elif total_lessons >= 6 or total_passed >= 2:
        rank_tier = "Cyber Guardian"
        rank_icon = "🛡️"
    elif total_lessons >= 2 or attempts >= 1:
        rank_tier = "Cyber Sentinel"
        rank_icon = "⚡"
    else:
        rank_tier = "Cyber Recruit"
        rank_icon = "🔰"

    return {
        "total_lessons": total_lessons,
        "category_breakdown": category_breakdown,
        "quiz_attempts": attempts,
        "quiz_avg_score": avg_score,
        "quiz_high_score": high_score,
        "quiz_passed": total_passed,
        "scams_scanned": scans_count,
        "badges_count": badges_count,
        "rank_tier": rank_tier,
        "rank_icon": rank_icon,
    }


# Auto-initialize database on import
init_db()
