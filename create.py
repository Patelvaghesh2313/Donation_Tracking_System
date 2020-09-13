
from models import *


db.init_app(app)


def main():
    db.create_all()


if __name__ == '__main__':
    main()
