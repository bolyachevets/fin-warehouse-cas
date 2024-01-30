import os
import re
import sys
from datetime import datetime, timedelta

regex = r"\d{4}-\d{2}-\d{2}"


def get_previous_business_day():
    today = datetime.today()
    one_day = timedelta(days=1)
    previous_day = today - one_day
    while previous_day.weekday() >= 5:
        previous_day -= one_day
    return previous_day.strftime("%Y-%m-%d")


def patch_config(file):
    host = open(file, "r")
    try:
        with open('./temp.conf', "w") as out:
            for line in host:
                if line.startswith('WHERE '):
                    print('Replacing: \n')
                    print(line)
                    result = re.sub(regex, new_date, line)
                    print('with: \n')
                    print(result)
                    out.write(result)
                else:
                    out.write(line)
    finally:
        host.close()
        os.rename('./temp.conf', file)


if __name__ == '__main__':
    num_args = len(sys.argv)

    if num_args == 2:
        config_file = sys.argv[1]
        new_date = get_previous_business_day()
        print('patching ora2pg config...')
        patch_config(config_file)
        print('patched...')
    else:
        print('the script takes 1 argument - path to ora2pg.conf config file')
