from fetch import *
from sql import *

if __name__ == "__main__":
    for i in get_x():
        h=get_html(i)
        insert_xpost(i,h)
