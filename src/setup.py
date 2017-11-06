from db import build_db
from btree import BTree
import pickle

if __name__ == "__main__":
    pickle.dump( build_db(BTree(15)), open("Courses.db", "w"), -1)
