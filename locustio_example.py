#!/usr/bin/env python
# encoding: utf-8

from locust import HttpLocust, TaskSet

def login(l):
    l.client.post("/api/user/login", {"phone":"18500426633", "password":"111111"})

def index(l):
    l.client.get("/")

def profile(l):
    l.client.get("/api/user/info")

class UserBehavior(TaskSet):
    tasks = {index:2, profile:1}

    def on_start(self):
        login(self)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
