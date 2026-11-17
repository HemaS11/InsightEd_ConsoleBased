
import requests
import csv

API = "http://127.0.0.1:8000"


def get_data(endpoint):
    response = requests.get(f"{API}{endpoint}")
    response.raise_for_status()
    return response.json()


def submit_feedback():
    print("\n--- SUBMIT COURSE FEEDBACK ---")

    course = input("Course name: ").strip()
    instructor = input("Instructor name: ").strip()

    try:
        rating = float(input("Rating (1-5): "))
        if not 1 <= rating <= 5:
            print("Rating must be between 1 and 5.")
            return
    except ValueError:
        print("Please enter a valid rating.")
        return

    comment = input("Feedback comment: ").strip()

    if not course or not instructor or not comment:
        print("All fields are required.")
        return

    data = {
        "course_name": course,
        "instructor_name": instructor,
        "rating": rating,
        "comment": comment
    }

    response = requests.post(f"{API}/feedback", json=data)

    if response.ok:
        print("\nFeedback submitted successfully!")
    else:
        print("Error:", response.text)


def view_feedback():
    feedback = get_data("/feedback")

    print("\n--- ALL FEEDBACK ---")

    if not feedback:
        print("No feedback available.")
        return

    for item in feedback:
        print("-" * 40)
        print("Course:", item["course_name"])
        print("Instructor:", item["instructor_name"])
        print("Rating:", item["rating"])
        print("Sentiment:", item.get("sentiment"))
        print("Comment:", item["comment"])


def dashboard():
    data = get_data("/analytics")

    print("\n--- DASHBOARD ANALYTICS ---")
    print("Total feedback:", data.get("total_feedback", 0))
    print("Average rating:", data.get("average_rating", 0))
    print("Positive:", data.get("positive_feedback", 0))
    print("Negative:", data.get("negative_feedback", 0))
    print("Neutral:", data.get("neutral_feedback", 0))


def course_analytics():
    data = get_data("/analytics/courses")

    print("\n--- COURSE ANALYTICS ---")

    for item in data:
        print("-" * 40)
        print("Course:", item["course_name"])
        print("Instructor:", item["instructor_name"])
        print("Feedback count:", item["total_feedback"])
        print("Average rating:", item["average_rating"])


def sentiment_analysis():
    data = get_data("/analytics/sentiment")

    print("\n--- SENTIMENT ANALYSIS ---")

    for item in data:
        print(
            item["course_name"],
            "|", item["instructor_name"],
            "| Positive:", item["positive"],
            "| Negative:", item["negative"],
            "| Neutral:", item["neutral"]
        )


def topic_insights():
    feedback = get_data("/feedback")

    topics = {
        "Teaching Quality": ["teach", "explain", "instructor"],
        "Course Content": ["content", "syllabus", "topic"],
        "Practical Learning": ["practical", "lab", "project"],
        "Course Pace": ["pace", "fast", "slow"],
        "Learning Resources": ["notes", "material", "resource"]
    }

    print("\n--- TOPIC INSIGHTS ---")

    for topic, keywords in topics.items():
        matches = [
            item["comment"] for item in feedback
            if any(word in item["comment"].lower() for word in keywords)
        ]

        if matches:
            print(f"\n{topic}: {len(matches)} matching comments")
            for comment in matches:
                print("-", comment)


def recommendations():
    data = get_data("/analytics/courses")

    print("\n--- RECOMMENDATIONS ---")

    if not data:
        print("No course data available.")
        return

    for item in data:
        rating = float(item["average_rating"])

        print("\nCourse:", item["course_name"])
        print("Instructor:", item["instructor_name"])
        print("Average rating:", rating)

        if rating < 3:
            print("Suggestion: Review teaching methods and collect detailed feedback.")
        elif rating < 4:
            print("Suggestion: Identify areas that need improvement.")
        else:
            print("Suggestion: Maintain the current teaching approach.")


def export_csv():
    feedback = get_data("/feedback")

    if not feedback:
        print("No feedback available to export.")
        return

    fields = [
        "id", "course_name", "instructor_name",
        "rating", "sentiment", "comment", "created_at"
    ]

    with open("feedback_report.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for item in feedback:
            writer.writerow({
                field: item.get(field, "") for field in fields
            })

    print("CSV report saved as feedback_report.csv")


def main():
    while True:
        print("\n" + "=" * 45)
        print("              INSIGHTED")
        print("     Academic Feedback Intelligence")
        print("=" * 45)

        print("1. Submit Course Feedback")
        print("2. View All Feedback")
        print("3. Dashboard Analytics")
        print("4. Course Analytics")
        print("5. Sentiment Analysis")
        print("6. Topic Insights")
        print("7. Recommendations")
        print("8. Generate CSV Report")
        print("9. Exit")

        choice = input("\nEnter your choice: ")

        try:
            if choice == "1":
                submit_feedback()
            elif choice == "2":
                view_feedback()
            elif choice == "3":
                dashboard()
            elif choice == "4":
                course_analytics()
            elif choice == "5":
                sentiment_analysis()
            elif choice == "6":
                topic_insights()
            elif choice == "7":
                recommendations()
            elif choice == "8":
                export_csv()
            elif choice == "9":
                print("Thank you for using InsightEd!")
                break
            else:
                print("Invalid choice. Try again.")

        except requests.RequestException as error:
            print("\nCould not connect to the backend.")
            print("Make sure your FastAPI server is running.")
            print("Details:", error)


if __name__ == "__main__":
    main()
