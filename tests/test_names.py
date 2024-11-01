import pytest
from redactor import identify_names
def test_names():
    text = "Jane Smith, alice_green or Judy"
    expected = {"Jane Smith", "alice_green", "Judy"}
    assert set(identify_names(text))  == expected

if __name__ == '__main__':
    pytest.main()
