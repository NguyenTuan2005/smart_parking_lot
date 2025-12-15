from dao.CustomerDAO import CustomerDAO
from dao.MonthlyCardDAO import MonthlyCardDAO
from dao.VehicleDAO import VehicleDAO


class MonthlyCardController:
    def __init__(self, view):
        self.view = view
        self.dao = MonthlyCardDAO(CustomerDAO(), VehicleDAO())
        # self._bind_events()
        self.load_data()

    # def _bind_events(self):
        # self.view.btnAddCard.clicked.connect(self.on_add)
        # self.view.txtSearchCardCode.textChanged.connect(self.on_search)
        #
        # self.view.viewRequested.connect(self.on_view)
        # self.view.editRequested.connect(self.on_edit)
        # self.view.deleteRequested.connect(self.on_delete)

    def load_data(self, ):
        cards = self.dao.get_all()

        self.view.set_table_data(cards)
