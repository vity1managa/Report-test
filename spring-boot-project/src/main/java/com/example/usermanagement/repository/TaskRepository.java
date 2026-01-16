package com.example.usermanagement.repository;

import com.example.usermanagement.entity.Task;
import com.example.usermanagement.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {
    List<Task> findByUserId(Long userId);
    List<Task> findByUserUsername(String username);
    List<Task> findByStatus(com.example.usermanagement.entity.TaskStatus status);
}