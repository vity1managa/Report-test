import json
import csv
from datetime import datetime
from user_queries import UserDatabaseManager
from typing import List, Dict


class ReportGenerator:
    def __init__(self):
        self.db_manager = UserDatabaseManager()
    
    def generate_user_summary_report(self) -> Dict:
        """Generate a summary report of all users"""
        users = self.db_manager.get_all_users()
        total_users = len(users)
        
        # Count tasks per status
        task_status_counts = {'pending': 0, 'in_progress': 0, 'completed': 0}
        total_tasks = 0
        
        for user in users:
            user_tasks = self.db_manager.get_user_tasks(user['id'])
            for task in user_tasks:
                status = task['status']
                if status in task_status_counts:
                    task_status_counts[status] += 1
                total_tasks += 1
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_users': total_users,
                'total_tasks': total_tasks,
                'task_status_breakdown': task_status_counts
            },
            'users': users
        }
        
        return report
    
    def generate_user_task_report(self) -> List[Dict]:
        """Generate a detailed report of users with their tasks"""
        all_users_with_tasks = self.db_manager.get_all_users_with_tasks()
        
        report = []
        for user in all_users_with_tasks:
            user_report = {
                'user_info': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'full_name': user['full_name'],
                    'created_at': str(user['created_at'])
                },
                'tasks': [
                    {
                        'id': task['id'],
                        'title': task['title'],
                        'description': task['description'],
                        'status': task['status'],
                        'created_at': str(task['created_at'])
                    } for task in user['tasks']
                ],
                'task_count': len(user['tasks']),
                'completed_tasks': len([t for t in user['tasks'] if t['status'] == 'completed']),
                'pending_tasks': len([t for t in user['tasks'] if t['status'] == 'pending']),
                'in_progress_tasks': len([t for t in user['tasks'] if t['status'] == 'in_progress'])
            }
            report.append(user_report)
        
        return report
    
    def export_to_json(self, data: Dict, filename: str):
        """Export report data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Report exported to {filename}")
    
    def export_to_csv(self, data: List[Dict], filename: str):
        """Export user-task data to CSV file"""
        if not data:
            print("No data to export")
            return
        
        fieldnames = ['user_id', 'username', 'email', 'full_name', 'task_id', 'task_title', 'task_description', 'task_status', 'task_created_at']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for user_report in data:
                user_info = user_report['user_info']
                if user_report['tasks']:
                    for task in user_report['tasks']:
                        writer.writerow({
                            'user_id': user_info['id'],
                            'username': user_info['username'],
                            'email': user_info['email'],
                            'full_name': user_info['full_name'],
                            'task_id': task['id'],
                            'task_title': task['title'],
                            'task_description': task['description'],
                            'task_status': task['status'],
                            'task_created_at': task['created_at']
                        })
                else:
                    # Write user even if they have no tasks
                    writer.writerow({
                        'user_id': user_info['id'],
                        'username': user_info['username'],
                        'email': user_info['email'],
                        'full_name': user_info['full_name'],
                        'task_id': '',
                        'task_title': '',
                        'task_description': '',
                        'task_status': '',
                        'task_created_at': ''
                    })
        
        print(f"Report exported to {filename}")


def main():
    print("Generating project reports...")
    
    generator = ReportGenerator()
    
    # Generate summary report
    summary_report = generator.generate_user_summary_report()
    generator.export_to_json(summary_report, '/workspace/project_report/reports/user_summary_report.json')
    
    # Generate detailed user-task report
    detailed_report = generator.generate_user_task_report()
    generator.export_to_json(detailed_report, '/workspace/project_report/reports/user_task_report.json')
    generator.export_to_csv(detailed_report, '/workspace/project_report/reports/user_task_report.csv')
    
    print("\n=== Summary Report ===")
    print(f"Generated at: {summary_report['generated_at']}")
    print(f"Total Users: {summary_report['summary']['total_users']}")
    print(f"Total Tasks: {summary_report['summary']['total_tasks']}")
    print("Task Status Breakdown:")
    for status, count in summary_report['summary']['task_status_breakdown'].items():
        print(f"  {status}: {count}")
    
    print(f"\nDetailed reports saved to /workspace/project_report/reports/")
    print("- user_summary_report.json")
    print("- user_task_report.json") 
    print("- user_task_report.csv")


if __name__ == "__main__":
    main()