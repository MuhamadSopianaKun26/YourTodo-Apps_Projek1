from PyQt5.QtWidgets import QMessageBox


class TodoDeleter:
    """Static class for handling task deletion operations"""

    @staticmethod
    def delete_task(table_widget, save_callback):
        """Delete a single selected task after confirmation"""
        selected = table_widget.currentRow()
        if selected >= 0:
            reply = QMessageBox.question(
                table_widget.parent(),
                "Delete Task",
                "Are you sure you want to delete this task?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                table_widget.removeRow(selected)
                save_callback()

    @staticmethod
    def clear_all_tasks(table_widget, save_callback):
        """Clear all tasks after confirmation"""
        reply = QMessageBox.question(
            table_widget.parent(),
            "Clear All Tasks",
            "Are you sure you want to clear all tasks?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            table_widget.setRowCount(0)
            save_callback()
