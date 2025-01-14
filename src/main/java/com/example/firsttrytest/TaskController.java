package com.example.firsttrytest;

import java.util.List;

public class TaskController {
    private TaskService taskService;

    public TaskController() {
        this.taskService = new TaskService();
    }

    public Task createTask(String title, String description) {
        return taskService.createTask(title, description);
    }

    public List<Task> getAllTasks() {
        return taskService.listTasks();
    }

    public Task completeTask(Long taskId) {
        return taskService.completeTask(taskId).orElse(null);
    }

}
