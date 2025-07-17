#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auth Manager - Quản lý xác thực đăng nhập
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Tuple, Dict, Optional
from PyQt6.QtCore import QSettings

from constants import DEFAULT_USERNAME, DEFAULT_PASSWORD


class AuthManager:
    """Quản lý đăng nhập, phân quyền, ghi log"""
    def __init__(self):
        self.users = {"admin": self.hash_password("admin")}
        self.current_user = None

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username, password):
        if username in self.users and self.users[username] == self.hash_password(password):
            self.current_user = username
            return True
        return False

    def logout(self):
        self.current_user = None

    def is_logged_in(self):
        return self.current_user is not None 