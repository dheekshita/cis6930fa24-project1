import pytest
from redactor import identify_phones
def test_phones():
    text = "You can contact me via 123-456-7890 or (123) 456-7890 or 1234567890"
    expected = {"123-456-7890", "123) 456-7890", "1234567890"}
    assert set(identify_phones(text))  == expected

if __name__ == '__main__':
    pytest.main()
