from Selenium2Library import Selenium2Library


class CustomSeleniumLibrary(Selenium2Library):
    def get_table_row_count(self, table_locator):
        table = self._table_element_finder.find(self._current_browser(), table_locator)
        if table is not None:
            return len(table.find_elements_by_xpath("./tbody/tr"))
        raise AssertionError("Cell in table %s could not be found." % table_locator)
