package com.example.firsttrytest;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TaskServiceTest {
    @Test
    public void testCreateTask() {
        TaskService taskService = new TaskService();
        Task task = taskService.createTask("Test Task", "Test Description");

        assertNotNull(task.getId());
        assertEquals("Test Task", task.getTitle());
        assertEquals("Test Description", task.getDescription());
        assertFalse(task.isCompleted());
    }

    @Test
    public void testCompleteTask() {
        TaskService taskService = new TaskService();
        Task task = taskService.createTask("Test Task", "Test Description");

        Task completedTask = taskService.completeTask(task.getId()).orElse(null);
        assertNotNull(completedTask);
        assertTrue(completedTask.isCompleted());
    }

}
