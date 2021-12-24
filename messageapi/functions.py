from .models import PhoneNumber


def is_number_valid(n):
    n = len(str(n))
    if n > 5 and n < 17:
        return True
    else:
        return False


def get_phonenumber_obj(n):
    try:
        number = PhoneNumber.objects.get(number=n)

    except PhoneNumber.DoesNotExist:
        return -1
    return number
