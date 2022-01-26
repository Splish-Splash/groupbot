# from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
#
#
# Base = declarative_base()
#
#
# class Query(Base):
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255), nullable=True)
#     def __init__(self, name):
#         __tablename__ = name
#         for i in range(1, 31):
from dataclasses import dataclass


class Query:

    def __init__(self, name, query=None):
        print(name)
        print(query)
        self.name = name
        self.query = [None] * 25
        if query is not None:
            for i in range(len(query)):
                self.query[i] = query[i] if query[i] != 'None' else None

    def set(self, id, nick):
        if self.query[id-1] not in (nick, None):
            return
        if self.query[id-1] == nick:
            self.query[id-1] = None
            return
        self.query[id - 1] = nick if self.query[id - 1] is None else self.query[id - 1]
        for i, el in enumerate(self.query):
            if el == nick and i + 1 != id:
                self.query[i] = None

    def __repr__(self):
        s = self.name + '\n'
        for i, el in enumerate(self.query):
            s += f'{i+1}. {el if el is not None else ""} \n'
        return s