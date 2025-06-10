class Rules:
    """
    Klasa definiująca zasady gry — które komórki przeżywają, a które się rodzą.

    :param survive: Reguły przeżycia jako string z cyframi (np. "23").
    :param born: Reguły narodzin jako string z cyframi (np. "3").
    """

    def __init__(self, survive, born):
        self.set_rules(survive, born)

    def set_rules(self, survive, born):
        """
        Aktualizuje reguły przeżycia i narodzin.

        :param survive: String z cyframi określającymi liczbę sąsiadów potrzebną do przeżycia.
        :param born: String z cyframi określającymi liczbę sąsiadów potrzebną do narodzin.
        """
        self.keep_alive = [0] * 9
        self.revive = [0] * 9
        for i in survive:
            self.keep_alive[int(i)] = 1
        for i in born:
            self.revive[int(i)] = 1

    def is_alive_next(self, neighbors):
        """
        Sprawdza, czy żywa komórka przeżyje.

        :param neighbors: Liczba żywych sąsiadów.
        :return: True jeśli komórka przeżyje, False jeśli umrze.
        :rtype: bool
        """
        return self.keep_alive[neighbors] == 1

    def should_be_born(self, neighbors):
        """
        Sprawdza, czy martwa komórka powinna się narodzić.

        :param neighbors: Liczba żywych sąsiadów.
        :return: True jeśli komórka się narodzi, False w przeciwnym razie.
        :rtype: bool
        """
        return self.revive[neighbors] == 1
