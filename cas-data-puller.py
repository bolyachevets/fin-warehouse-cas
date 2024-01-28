#  Author: Andriy.Bolyachevets@gov.bc.ca
#  Date: 2024-01-25
# run:
# cat cas-data-puller.py | ssh nettle.bcgov python - ora2pg/ora2pg.conf
import sys
import subprocess


def main():
    num_args = len(sys.argv)

    if num_args == 2:
        config = sys.argv[1]
        run_ora2pg(config)
    else:
        print('the script takes 1 argument - path to ora2pg.conf config files')


def run_ora2pg(config_file):
    print('Running ora2pg with ' + config_file)
    timeout = 'OCIServerAttach'
    session = 'OCISessionBegin'

    repeat = 0
    while True:
        try:
            print('---')
            print(repeat)
            print('---')
            ret = subprocess.run(['/usr/perl5/5.36/bin/ora2pg', '--basedir', '/dsk01/warehouse', '-c', config_file], capture_output=True, text=True)
            print(ret.stdout)
            if timeout not in ret.stdout and session not in ret.stdout:
                break
        except Exception as e:
            print('retrying data pull with' + config_file)
            print(e)
        finally:
            repeat += 1
            if repeat > 2:
                break


if __name__ == '__main__':
    main()
