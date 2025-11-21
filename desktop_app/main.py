from desktop_app.dao.CardDAO import CardDAO
from desktop_app.dao.CustomerDAO import CustomerDAO

if __name__ == '__main__':
    cardDao = CardDAO()
    print(cardDao.get_all())

    c = CustomerDAO()
    print(c.get_all())   

    