from import_module_package.application.db.people import get_employees
from import_module_package.application.salary import calculate_salary as alias
from datetime import datetime


current_date = datetime.date(datetime.now())
print(current_date)


if __name__ == '__main__':
    alias()
    get_employees()




