import sys


def progress_bar(current, total, title_of_process, barLength=20):
    percent = float(current) * 100 / total
    arrow = '-' * int(percent / 100 * barLength - 1) + '>'
    spaces = ' ' * (barLength - len(arrow))
    sys.stdout.flush()
    sys.stdout.write('\r%s is in progress: [%s%s] %f %%' % (title_of_process, arrow, spaces, percent))
    sys.stdout.flush()
