from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def load_test(self):
        self.client.get("/")
        self.client.get("/page2")
        self.client.get("/page3")
        self.client.get("/api")
        self.client.get("/pages")
        self.client.get("/home")
        self.client.get("/aboutme")
        self.client.get("/contact")
        self.client.get("/api/users")
        self.client.get("/api/posts")
        self.client.get("/api/comments")
        self.client.get("/api/likes")
        self.client.get("/api/followers")
        self.client.get("/api/following")
        self.client.get("/api/friends")
        self.client.get("/api/messages")
        self.client.get("/api/chats")
        self.client.get("/api/groups")