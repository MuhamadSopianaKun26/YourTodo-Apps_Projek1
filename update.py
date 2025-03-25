from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate
from create import TaskDialog


class TodoUpdater:
    @staticmethod
    def update_task_table_item(table_widget, row, task_data):
        for col, key in enumerate(
            ["name", "description", "start_time", "deadline", "priority", "status"]
        ):
            item = QTableWidgetItem(task_data[key])
            table_widget.setItem(row, col, item)

    @staticmethod
    def update_task(table_widget, save_callback):
        from read import TodoReader

        selected = table_widget.currentRow()
        if selected >= 0:
            task_data = TodoReader.get_selected_task_data(table_widget)
            dialog = TaskDialog(table_widget.parent(), task_data)
            if dialog.exec_():
                task_data = dialog.getTaskData()
                TodoUpdater.update_task_table_item(table_widget, selected, task_data)
                save_callback()

    @staticmethod
    def mark_task_as_done(table_widget, save_callback):
        from read import TodoReader

        selected = table_widget.currentRow()
        if selected >= 0:
            task_data = TodoReader.get_selected_task_data(table_widget)
            current_date = QDate.currentDate().toString("yyyy-MM-dd")
            task_data["status"] = f"done ✅ - Completed on {current_date}"
            TodoUpdater.update_task_table_item(table_widget, selected, task_data)
            save_callback()

    @staticmethod
    def mark_task_as_failed(table_widget, row, save_callback):
        from read import TodoReader

        selected = row if row is not None else table_widget.currentRow()
        if selected >= 0:
            task_data = TodoReader.get_selected_task_data(table_widget)
            task_data["status"] = "failed ❌"
            TodoUpdater.update_task_table_item(table_widget, selected, task_data)
            save_callback()

    @staticmethod
    def move_task_to_history(table_widget, save_callback):
        from read import TodoReader

        selected = table_widget.currentRow()
        if selected >= 0:
            task_data = TodoReader.get_selected_task_data(table_widget)
            if task_data["status"] == "due":
                QMessageBox.warning(
                    table_widget.parent(),
                    "Cannot Move Task",
                    "Task cannot be moved to history while its status is still 'due'",
                )
                return

            try:
                with open("history.txt", "a", encoding="utf-8") as file:
                    data = [
                        task_data[key]
                        for key in [
                            "name",
                            "description",
                            "start_time",
                            "deadline",
                            "priority",
                            "status",
                        ]
                    ]
                    file.write(" | ".join(data) + "\n")

                table_widget.removeRow(selected)
                save_callback()
                QMessageBox.information(
                    table_widget.parent(),
                    "Success",
                    "Task has been moved to history successfully!",
                )
            except Exception as e:
                QMessageBox.critical(
                    table_widget.parent(), "Error", f"Error moving task to history: {e}"
                )
