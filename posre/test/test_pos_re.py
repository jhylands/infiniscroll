import pytest
from posre.match import match


@pytest.mark.parametrize("posgex, string", [
    ("[NOUN]", "cat")])
def test_positive_match(posgex, string):
    # Testing string that should positivly match
    assert match(f"^{posgex}$", string)

@pytest.mark.parametrize("posgex, string", [
    ("[NOUN]", "the")])
def test_negative_match(posgex, string):
    # Testing string that should positivly match
    assert match(f"^{posgex}$", string) is None


