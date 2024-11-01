import pytest
from redactor import identify_address
def test_addresses():
    text = "My location is 123 Main Street, Springfield, IL 62704; and work location is 345 Pine Road"
    expected = {"123 Main Street", "Springfield, IL 62704", "345 Pine Road"}
    assert set(identify_address(text))  == expected

if __name__ == '__main__':
    pytest.main()
