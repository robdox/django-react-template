import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

User = get_user_model()

TEST_PASSWORD = {
    "password1": "aaAA11!!!!",
    "password2": "aaAA11!!!!",
}

TEST_USER = {
    "email": "testuser@user.com",
}


@pytest.fixture(scope="class")
def setup():
    # Lets set up our test user
    User.objects.create_user(
        email=TEST_USER["email"],
        password=TEST_PASSWORD["password1"],
    )


@pytest.mark.usefixtures("setup")
class TestAccountsAPI(APITestCase):
    def test_health_check(self):
        client = APIClient()
        response = client.get("/health_check/")
        assert response.status_code == 200

    def test_user_login(self):
        client = APIClient()

        # Should fail to verify a user as we are not logged in
        response = client.get("/api/accounts/users/verify/")
        assert response.status_code == 401

        # Lets login as user
        response = client.post(
            "/api/auth/login/",
            {"email": TEST_USER["email"], "password": TEST_PASSWORD["password1"]},
        )
        assert response.status_code == 200
        assert "key" in response.data
        token = response.data["key"]
        client.credentials(HTTP_AUTHORIZATION="Token %s" % token)

        # Verify their token is valid
        response = client.get("/api/accounts/users/verify/")

        assert "email" in response.data
        assert "first_name" in response.data
        assert "last_name" in response.data

        response = client.get(f"/api/accounts/users/{TEST_USER['email']}/")
        assert response.status_code == 200
        assert response.data["email"] == TEST_USER["email"]

        # Lets logout
        response = client.post("/api/auth/logout/")
        assert response.status_code == 200

        # Gotta clear the token from DRF too, its weird
        client.logout()

    def test_user_retrieve(self):
        client = APIClient()

        # Should fail we are not logged in
        response = client.get(f"/api/accounts/users/{TEST_USER['email']}/")
        assert response.status_code == 401

        # Lets login as user
        response = client.post(
            "/api/auth/login/",
            {"email": TEST_USER["email"], "password": TEST_PASSWORD["password1"]},
        )
        assert response.status_code == 200
        assert "key" in response.data
        token = response.data["key"]
        client.credentials(HTTP_AUTHORIZATION="Token %s" % token)

        # Should pass we are not logged in
        response = client.get(f"/api/accounts/users/{TEST_USER['email']}/")
        assert response.status_code == 200
        assert response.data["email"] == TEST_USER["email"]

    def test_user_update(self):
        client = APIClient()

        # Should fail we are not logged in
        response = client.put(
            f"/api/accounts/users/{TEST_USER['email']}/", {"first_name": "Robert"}
        )
        assert response.status_code == 401

        # Lets login as user
        response = client.post(
            "/api/auth/login/",
            {"email": TEST_USER["email"], "password": TEST_PASSWORD["password1"]},
        )
        assert response.status_code == 200
        assert "key" in response.data
        token = response.data["key"]
        client.credentials(HTTP_AUTHORIZATION="Token %s" % token)

        # Gonna change the first name
        NEW_FIRST_NAME = "Robert"

        # Lets make sure the first name is not set
        response = client.get(f"/api/accounts/users/{TEST_USER['email']}/")
        assert response.status_code == 200
        assert response.data["first_name"] != NEW_FIRST_NAME

        # Now lets change it
        response = client.put(
            f"/api/accounts/users/{TEST_USER['email']}/", {"first_name": "Robert"}
        )
        assert response.status_code == 200

        # And verify it changed
        response = client.get(f"/api/accounts/users/{TEST_USER['email']}/")
        assert response.status_code == 200
        assert response.data["first_name"] == NEW_FIRST_NAME

        # Finally, try to change a different users info, should fail
        NEW_USER_EMAIL = "test@test.test"
        User.objects.create_user(
            email=NEW_USER_EMAIL, password=TEST_PASSWORD["password1"]
        )
        # Now lets try to change it (and fail)
        response = client.put(
            f"/api/accounts/users/{NEW_USER_EMAIL}/", {"first_name": "Steve"}
        )
        assert response.status_code == 403

        # But lets verify we can retrieve their data thats fine
        response = client.get(f"/api/accounts/users/{NEW_USER_EMAIL}/")
        assert response.status_code == 200
        assert response.data["email"] == NEW_USER_EMAIL

    # Really, delete just sets in_active to False
    def test_user_delete(self):
        client = APIClient()

        # Should fail we are not logged in
        response = client.delete(f"/api/accounts/users/{TEST_USER['email']}/")
        assert response.status_code == 401

        user = User.objects.get(email=TEST_USER["email"])
        assert user.is_active is True

        # Lets login as user
        response = client.post(
            "/api/auth/login/",
            {"email": TEST_USER["email"], "password": TEST_PASSWORD["password1"]},
        )
        assert response.status_code == 200
        assert "key" in response.data
        token = response.data["key"]
        client.credentials(HTTP_AUTHORIZATION="Token %s" % token)

        # Try to delete a different account its gonna fial
        NEW_USER_EMAIL = "test@test.test"
        User.objects.create_user(
            email=NEW_USER_EMAIL, password=TEST_PASSWORD["password1"]
        )
        response = client.delete(f"/api/accounts/users/{NEW_USER_EMAIL}/")
        assert response.status_code == 403

        # Now lets actually delete it should work
        response = client.delete(f"/api/accounts/users/{TEST_USER['email']}/")
        assert response.status_code == 204

        user = User.objects.get(email=TEST_USER["email"])
        assert user.is_active is False


class AccountsTests(APITestCase):
    def test_create_user(self):
        email = "test@test.com"
        user = User.objects.create_user(
            email=email, password=TEST_PASSWORD["password1"]
        )
        assert user.email == email
        assert str(user) == email

    def test_create_user_no_password(self):
        user = User.objects.create_user(
            email="nopassword@user.com",
        )

        assert user.email == "nopassword@user.com"
        assert str(user) == "nopassword@user.com"

    def test_fail_create_user(self):
        with pytest.raises(ValueError):
            User.objects.create_user(email="hi", password="hello")
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="")

    def test_create_superuser(self):
        user = User.objects.create_superuser(email="hi@superuser.com", password="hello")
        assert user.email == "hi@superuser.com"
        assert str(user) == "hi@superuser.com"

    def test_fail_create_superuser(self):
        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email="hi@superuser.com",
                password="hello",
                is_staff=False,
            )
        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email="hi@superuser.com",
                password="hello",
                is_superuser=False,
            )
