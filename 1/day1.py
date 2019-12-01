DATA_FILEPATH = "data.txt"

def read_data(filepath):
    with open(filepath) as fd:
        return fd.readlines()

def calculate_required_fuel(mass):
    required_fuel = 0

    while(mass > 0):
        fuel_this_step = (mass // 3) - 2
        if (fuel_this_step <= 0):
            break

        ## Reset the loop to begin calculating fuel needed for the added fuel
        mass = fuel_this_step
        required_fuel += fuel_this_step

    return required_fuel

def main():
    masses = read_data(DATA_FILEPATH)

    total = 0
    for mass in masses:
        total += calculate_required_fuel(int(mass))

    print(total)

if (__name__ == '__main__'):
    ## Sanity checks
    assert (calculate_required_fuel(14) == 2)
    assert (calculate_required_fuel(1969) == 966)
    assert (calculate_required_fuel(100756) == 50346)

    main()
