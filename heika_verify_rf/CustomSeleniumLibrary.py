from Selenium2Library import Selenium2Library


def _get_table_field_value(element, field):
    # return element.find_element_by_xpath("./td[@field='" + field + "']").get_text().strip()
    return element.find_element_by_xpath("./td[@field='" + field + "']").text.strip()


class CustomSeleniumLibrary(Selenium2Library):
    def get_table_row_count(self, table_locator):
        table = self._table_element_finder.find(self._current_browser(), table_locator)
        if table is not None:
            return len(table.find_elements_by_xpath("./tbody/tr"))
        raise AssertionError("Cell in table %s could not be found." % table_locator)

    def get_user_search_results(self, table_locator, row_index):
        table = self._table_element_finder.find(self._current_browser(), table_locator)
        ret = []
        if table is not None:
            rows = table.find_elements_by_xpath("./tbody/tr")
            if len(rows) <= 0:
                return None
            row_index = int(row_index)
            if len(rows)-1 < row_index:
                raise AssertionError("The row index '%s' is large than row length '%s'." % (row_index, len(rows)))
            for row in rows:
                dic = {
                    'userId': _get_table_field_value(row, 'userId'),
                    'nickName': _get_table_field_value(row, 'nickName'),
                    'realName': _get_table_field_value(row, 'realName'),
                    'mobile': _get_table_field_value(row, 'mobile'),
                    'idNo': _get_table_field_value(row, 'idNo'),
                    'userType': _get_table_field_value(row, 'userType'),
                    'verifyUserStatus': _get_table_field_value(row, 'verifyUserStatus'),
                    'operater': _get_table_field_value(row, 'operater'),
                    'operateTime': _get_table_field_value(row, 'operateTime'),
                }
                ret.append(dic)
            return ret[row_index]
        else:
            return None

