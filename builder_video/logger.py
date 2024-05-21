from datetime import datetime

def write_log(log_type, object_name, log_message):
    log_path = "data/log/db_{}_{}_{}.log".format(datetime.now().year, datetime.now().month, datetime.now().day)
    log_message = "[{}][{}][{}] - {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f"), object_name, log_type, log_message)
    with open(log_path, "a") as file:
        file.write(log_message + "\n")

def info_log(object_name, message):
    write_log("info", object_name, message)

def error_log(object_name, message):
    write_log("error", object_name, message)
