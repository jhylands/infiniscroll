from neo.main import get_user, get_items

def test_get_user():
    assert get_user(1).name == "James"

def test_get_items():
    a = list(get_items(None))
    print(a[0].url)
    assert len(a)==2
