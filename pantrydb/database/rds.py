# RDS database implementation for pantrydb
from typing import List

from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from pantrydb.database.abstract import PantryDatabase
from pantrydb.items import PantryItem

# DATABASE_URL_ENV = "DATABASE_URL"


# TODO hook up to RDS
# TODO auth
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
Session = sessionmaker(engine)


# TODO better logging
# TODO make async ?
class Base(DeclarativeBase): ...


class DBPantryItem(Base):
    __tablename__ = "pantry_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO is 30 the best here?
    name: Mapped[str] = mapped_column(String(30))
    amount: Mapped[int]

    def __repr__(self) -> str:
        return (
            f"PantryItem(id={self.id!r}, name={self.name!r}, amount={self.amount!r})"
        )

    @classmethod
    def from_pantry_item(cls, item: PantryItem) -> "DBPantryItem":
        return cls(name=item.name, amount=item.amount)

    def to_pantry_item(self) -> PantryItem:
        return PantryItem(name=self.name, amount=self.amount)


class RDSPantryDatabase(PantryDatabase):
    """RDS implementation of the Database abstract class using SQLAlchemy and databases (asyncpg driver)."""

    @classmethod
    def from_env_vars(cls) -> "RDSPantryDatabase":
        """Create a RDSPantryDatabase instance from environment variables."""
        return cls()

    def __init__(self):
        # TODO do with alembic instead
        Base.metadata.create_all(engine)

    def list_items(self) -> List[PantryItem]:
        with Session() as session:
            try:
                stmt = select(DBPantryItem)
                results = session.execute(stmt).scalars().all()
                return [db_pantry_item.to_pantry_item() for db_pantry_item in results]
            except Exception:
                return []

    def add_item(self, item: PantryItem) -> bool:
        with Session.begin() as session:
            try:
                stmt = select(DBPantryItem).where(DBPantryItem.name == item.name)
                result = session.execute(stmt).scalar_one_or_none()
                if result:
                    result.amount += item.amount
                    session.add(result)
                else:
                    new_item = DBPantryItem.from_pantry_item(item)
                    session.add(new_item)
                return True
            except Exception:
                return False

    def remove_item(self, item: PantryItem) -> bool:
        with Session.begin() as session:
            try:
                stmt = select(DBPantryItem).where(DBPantryItem.name == item.name)
                result = session.execute(stmt).scalar_one_or_none()
                if not result:
                    return False
                result.amount -= item.amount
                if result.amount <= 0:
                    session.delete(result)
                else:
                    session.add(result)
                return True
            except Exception:
                return False
