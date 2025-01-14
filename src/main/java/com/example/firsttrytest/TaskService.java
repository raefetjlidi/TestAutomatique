package com.example.firsttrytest;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class TaskService {
    private List<Task> tasks = new ArrayList<>();
        private Long idCounter = 1L;

        public Task createTask(String title, String description) {
            Task task = new Task();
            task.setId(idCounter++);
            task.setTitle(title);
            task.setDescription(description);
            task.setCompleted(false);
            tasks.add(task);
            return task;
        }

        public List<Task> listTasks() {
            return tasks;
        }

        public Optional<Task> completeTask(Long taskId) {
            return tasks.stream()
                    .filter(task -> task.getId().equals(taskId))
                    .findFirst()
                    .map(task -> {
                        task.setCompleted(true);
                        return task;
                    });
        }
    }