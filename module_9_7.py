def is_prime(func):
    def wrapper(*args):
        number = func(*args)
        for i in range(2, number):
            if number % i == 0:
                print("Составное")
                break
        else:
            print("Простое")

        return number

    return wrapper


@is_prime
def sum_three(*args):
    return sum(args)


result = sum_three(2, 3, 6)
print(result)

