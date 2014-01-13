from alembic import context
from art17.models import db, alembic_ignore_tables


def include_object(obj, name, type_, reflected, compare_to):
    if type_ == 'table' and name in alembic_ignore_tables:
        return False

    return True


context.configure(
    connection=db.session.connection(),
    target_metadata=db.metadata,
    include_object=include_object,
)

context.run_migrations()

if not context.is_offline_mode():
    db.session.commit()
