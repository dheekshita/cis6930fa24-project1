import pytest
from redactor import identify_concept
def test_concept():
    text = "Alice has a house. Her son lives in it. They refer to it as their Dream Mansion"
    concept = "house"
    expected = "██████████████████ Her son lives in it. ███████████████████████████████████████"
    assert identify_concept(text, [concept])  == expected

if __name__ == '__main__':
    pytest.main()
