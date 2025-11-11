from app.db.session import Base, engine


def init_db() -> None:
	"""Create all tables (development helper). Use Alembic for real migrations."""
	Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
	init_db()
	print("Database initialized")

