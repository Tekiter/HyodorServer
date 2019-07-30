import argparse

from server import create_app, db
from server.model import User, UserAddi

app = create_app()
app.app_context().push()
db.init_app(app=create_app())


parser = argparse.ArgumentParser()

parser.add_argument("--makedb", action="store_true")

args = parser.parse_args()

if args.makedb:
    db.create_all()
else:
    print("Nothing Happened.")



