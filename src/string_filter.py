
class StringFilter(str):
    """
    A class for determining if strings meet various
    filtering criteria
    """
    def __new__(cls, string, *args, **kwargs):
        return str.__new__(cls, string)

    def __init__(self, string, match_case=True):
        """
        :param string: the string which filtering is to be performed on
        :type string: str
        :param match_case: flag to consider case differences in filtering
        :type match_case: bool
        """
        if type(string) is not str:
            raise TypeError('Initial input string for StringFilter object must be str type')
        if type(match_case) is not bool:
            raise TypeError('match_case input for StringFilter object must be bool type')

        self._match_case = match_case
        self._string = string

    def case(self, string):
        """
        Returns the given string in all lower case if letter case is not
        to be considered in filtering, else returns the original string
        :param string: the string to have it case (potentially) modified
        :type string: str
        :return: the string with (potentially) modified case
        :rtype: str
        """
        if self._match_case and type(string) in [str, tuple]:
            return string
        if not self._match_case and type(string) is tuple:
            return tuple(s.lower() for s in string)
        elif not self._match_case and type(string) is str:
            return string.lower()
        else:
            raise TypeError('invalid input string type')

    def contains(self, substring):
        """
        Returns True if the string contains substring or any of a tuple
        of substrings, False else
        :param substring: the substring(s) to check for in the string
        :type substring: str or tuple(str)
        :return: filter result
        :rtype: bool
        """
        if type(substring) is str:
            return self.case(substring) in self.string
        elif type(substring) is tuple:
            return any(self.case(s) in self.string for s in substring)
        else:
            raise TypeError('invalid input substring type')

    def endswith(self, substring):
        """
        Returns true if the string ends with the substring or any of a
        tuple of substrings, False else
        :param substring: the substring to check
        :type substring: str or tuple(str)
        :return: filter results
        :rtype: bool
        """
        if type(substring) in [str, tuple]:
            return self.string.endswith(self.case(substring))
        else:
            raise TypeError('invaild input substring type')

    def equals(self, string):
        """
        Returns true if the filter string equals the given string or any of
        a tuple of strings, False else
        :param string: the string to compare to
        :type string: str or tuple(str)
        :return: filter results
        :rtype: bool
        """
        if type(string) is str:
            return self.string == self.case(string)
        elif type(string) is tuple:
            return any(self.case(s) == self.string for s in string)
        else:
            raise TypeError('invalid input string type')

    def startswith(self, substring):
        """
        Returns true if the filter string starts with the substring or any
        of a tuple of substrings, False else
        :param substring: the substring to check
        :type substring: str or tuple(str)
        :return: filter results
        :rtype: bool
        """
        if type(substring) in [str, tuple]:
            return self.string.startswith(self.case(substring))
        else:
            raise TypeError('invalid input substring type')

    @property
    def string(self):
        """
        :return: the StringFilter object's string to be filtered
        :rtype: str
        """
        return self.case(self._string)

