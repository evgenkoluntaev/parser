class Vacancy:
    def __init__(self, salary = "0"):
        self.__salary = self.__salary_parser(salary)

    def get_salary(self):            
        return self.__salary

    def set_salary(self, new_salary):
        self.__salary = new_salary

    def __salary_parser(self, salary):
        temp = salary.split()

        try:
            t = (int(temp[0]) + int(temp[1].split('-')[1]))/2*1000

        except:
            t = (int(temp[1]))*1000

        if temp[-1] == "USD":
            t = t* 71
        elif temp[-1] == "EUR":
            t = t* 83
        return t
