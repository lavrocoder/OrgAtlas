from sqladmin import ModelView

from app.models.building import Building


class BuildingAdmin(ModelView, model=Building):
    """Админка для зданий."""

    name = "Здание"
    name_plural = "Здания"
    icon = "fa-solid fa-building"

    column_list = [Building.id, Building.address, Building.latitude, Building.longitude]
    column_searchable_list = [Building.address]
    column_sortable_list = [Building.id, Building.address]
    column_default_sort = [(Building.id, False)]

    column_labels = {
        Building.id: "ID",
        Building.address: "Адрес",
        Building.latitude: "Широта",
        Building.longitude: "Долгота",
        Building.organizations: "Организации",
    }
