import pytest
from redactor import identify_dates
def test_dates():
    text = "Some important dates in history are July 22, 2019; October 28 and also 12/25/2022"
    expected = {"July 22, 2019", "October 28", "12/25/2022"}
    assert set(identify_dates(text))  == expected

if __name__ == '__main__':
    pytest.main()
