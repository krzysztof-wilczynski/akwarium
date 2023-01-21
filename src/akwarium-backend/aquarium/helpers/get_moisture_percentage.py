def get_moisture_percentage(value):
    result = round((value - 320) / 6.96, 2)
    if result < 0:
        result = 0
    return result
