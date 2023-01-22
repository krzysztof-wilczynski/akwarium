def get_moisture_percentage(value):
    result = round((value - 200) / 18, 2)
    if result < 0:
        result = 0
    return result
