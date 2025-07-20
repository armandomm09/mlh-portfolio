import unittest
import os

os.environ['TESTING'] = 'true'

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Portfolio</title>" in html
        assert '<img src="./static/img/armando.jpg">' in html
        assert '<img src="./static/img/fiona_laygo.png">' in html
        

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json_data = response.get_json()
        assert "timeline_posts" in json_data
        assert len(json_data["timeline_posts"]) == 0
        post_response = self.client.post(
            "/api/timeline_post",
            data={"name": "Alice", "email": "alice@example.com", "content": "First post!"}
        )
        assert post_response.status_code == 200
        post_json = post_response.get_json()
        assert post_json["name"] == "Alice"
        assert post_json["email"] == "alice@example.com"
        assert post_json["content"] == "First post!"
        
        response = self.client.get("/api/timeline_post")
        json_data = response.get_json()
        assert len(json_data["timeline_posts"]) == 1
        assert json_data["timeline_posts"][0]["name"] == "Alice"

    def test_malformed_timeline_post(self):
        # Missing name
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": "Hello world, I'm John!"}
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # Empty content
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "john@example.com", "content": ""}
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # Invalid email
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"}
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
