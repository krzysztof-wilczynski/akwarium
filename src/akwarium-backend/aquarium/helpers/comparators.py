def compare(a, comparator, b):
    """Compare two values accordingly to comparator character passed.

        Parameters:
            a (float): First value to be compared
            comparator (str): Comparator (>, >=, <, or <=)
            b (float): Second value to be compared

        Returns:
            bool: Boolean
    """

    if comparator == ">":
        return a > b
    elif comparator == ">=":
        return a >= b
    elif comparator == "<":
        return a < b
    elif comparator == "<=":
        return a <= b
    else:
        raise Exception("Nieprawidłowy komparator")
