"""Административная панель SQLAdmin."""

from sqladmin import Admin

from app.db.session import engine
from app.admin.activity import ActivityAdmin
from app.admin.building import BuildingAdmin
from app.admin.organization import OrganizationAdmin, OrganizationPhoneAdmin


def setup_admin(app) -> Admin:
    """Настраивает и возвращает админку."""
    admin = Admin(
        app,
        engine,
        title="OrgAtlas Admin",
        base_url="/admin",
    )

    admin.add_view(BuildingAdmin)
    admin.add_view(ActivityAdmin)
    admin.add_view(OrganizationAdmin)
    admin.add_view(OrganizationPhoneAdmin)

    return admin
