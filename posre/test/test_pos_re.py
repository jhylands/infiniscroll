import pytest
from posre.match import match, compile


@pytest.mark.parametrize("posgex, string", [
    ("[NOUN]", "cat"),
    ("[VERB]", "run")])
def test_positive_match(posgex, string):
    # Testing string that should positivly match
    assert match(f"^{posgex}$", string)


@pytest.mark.parametrize("posgex, string", [
    ("[NOUN]", "the")])
def test_negative_match(posgex, string):
    # Testing string that should positivly match
    assert match(f"^{posgex}$", string) is None


compiled_search = compile("^[DETERMINER] [NOUN] [VERB]$")

def test_compiled():
    assert compiled_search.match("the cat sleep")
    assert compiled_search.match("a dog sit")
    assert compiled_search.match("some dog eat")
    assert compiled_search.match("not at all") is None
    assert compiled_search.match("any sleep dog") is None
    
