package com.example.usermanagement.service;

import com.example.usermanagement.entity.Task;
import com.example.usermanagement.entity.TaskStatus;
import com.example.usermanagement.entity.User;
import com.example.usermanagement.repository.TaskRepository;
import com.example.usermanagement.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class ReportService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private TaskRepository taskRepository;

    public Map<String, Object> generateUserReport() {
        Map<String, Object> report = new HashMap<>();
        
        // Total users count
        long totalUsers = userRepository.count();
        report.put("total_users", totalUsers);
        
        // Total tasks count
        long totalTasks = taskRepository.count();
        report.put("total_tasks", totalTasks);
        
        // Users with their task counts
        List<User> allUsers = userRepository.findAll();
        Map<String, Object> userStats = new HashMap<>();
        
        for (User user : allUsers) {
            Map<String, Object> userData = new HashMap<>();
            
            // Count tasks per status for this user
            List<Task> userTasks = taskRepository.findByUserId(user.getId());
            int pendingCount = 0;
            int inProgressCount = 0;
            int completedCount = 0;
            
            for (Task task : userTasks) {
                switch (task.getStatus()) {
                    case PENDING:
                        pendingCount++;
                        break;
                    case IN_PROGRESS:
                        inProgressCount++;
                        break;
                    case COMPLETED:
                        completedCount++;
                        break;
                }
            }
            
            userData.put("total_tasks", userTasks.size());
            userData.put("pending_tasks", pendingCount);
            userData.put("in_progress_tasks", inProgressCount);
            userData.put("completed_tasks", completedCount);
            userData.put("email", user.getEmail());
            userData.put("full_name", user.getFirstName() + " " + user.getLastName());
            
            userStats.put(user.getUsername(), userData);
        }
        
        report.put("user_statistics", userStats);
        
        // Overall task status distribution
        Map<String, Long> taskStatusDistribution = new HashMap<>();
        taskStatusDistribution.put("PENDING", taskRepository.findByStatus(TaskStatus.PENDING).size());
        taskStatusDistribution.put("IN_PROGRESS", taskRepository.findByStatus(TaskStatus.IN_PROGRESS).size());
        taskStatusDistribution.put("COMPLETED", taskRepository.findByStatus(TaskStatus.COMPLETED).size());
        
        report.put("task_status_distribution", taskStatusDistribution);
        
        return report;
    }
}