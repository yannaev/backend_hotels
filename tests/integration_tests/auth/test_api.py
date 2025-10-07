import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ('ivan@me.com', '1234', 200),
    ('sss@kkf.com', 'abcd', 200),
    ('invalid-email', '1234', 422),
    ])
async def test_register_user(email, password, status_code, ac):
    register_response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password
        }
    )
    assert register_response.status_code == status_code

    login_response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    if status_code == 200:
        assert login_response.status_code == 200
        assert ac.cookies['access_token']
    else:
        assert login_response.status_code == 422

    me_response = await ac.get("/auth/me")
    if status_code == 200:
        assert me_response.status_code == 200
        res = me_response.json()
        assert isinstance(res, dict)
        assert "id" in res
        assert "email" in res
        assert res["email"] == email
    else:
        assert me_response.status_code == 401

    logout_response = await ac.post('/auth/logout')
    assert logout_response.status_code == 200
    assert 'access_token' not in ac.cookies