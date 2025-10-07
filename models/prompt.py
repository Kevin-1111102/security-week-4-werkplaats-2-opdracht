from datetime import date

from models.database import Database


class Prompt:
    def __init__(self):
        database = Database('./databases/database.db')
        self.cursor, self.con = database.connect_db()

    def get_total_prompts(self):
        self.cursor.execute("SELECT COUNT(*) FROM prompts")
        data = self.cursor.fetchone()
        return data[0] if data else 0

    def get_all_prompts(self, page, per_page, filters=None):

        offset = (page - 1) * per_page

        query_get_prompts = "SELECT * FROM prompts WHERE 1=1"
        query_get_total_prompts = "SELECT COUNT(*) FROM prompts WHERE 1=1"
        params = []

        if filters:
            # Apply filters
            if filters.get("prompts_id"):
                query_get_prompts += " AND prompts_id LIKE ?"
                query_get_total_prompts += " AND prompts_id LIKE ?"
                params.append(f"%{filters['prompts_id']}%")
            if filters.get("prompt"):
                query_get_prompts += " AND prompt LIKE ?"
                query_get_total_prompts += " AND prompt LIKE ?"
                params.append(f"%{filters['prompt']}%")

        query_get_prompts += " LIMIT ? OFFSET ?"
        params_get_prompts = params + [per_page, offset]

        # Execute the query
        self.cursor.execute(query_get_prompts, params_get_prompts)
        result = self.cursor.fetchall()

        self.cursor.execute(query_get_total_prompts, params)
        total_prompts = self.cursor.fetchone()[0]

        return result, total_prompts

    def get_single_prompt(self, prompt_id):
        self.cursor.execute(
            "SELECT u.*, p.* FROM prompts p inner join users u on p.user_id = u.user_id WHERE prompts_id = ?",
            (prompt_id,))
        prompt = self.cursor.fetchone()
        return prompt

    def get_prompts(self):
        result = self.cursor.execute("SELECT * FROM prompts").fetchall()
        return result

    # TODO use correct user id
    def create_prompt(self, title, prompt, user_id=3, curr_date=date.today(),
                      categorized=0, correct=0, incorrect=0):
        self.cursor.execute(
            "INSERT INTO prompts (user_id, title, prompt, date, categorized, correct, incorrect) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, title, prompt, curr_date, categorized, correct, incorrect))
        self.con.commit()
        return True

    def update_prompt(self, prompt_id, title, prompt):
        self.cursor.execute("""
                UPDATE prompts
                SET title = ?, prompt = ?
                WHERE prompts_id = ?;
            """, (title, prompt, prompt_id))
        self.con.commit()  # Commit the transaction

    def delete_prompt(self, prompt_id):
        self.cursor.execute("DELETE FROM prompts WHERE prompts_id=?", (str(prompt_id),))
        self.con.commit()
