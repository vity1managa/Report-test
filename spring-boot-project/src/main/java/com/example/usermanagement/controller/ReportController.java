package com.example.usermanagement.controller;

import com.example.usermanagement.service.ReportService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.Map;

@RestController
@RequestMapping("/api/reports")
@CrossOrigin(origins = "*")
public class ReportController {

    @Autowired
    private ReportService reportService;

    @GetMapping("/user-report")
    public ResponseEntity<Map<String, Object>> generateUserReport() {
        Map<String, Object> report = reportService.generateUserReport();
        return ResponseEntity.ok(report);
    }
}