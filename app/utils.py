from passlib.context import CryptContext
import datetime

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash_password(password: str):
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def convert_time(past_time):
    past_day = past_time.day
    total_past_seconds = past_time.second + \
        (past_time.minute * 60) + ((past_time.hour * 60) * 60)

    time_now = datetime.datetime.now()
    time_now_day = time_now.day
    diff_day = time_now_day - past_day

    time_now_total_seconds = time_now.second + \
        (time_now.minute * 60) + ((time_now.hour * 60) * 60) + \
        (diff_day * 24 * 60 * 60)
    diff_time = round((time_now_total_seconds - total_past_seconds) / 60)
    return diff_time
