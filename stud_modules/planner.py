# stud_modules/planner.py

from datetime import datetime, timedelta, date

def create_plan(subject, exam_date_obj, study_hours_per_day):
    """
    Creates a study plan dictionary based on the exam date and hours per day.

    Args:
        subject (str): Subject name.
        exam_date_obj (datetime.date): Exam date as a date object.
        study_hours_per_day (int): Number of hours to study per day.

    Returns:
        dict or str: Study plan dictionary or error message.
    """
    try:
        if not isinstance(exam_date_obj, date):
            return "⚠️ Invalid exam date format."

        today = datetime.today().date()
        remaining_days = (exam_date_obj - today).days

        if remaining_days <= 0:
            return f"❌ The exam date for '{subject}' has already passed or is today."

        total_study_hours = remaining_days * study_hours_per_day

        plan = {
            "subject": subject,
            "exam_date": exam_date_obj.strftime("%Y-%m-%d"),
            "start_date": today.strftime("%Y-%m-%d"),
            "remaining_days": remaining_days,
            "daily_study_hours": study_hours_per_day,
            "total_study_hours": total_study_hours,
            "message": f"📚 You need to study {study_hours_per_day} hours daily for {remaining_days} days to prepare for '{subject}' exam on {exam_date_obj.strftime('%Y-%m-%d')}."
        }

        return plan

    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"
