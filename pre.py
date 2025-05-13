class User:
    def __init__(self, name, birth_year):
        self.cur_year = 2025
        self.name = name
        self.birth_year = birth_year

    def get_name(self):
        print(self.name.capitalize())

    def age(self):
        age = self.cur_year - self.birth_year
        print(age)


if __name__ == '__main__':
    momo = User('Momo', 1986)
    misha = User('Misha', 1999)

    momo.get_name()
    momo.age()

    misha.get_name()
    misha.age()
