import dataclasses
import json

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column

# oonce for every database.
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


# simple using,
with Session(engine) as session:
    result = session.execute(text("select 'hello world'"))
    print(result.all())


# once for every group (some gropped tables).
class Base(DeclarativeBase):
    pass


# class Purchase(Base):
#     __tablename__ = "purchase"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str]
#     count: Mapped[int]
#     is_active: Mapped[bool]

#     def __repr__(self) -> str:
#         return f"Purchase(id={self.id!r}, name={self.name!r}, count={self.count!r}, is_active={self.is_active!r})"


# from sqlalchemy import Table
# some_table = Table("some_table", Base.metadata, autoload_with=engine)
# print(some_table)

@dataclasses.dataclass
class Purchase:
    name: str
    count: int
    is_active: bool

    def __init__(self, name: str, count: int, is_active: bool) -> None:
        self.name = name
        self.count = count
        self.is_active = is_active


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class NoChangesException(Exception):
    ...


class NotExistException(Exception):
    ...


data: dict[str, Purchase] = {}


def get_purchases() -> list[Purchase]:
    return list(data.values())


def get_purchases_json() -> str:
    data = get_purchases()
    return json.dumps(data, cls=EnhancedJSONEncoder)


def set_purchases(purchases: list[Purchase]) -> None:
    global data
    data = {item.name: item for item in purchases}


def set_purchase_json(purchases_json: str) -> None:
    purchases: list[Purchase] = json.loads(purchases_json)  # TODO: is `, cls=purchase.EnhancedJSONEncoder` need?; use to correct https://stackoverflow.com/questions/51286748/make-the-python-json-encoder-support-pythons-new-dataclasses
    set_purchases(purchases)


def add_purchase(purchase_name: str) -> None:
    purchase: Purchase | None = data.get(purchase_name)
    if purchase is not None and purchase.is_active:
        raise NoChangesException()

    if purchase is None:
        purchase = Purchase(purchase_name, 0, False)
        data[purchase_name] = purchase

    purchase.is_active = True


def buy_purchase(purchase_name: str) -> None:
    purchase: Purchase | None = data.get(purchase_name)
    if purchase is None:
        raise NotExistException()

    if not purchase.is_active:
        raise NoChangesException()

    purchase.count += 1
    purchase.is_active = False


def cancel_purchase(purchase_name: str) -> None:
    purchase: Purchase | None = data.get(purchase_name)
    if purchase is None:
        raise NotExistException()

    if not purchase.is_active:
        raise NoChangesException()

    purchase.is_active = False
