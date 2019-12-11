def is_valid_password_part_two(digits):
    ## Check for 6 digits
    if (digits < 100000 or digits >= 1000000):
        return False

    ## This should be faster than the obvious int() and str() conversions, right?
    digit_list = []
    always_descending = True    ## Note that this iterates backwards, so we're checking for a descent instead
    last_digit = 10 ## No single digit can be bigger than this, so it's a good starting spot for the comparison
    while (digits != 0 and always_descending):
        digit = digits % 10
        
        if (last_digit < digit):
            always_descending = False

        last_digit = digit
        digit_list.append(digit)
        digits //= 10

    ## From inside out:
    ## - Builds a set of the digits, so there's only one of each
    ## - Use list comprehension to build a new list containing the count of every digit in the set
    ## - Check if any of those counts are equal to 2, and thus is a valid password
    contains_double_digit = any(digit_count == 2 for digit_count in [digit_list.count(digit) for digit in set(digit_list)])
    
    return always_descending and contains_double_digit


def is_valid_password_part_one(digits):
    ## Check for 6 digits
    if (digits < 100000 or digits >= 1000000):
        return False

    ## This should be faster than the obvious int() and str() conversions, right?
    always_descending = True    ## Note that this iterates backwards, so we're checking for a descent instead
    contains_double_digit = False
    last_digit = 10 ## No single digit can be bigger than this, so it's a good starting spot for the comparison
    while (digits != 0 and always_descending):
        digit = digits % 10

        if (last_digit == digit):
            contains_double_digit = True
        
        if (last_digit < digit):
            always_descending = False

        last_digit = digit
        digits //= 10
    
    return always_descending and contains_double_digit


def find_valid_passwords(validation_func, start, end):
    valid_passwords = []
    for candidate in range(start, end + 1):
        if (validation_func(candidate)):
            valid_passwords.append(candidate)

    return valid_passwords


if (__name__ == '__main__'):
    ## Sanity checks
    assert(is_valid_password_part_one(0) == False)
    assert(is_valid_password_part_one(1234567) == False)
    assert(is_valid_password_part_one(111111) == True)
    assert(is_valid_password_part_one(223450) == False)
    assert(is_valid_password_part_one(123789) == False)

    assert(is_valid_password_part_two(112233) == True)
    assert(is_valid_password_part_two(123444) == False)
    assert(is_valid_password_part_two(111122) == True)

    valid_passwords_part_one = find_valid_passwords(is_valid_password_part_one, 178416, 676461)
    print("Part 1: {} different passwords".format(len(valid_passwords_part_one)))

    valid_passwords_part_two = find_valid_passwords(is_valid_password_part_two, 178416, 676461)
    print("Part 2: {} different passwords".format(len(valid_passwords_part_two)))
    