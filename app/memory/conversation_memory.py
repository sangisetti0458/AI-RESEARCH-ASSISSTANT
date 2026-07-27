from collections import defaultdict

MAX_MESSAGES = 10


class ConversationMemory:

    def __init__(self):
        self.sessions = defaultdict(list)

    def add_message(self, session_id: str, role: str, content: str):

        self.sessions[session_id].append(
            {
                "role": role,
                "content": content,
            }
        )

        # Keep only the last MAX_MESSAGES
        if len(self.sessions[session_id]) > MAX_MESSAGES:
            self.sessions[session_id] = self.sessions[session_id][-MAX_MESSAGES:]

    def get_history(self, session_id: str):

        return self.sessions.get(session_id, [])

    def clear_history(self, session_id: str):

        if session_id in self.sessions:
            del self.sessions[session_id]


memory = ConversationMemory()