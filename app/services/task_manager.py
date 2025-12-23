import json
from pathlib import Path
from typing import List

from app.models.task_model import task


class task_manager:
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    data_file: Path = base_dir / "data" / "tasks_json.json"
    tasks_key: str = "Tasks"
    last_id_key: str = "last_id"

    @staticmethod
    def _ensure_data_file_exists() -> None:
        task_manager.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not task_manager.data_file.exists():
            initial_content = {
                task_manager.tasks_key: [],
                task_manager.last_id_key: 0,
            }
            with task_manager.data_file.open("w", encoding="utf-8") as file:
                json.dump(initial_content, file, ensure_ascii=False, indent=2)

    @staticmethod
    def load_tasks() -> List[task]:
        task_manager._ensure_data_file_exists()
        with task_manager.data_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
        tasks_data = data.get(task_manager.tasks_key, [])
        return [task.from_dict(t) for t in tasks_data]

    @staticmethod
    def save_tasks(tasks: List[task]) -> None:
        task_manager._ensure_data_file_exists()
        with task_manager.data_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
        data[task_manager.tasks_key] = [t.to_dict() for t in tasks]
        with task_manager.data_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def _get_next_id() -> int:
        task_manager._ensure_data_file_exists()
        with task_manager.data_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
        last_id = int(data.get(task_manager.last_id_key, 0))
        next_id = last_id + 1
        data[task_manager.last_id_key] = next_id
        with task_manager.data_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return next_id

    @staticmethod
    def create_task(new_task: task) -> task:
        tasks = task_manager.load_tasks()
        new_id = task_manager._get_next_id()
        new_task.id = new_id
        tasks.append(new_task)
        task_manager.save_tasks(tasks)
        return new_task

    @staticmethod
    def get_all_tasks() -> List[task]:
        return task_manager.load_tasks()

    @staticmethod
    def get_task_by_id(task_id: int) -> task | None:
        tasks = task_manager.load_tasks()
        for existing_task in tasks:
            if existing_task.id == task_id:
                return existing_task
        return None

    @staticmethod
    def update_task(task_id: int, updated_task: task) -> task | None:
        tasks = task_manager.load_tasks()
        for index, existing_task in enumerate(tasks):
            if existing_task.id == task_id:
                updated_task.id = task_id
                tasks[index] = updated_task
                task_manager.save_tasks(tasks)
                return updated_task
        return None

    @staticmethod
    def delete_task(task_id: int) -> bool:
        tasks = task_manager.load_tasks()
        filtered_tasks = [t for t in tasks if t.id != task_id]
        if len(filtered_tasks) == len(tasks):
            return False
        task_manager.save_tasks(filtered_tasks)
        return True



