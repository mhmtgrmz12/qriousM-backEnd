from database import execute_sql_query
from typing import Optional
import random


SCHEMA = "qriousmindsdb"

fetch_question_by_id = f"""
SELECT * FROM {SCHEMA}.question WHERE questionId = %s;
"""

fetch_question_all = f"""
SELECT * FROM {SCHEMA}.question
"""

fetch_correct_answer = f"""
SELECT correctAnswer FROM {SCHEMA}.question WHERE questionId = %s;
"""

def fetch_question(id: Optional[int], category: Optional[str], difficulty: Optional[str], type: Optional[str] = None):
    if id is not None:
        result = execute_sql_query(fetch_question_by_id, (id,))
        if not result or isinstance(result, Exception):
            return None
        row = result[0]
    else:
        filters = []
        values = []
        sql = fetch_question_all

        if category:
            filters.append("category = %s")
            values.append(category)
        if difficulty:
            filters.append("difficulty = %s")
            values.append(difficulty)
        if type:
            filters.append("\"type\" = %s")
            values.append(type)

        if filters:
            sql += " WHERE " + " AND ".join(filters)

        result = execute_sql_query(sql, tuple(values))
        if not result or isinstance(result, Exception):
            return None

        row = random.choice(result) if result else None

    if row:
        return {
            "id": row[0],
            "category": row[1],
            "difficulty": row[2],
            "type": row[3],
            "question": row[4],
            "choice1": row[5],
            "choice2": row[6],
            "choice3": row[7],
            "choice4": row[8],
            "correctAnswer": row[9]
        }

    return None

def get_correct_answer(id: int):
    result = execute_sql_query(fetch_correct_answer, (id,))
    if result and not isinstance(result, Exception):
        return result[0][0]
    return None
