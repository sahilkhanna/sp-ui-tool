if __name__ == "__main__" and __package__ is None:
    import sys
    import pathlib
    sys.path.append(str(pathlib.Path(__file__).parent.parent.resolve()))

    __package__ = "project"

from project import Project


def main():
    p = Project()
    p.main()


if __name__ == "__main__":
    main()
