from sqladmin import ModelView

from app.models.organization import Organization, OrganizationPhone


class OrganizationAdmin(ModelView, model=Organization):
    """Админка для организаций."""

    name = "Организация"
    name_plural = "Организации"
    icon = "fa-solid fa-briefcase"

    column_list = [Organization.id, Organization.name, Organization.building_id]
    column_searchable_list = [Organization.name]
    column_sortable_list = [Organization.id, Organization.name]
    column_default_sort = [(Organization.id, False)]

    column_labels = {
        Organization.id: "ID",
        Organization.name: "Название",
        Organization.building_id: "ID здания",
        Organization.building: "Здание",
        Organization.phones: "Телефоны",
        Organization.activities: "Виды деятельности",
    }


class OrganizationPhoneAdmin(ModelView, model=OrganizationPhone):
    """Админка для телефонов организаций."""

    name = "Телефон"
    name_plural = "Телефоны"
    icon = "fa-solid fa-phone"

    column_list = [OrganizationPhone.id, OrganizationPhone.phone, OrganizationPhone.organization_id]
    column_searchable_list = [OrganizationPhone.phone]
    column_sortable_list = [OrganizationPhone.id, OrganizationPhone.phone]
    column_default_sort = [(OrganizationPhone.id, False)]

    column_labels = {
        OrganizationPhone.id: "ID",
        OrganizationPhone.phone: "Номер телефона",
        OrganizationPhone.organization_id: "ID организации",
        OrganizationPhone.organization: "Организация",
    }
