"""
API test suite against JSONPlaceholder (https://jsonplaceholder.typicode.com),
a free, no-auth REST API for testing and prototyping.

Covers GET (list + single + nested resource + 404), POST, PUT, PATCH,
and DELETE across the /posts and /users resources. Note: per
JSONPlaceholder's documented behavior, write operations (POST/PUT/
PATCH/DELETE) return realistic success responses but do not actually
persist data server-side -- tests assert on response shape and status
codes rather than on subsequent reads reflecting the write.
"""
import allure
import pytest

from utils.test_data_factory import TestDataFactory


@allure.feature("API - Posts")
class TestPostsAPI:

    @allure.story("List posts")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_all_posts_returns_200_and_list(self, api_client):
        response = api_client.get("/posts")

        assert response.status_code == 200
        body = response.json()
        assert isinstance(body, list)
        assert len(body) == 100

    @allure.story("Get single post")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_single_post_returns_expected_schema(self, api_client):
        response = api_client.get("/posts/1")

        assert response.status_code == 200
        post = response.json()
        for field in ("id", "userId", "title", "body"):
            assert field in post
        assert post["id"] == 1

    @allure.story("Get nonexistent post")
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.api
    def test_get_nonexistent_post_returns_404(self, api_client):
        response = api_client.get("/posts/9999")

        assert response.status_code == 404

    @allure.story("Filter posts by user")
    @pytest.mark.regression
    @pytest.mark.api
    def test_filter_posts_by_user_id(self, api_client):
        response = api_client.get("/posts", params={"userId": 1})

        assert response.status_code == 200
        posts = response.json()
        assert len(posts) > 0
        assert all(post["userId"] == 1 for post in posts)

    @allure.story("Nested comments")
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_comments_for_a_post(self, api_client):
        response = api_client.get("/posts/1/comments")

        assert response.status_code == 200
        comments = response.json()
        assert len(comments) > 0
        assert all(comment["postId"] == 1 for comment in comments)
        for field in ("id", "name", "email", "body"):
            assert field in comments[0]

    @allure.story("Create post")
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_post_returns_201(self, api_client):
        payload = {
            "title": "QA portfolio test post",
            "body": "Body content created during automated test run",
            "userId": 1,
        }
        response = api_client.post("/posts", json=payload)

        assert response.status_code == 201
        body = response.json()
        assert body["title"] == payload["title"]
        assert body["body"] == payload["body"]
        assert body["userId"] == payload["userId"]
        assert "id" in body

    @allure.story("Update post")
    @pytest.mark.regression
    @pytest.mark.api
    def test_update_post_returns_200(self, api_client):
        payload = {"id": 1, "title": "Updated title", "body": "Updated body", "userId": 1}
        response = api_client.put("/posts/1", json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "Updated title"
        assert body["body"] == "Updated body"

    @allure.story("Partial update post")
    @pytest.mark.regression
    @pytest.mark.api
    def test_patch_post_returns_200(self, api_client):
        response = api_client.patch("/posts/1", json={"title": "Patched title only"})

        assert response.status_code == 200
        assert response.json()["title"] == "Patched title only"

    @allure.story("Delete post")
    @pytest.mark.regression
    @pytest.mark.api
    def test_delete_post_returns_200(self, api_client):
        response = api_client.delete("/posts/1")

        assert response.status_code == 200


@allure.feature("API - Users")
class TestUsersAPI:

    @allure.story("List users")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_all_users_returns_200_and_list(self, api_client):
        response = api_client.get("/users")

        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert len(users) == 10

    @allure.story("Get single user")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_single_user_returns_expected_schema(self, api_client):
        response = api_client.get("/users/1")

        assert response.status_code == 200
        user = response.json()
        for field in ("id", "name", "email", "address", "company"):
            assert field in user

    @allure.story("Get nonexistent user")
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.api
    def test_get_nonexistent_user_returns_404(self, api_client):
        response = api_client.get("/users/9999")

        assert response.status_code == 404

    @allure.story("User's todos")
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_todos_for_a_user(self, api_client):
        response = api_client.get("/users/1/todos")

        assert response.status_code == 200
        todos = response.json()
        assert len(todos) > 0
        assert all(todo["userId"] == 1 for todo in todos)
        for field in ("id", "title", "completed"):
            assert field in todos[0]

    @allure.story("Email format sanity check")
    @pytest.mark.regression
    @pytest.mark.api
    def test_all_users_have_valid_looking_email(self, api_client):
        response = api_client.get("/users")
        users = response.json()

        for user in users:
            assert "@" in user["email"]
            assert "." in user["email"].split("@")[-1]


@allure.feature("API - Todos")
class TestTodosAPI:

    @allure.story("List todos")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_all_todos_returns_200(self, api_client):
        response = api_client.get("/todos")

        assert response.status_code == 200
        todos = response.json()
        assert len(todos) == 200

    @allure.story("Completed todos filter")
    @pytest.mark.regression
    @pytest.mark.api
    def test_filter_completed_todos(self, api_client):
        response = api_client.get("/todos", params={"completed": "true"})

        assert response.status_code == 200
        todos = response.json()
        assert len(todos) > 0
        assert all(todo["completed"] is True for todo in todos)

    @allure.story("Create todo")
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_todo_returns_201(self, api_client):
        payload = {"title": "Write QA automation tests", "completed": False, "userId": 1}
        response = api_client.post("/todos", json=payload)

        assert response.status_code == 201
        body = response.json()
        assert body["title"] == payload["title"]
        assert body["completed"] is False
