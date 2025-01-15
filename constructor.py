"""Constructor exercise."""


class Empty:
    """An empty class without constructor."""


    pass


class Person:
    """Represent person with firstname, lastname and age."""
    def __init__(self, firstname="", lastname="", age=0):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age

    pass


class Student:
    """Represent student with firstname, lastname and age."""
    def __init__(self, firstname, lastname, age):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age

    pass


if __name__ == '__main__':
    # empty usage
    nothing = Empty()
    print(nothing)

    # 3 x person usage
    person_1 = Person()
    person_1.firstname = "Karl"
    person_1.lastname = "Kala"
    person_1.age = 16

    person_2 = Person()
    person_2.firstname = "Juhan"
    person_2.lastname = "Martinson"
    person_2.age = 45

    person_3 = Person()
    person_3.firstname = "Mari"
    person_3.lastname = "Klaas"
    person_3.age = 2

    # 3 x student usage
    student_1 = Student()
    student_1.firstname = "Karl"
    student_1.lastname = "Kala"
    student_1.age = 16
    
    student_2 = Student()
    student_2.firstname = "Juhan"
    student_2.lastname = "Martinson"
    student_2.age = 45
    
    student_3 = Student()
    student_3.firstname = "Mari"
    student_3.lastname = "Klaas"
    student_3.age = 2
    pass
