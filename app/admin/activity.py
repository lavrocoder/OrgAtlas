from sqladmin import ModelView

from app.models.activity import Activity


class ActivityAdmin(ModelView, model=Activity):
    """Админка для видов деятельности."""

    name = "Вид деятельности"
    name_plural = "Виды деятельности"
    icon = "fa-solid fa-tags"

    column_list = [Activity.id, Activity.name, Activity.parent_id, Activity.level]
    column_searchable_list = [Activity.name]
    column_sortable_list = [Activity.id, Activity.name, Activity.level]
    column_default_sort = [(Activity.level, False), (Activity.id, False)]

    column_labels = {
        Activity.id: "ID",
        Activity.name: "Название",
        Activity.parent_id: "Родитель",
        Activity.level: "Уровень",
        Activity.parent: "Родительская деятельность",
        Activity.children: "Дочерние",
    }
