import sqlite3
from tools import FILE_PATH
import random


class TopicManager:
    def __init__(self):
        conn = sqlite3.connect(FILE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, topic FROM topics")
        self.topics = {topic: id for id, topic in cursor.fetchall()}
        conn.close()


class CardManager:
    def __init__(self, topics):
        conn = sqlite3.connect(FILE_PATH)
        cursor = conn.cursor()
        if len(topics) > 0:
            placeholders = ",".join("?" * len(topics))
            query = f"SELECT ru, eng FROM cards WHERE topic IN ({placeholders})"
            cursor.execute(query, tuple(topics))
        else:
            query = f"SELECT ru, eng FROM cards"
            cursor.execute(query)
        self.cards = cursor.fetchall()
        random.shuffle(self.cards)
        self.cards = self.cards.__iter__()
        conn.close()
        self.current_card = self.cards.__next__()

    def check_input(self, inpt: str):
        if inpt == self.current_card[1]:
            return True
        else:
            return False

    def next_card(self):
        try:
            self.current_card = self.cards.__next__()
            return True
        except StopIteration:
            return False