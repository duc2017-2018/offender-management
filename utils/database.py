#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Manager - Quản lý cơ sở dữ liệu SQLite
"""

import sqlite3


class LegacyDatabaseManager:
    """Không dùng class này cho app chính. Chỉ dùng cho script cũ hoặc test."""
    def __init__(self, db_path="data/database.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor

    def fetchall(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetchone(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        self.conn.close() 