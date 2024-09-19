from datetime import datetime


def convert_date(date_str):
    date_obj = datetime.strptime(date_str, '%y%m%d')
    formatted_date = date_obj.strftime('%Y-%m-%d')
    return formatted_date


def convert_date_format(date_string):
    input_format = "%d %b, %Y"
    output_format = "%Y-%m-%d"
    try:
        date_obj = datetime.strptime(date_string, input_format)
        formatted_date = date_obj.strftime(output_format)
        return formatted_date
    except ValueError as e:
        print(f"Error: Incorrect date string format provided. {e}")
        return None


def convert_datetime_format(date_string):
    input_format = "%d %b, %Y"
    output_format = "%Y-%m-%d"
    try:
        date_obj = datetime.strptime(date_string, input_format)
        formatted_date = date_obj.strftime(output_format)
        current_time = datetime.now().strftime("%H:%M:%S")

        formatted_datetime = f"{formatted_date} {current_time}"
        return formatted_datetime
    except ValueError as e:
        print(f"Error: Incorrect date string format provided. {e}")
        return None
