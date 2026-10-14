from main import encode_phone, fix_email, fix_postal_zip


def test_fix_email():
    assert fix_email("john@yahoo.com") == "john@gmail.com"


def test_fix_postal_zip():
    assert fix_postal_zip("M5V-3A8") == 538


def test_fix_postal_zip_numeric():
    assert fix_postal_zip(60614) == 60614


def test_encode_phone():
    assert encode_phone("(816) 530-4269") == "QAOOE"


def test_encode_phone_second_example():
    assert encode_phone("1-811-920-9732") == r"OO\OI"