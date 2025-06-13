#import libraries
from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker
import random
from bson.objectid import ObjectId
import bson
import pprint as pp



#connect to mongoclient
client = MongoClient ("mongodb://localhost:27017")
fake = Faker()



#connect to database
db = client["eduhub_db"]
users_col = db["users"]
courses_col = db["courses"]
enrollments_col = db["enrollments"]
lessons_col = db["lessons"]
assignments_col = db["assignments"]
submissions_col = db["submissions"]



#CREATE USER SCHEMA
#Preselected values
roles = ["student", "instructor"]

bio = [
    "Passionate about lifelong learning and sharing knowledge.",
    "Loves# to solve problems through technology and data.",
    "Driven by curiosity and a desire to build meaningful things.",
    "Helping students grow into world-class developers.",
    "Committed to creating impactful learning experiences."
]

avatar = [
    "https://api.dicebear.com/6.x/thumbs/svg?seed=Alpha",
    "https://api.dicebear.com/6.x/thumbs/svg?seed=Beta",
    "https://api.dicebear.com/6.x/thumbs/svg?seed=Gamma",
    "https://api.dicebear.com/6.x/thumbs/svg?seed=Delta",
    "https://api.dicebear.com/6.x/thumbs/svg?seed=Echo",
    "https://api.dicebear.com/6.x/thumbs/svg?seed=Zeta",
    "https://api.dicebear.com/6.x/thumbs/svg?seed=Orion",
    "https://api.dicebear.com/6.x/thumbs/svg?seed=Nova",
    "https://api.dicebear.com/6.x/thumbs/svg?seed=Pixel",
    "https://api.dicebear.com/6.x/thumbs/svg?seed=Rocket"
]

skills = [
    "Python", "MongoDB", "Data Engineering", "ETL", "Machine Learning",
    "Cloud Computing", "Docker", "JavaScript", "SQL", "APIs"
]

# Generate users_schema
users_schema = []

for i in range(1, 101):
    r_user = {
        "_id" : ObjectId(),
        "user_id" : f"U{str(i).zfill(3)}",
        "email" : fake.email(),
        "first_name" : fake.first_name(),
        "last_name" : fake.last_name(),
        "date_joined" : fake.date_time_between(start_date="-1y", end_date="now"),
        "role" : random.choice(roles),
        "profile" : {
            "bio" : random.choice(bio),
            "avatar" : random.choice(avatar),
            "skills" : random.sample(skills, k=3)
        },

        "is_active" : random.choice([True, False])
    }

    users_schema.append(r_user)




#Create course schema
# Preselected options
categories = ["Data Engineering", "Web Development", "Cloud Computing", "AI", "DevOps"]
levels = ["beginner", "intermediate", "advanced"]
tags = [
    "project-based", "career-ready", "hands-on", "real-world", "certification",
    "mentor-supported", "interactive", "video-tutorials", "downloadable-resources",
    "quiz-included", "assignment-driven", "lifetime-access", "community-support",
    "interview-prep", "beginner-friendly"
]
descriptions = [
    "Learn how to build scalable data pipelines using modern tools and best practices.",
    "This course introduces you to web development using HTML, CSS, and JavaScript.",
    "Master cloud infrastructure and deployment using AWS, Docker, and Kubernetes.",
    "Understand core machine learning concepts with hands-on Python projects.",
    "Get started with databases and SQL for data analysis and backend development.",
    "Develop a strong foundation in data engineering with real-world ETL scenarios.",
    "Explore modern DevOps workflows, CI/CD pipelines, and monitoring strategies.",
    "Learn to build REST APIs and microservices with Flask and Django.",
    "Gain experience in big data technologies like Spark and Hadoop.",
    "Prepare for a career in AI with deep learning and neural network fundamentals."
]

titles = [
    "Python for Beginners",
    "Data Engineering with Python",
    "MongoDB for Developers",
    "Big Data Processing with Spark",
    "Machine Learning with scikit-learn",
    "Deep Learning with TensorFlow",
    "Data Visualization with Seaborn",
    "AWS Cloud Fundamentals",
    "Building REST APIs with FastAPI",
    "Kubernetes for Developers",
    "Unit Testing in Python",
    "Git & GitHub for Collaboration",
    "Clean Code and Refactoring",
    "Computer Vision with OpenCV",
    "Deploying Applications with Docker"
]

# Simulated instructor user_ids (replace with real ones later)
instructor_ids = [f"U{str(i).zfill(3)}" for i in range(1, 41)]

# Generate courses
course_schema = []

for i in range(1, 101):
    r_course = {
        "_id": ObjectId(),
        "course_id": f"C{str(i).zfill(3)}",
        "title": random.choice(titles),
        "description": random.choice(descriptions),
        "instructor_id": random.choice(instructor_ids),
        "category": random.choice(categories),
        "level": random.choice(levels),
        "duration": random.randint(5, 60),  # hours
        "price": random.choice([0, 50, 100, 150, 200, 250, 300]), 
        "tags": random.sample(tags, k=3),
        "created_at": fake.date_time_between(start_date="-6M", end_date="now"),
        "updated_at": datetime.now(),
        "is_published": random.choice([True, False])
    }

    course_schema.append(r_course)




#INSERT 20 USERS (mix of students and instructors)

users_schema = []
for i in range(1, 21):
    user = {
        "_id": ObjectId(),
        "user_id": f"U{str(i).zfill(3)}",
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "date_joined": fake.date_time_between(start_date="-1y", end_date="now"),
        "role": random.choice(roles),
        "profile": {
            "bio": random.choice(bio),
            "avatar": random.choice(avatar),
            "skills": random.sample(skills, k=3)
        },
        "is_active": random.choice([True, False])
    }
    users_schema.append(user)





#INSERT 8 COURSES ACROSS DIFFERENT CATEGORIES

course_schema = []

for i in range(1, 9):
    course = {
        "_id": ObjectId(),
        "course_id": f"C{str(i).zfill(3)}",
        "title": random.choice(titles),
        "description": random.choice(descriptions),
        "instructor_id": random.choice([user["user_id"] for user in users_schema if user["role"] == "instructor"]),
        "category": random.choice(categories),
        "level": random.choice(levels),
        "duration": random.randint(5, 60),
        "price": random.choice([0, 50, 100, 150, 200, 250, 300]),
        "tags": random.sample(tags, k=3),
        "created_at": fake.date_time_between(start_date="-6M", end_date="now"),
        "updated_at": datetime.now(),
        "is_published": random.choice([True, False])
    }
    course_schema.append(course)

# Clear and insert
courses_col.delete_many({})
courses_col.insert_many(course_schema)

print(" Inserted 8 courses successfully.")






#INSERT 15 ENROLLMENTS

enrollment_schema = []

for i in range(1, 16):
    student = random.choice([user for user in users_schema if user["role"] == "student"])
    course = random.choice(course_schema)

    enrollment = {
        "_id": ObjectId(),
        "enrollment_id": f"E{str(i).zfill(3)}",
        "user_id": student["user_id"],
        "course_id": course["course_id"],
        "enrolled_on": fake.date_time_between(start_date=course["created_at"], end_date="now"),
        "progress": random.randint(0, 100),
        "completed": random.choice([True, False])
    }

    enrollment_schema.append(enrollment)

# Clear and insert
enrollments_col.delete_many({})
enrollments_col.insert_many(enrollment_schema)

print("Inserted 15 enrollments successfully.")






lesson_schema = []

for i in range(1, 26):
    course = random.choice(course_schema)

    lesson = {
        "_id": ObjectId(),
        "lesson_id": f"L{str(i).zfill(3)}",
        "course_id": course["course_id"],
        "title": f"Lesson {i}: {random.choice(titles)}",
        "content": fake.paragraph(nb_sentences=5),
        "video_url": f"https://example.com/video/{i}",
        "resources": [f"https://resource.com/{fake.word()}" for _ in range(2)],
        "order": i,
        "created_at": datetime.now()
    }

    lesson_schema.append(lesson)

# Clear and insert
lessons_col.delete_many({})
lessons_col.insert_many(lesson_schema)

print(" Inserted 25 lessons successfully.")





#INSERT 10 ASSIGNMENTS
 
assignment_schema = []

for i in range(1, 11):
    lesson = random.choice(lesson_schema)
    
    assignment = {
        "_id": ObjectId(),
        "assignment_id": f"A{str(i).zfill(3)}",
        "course_id": lesson["course_id"],
        "lesson_id": lesson["lesson_id"],
        "title": f"Assignment {i}: {random.choice(titles)}",
        "description": fake.paragraph(nb_sentences=3),
        "due_date": datetime.now() + timedelta(days=random.randint(3, 14)),
        "max_score": 100,
        "created_at": datetime.now()
    }

    assignment_schema.append(assignment)

# Clear and insert
assignments_col.delete_many({})
assignments_col.insert_many(assignment_schema)

print(" Inserted 10 assignments successfully.")




#Insert 12 submissions

submission_schema = []

for i in range(1, 13):
    assignment = random.choice(assignment_schema)
    student = random.choice([user for user in users_schema if user["role"] == "student"])

    submission = {
        "_id": ObjectId(),
        "submission_id": f"S{str(i).zfill(3)}",
        "assignment_id": assignment["assignment_id"],
        "user_id": student["user_id"],
        "submitted_on": datetime.now() - timedelta(days=random.randint(0, 5)),
        "content": fake.paragraph(nb_sentences=4),
        "score": random.randint(50, 100),
        "graded": random.choice([True, False])
    }

    submission_schema.append(submission)

# Clear and insert
submissions_col.delete_many({})
submissions_col.insert_many(submission_schema)

print(" Inserted 12 submissions successfully.")





#CRUD OPERATIONS

#add new student user
new_user = {
    "_id": ObjectId(),
    "user_id": "U999",
    "email": "newuser@example.com",
    "first_name": "Feyisayo",
    "last_name": "Ajiboye",
    "date_joined": datetime.now(),
    "role": "student",
    "profile": {
        "bio": "Excited to explore the world of data.",
        "avatar": "https://api.dicebear.com/6.x/thumbs/svg?seed=Nova",
        "skills": ["Python", "MongoDB", "SQL"]
    },
    "is_active": True
}

# Insert user
users_col.insert_one(new_user)

print(" New user added successfully.")




#create a new course
# Get the first instructor from the users collection
instructor = db.altuserschema.find_one({"role": "instructor"})

if instructor:
    new_course = {
        "title": "Databases Design Fundamentals",
        "description": "Learning relational and NoSQL DB design.",
        "category": "Database",
        "instructor_id": instructor["_id"],
        "price": 20000,
        "created_at": datetime.utcnow()
    }

    course_result = db.courses.insert_one(new_course)
    course_id = course_result.inserted_id
    print("New course ID:", course_id)
else:
    print("No instructor found. Please add one.")

#validate 
user = users_col.find_one({"user_id": "U999"})

if user:
    print("User found:")
    pp.pprint(user)
else:
    print(" User not found.")





#insert one course
new_course = {
    "_id": ObjectId(),
    "course_id": "C999",
    "title": "Data Engineering Essentials",
    "description": "Master the basics of data pipelines, ETL, and database management.",
    "instructor_id": "U005",  # make sure this ID belongs to an instructor
    "category": "Data Engineering",
    "level": "beginner",
    "duration": 40,
    "price": 150,
    "tags": ["project-based", "career-ready", "interactive"],
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
    "is_published": True
}

# Insert course
courses_col.insert_one(new_course)

print("New course added successfully.")

#validate
course = courses_col.find_one({"course_id": "C999"})

if course:
    print("Course found:")
    pp.pprint(course)
else:
    print("Course not found.")




#Enroll a student 
# Example: Enroll user U999 into course C999
new_enrollment = {
    "_id": ObjectId(),
    "enrollment_id": "E999",
    "user_id": "U999",          # must be a student
    "course_id": "C999",
    "enrolled_on": datetime.now(),
    "progress": 0,
    "is_active": True
}

# Insert enrollment
enrollments_col.insert_one(new_enrollment)

print(" Student enrolled successfully.")

#Validate 

enrollment = enrollments_col.find_one({"enrollment_id": "E999"})

if enrollment:
    print(" Enrollment found:")
    pp.pprint(enrollment)
else:
    print(" Enrollment not found.")





#Add a new lesson 
new_lesson = {
    "_id": ObjectId(),
    "lesson_id": "L999",
    "course_id": "C999",  # existing course
    "title": random.choice(titles),  # from your preselected titles
    "content": "This lesson introduces the fundamentals of data engineering.",
    "duration": random.randint(10, 30),  # in minutes
    "resources": [
        "https://example.com/resource1",
        "https://example.com/resource2"
    ],
    "created_at": datetime.now()
}

# Insert lesson
lessons_col.insert_one(new_lesson)

print(" Lesson added successfully.")
#Validate 
lesson = lessons_col.find_one({"lesson_id": "L999"})

if lesson:
    print(" Lesson found:")
    pp.pprint(lesson)
else:
    print(" Lesson not found.")




#READ OPERATIONS
 
#Find all active students 

active_students = users_col.find({
    "role": "student",
    "is_active": True
})

print("Active Students:")
for student in active_students:
    print(f"{student['user_id']} - {student['first_name']} {student['last_name']}")







pipeline = [
    {
        "$match": {"course_id": "C004"}
    },
    {
        "$lookup": {
            "from": "users",
            "localField": "instructor_id",
            "foreignField": "user_id",
            "as": "instructor_info"
        }
    },
    {
        "$unwind": "$instructor_info"
    },
    {
        "$project": {
            "_id": 0,
            "course_id": 1,
            "title": 1,
            "category": 1,
            "level": 1,
            "price": 1,
            "instructor": {
                "full_name": {
                    "$concat": [
                        "$instructor_info.first_name",
                        " ",
                        "$instructor_info.last_name"
                    ]
                },
                "email": "$instructor_info.email",
                "skills": "$instructor_info.profile.skills"
            }
        }
    }
]

result = list(courses_col.aggregate(pipeline))

if result:
    print(" Course with Instructor Info:")
    pp.pprint(result[0])
else:
    print("No course found.")






#Get all courses in a specific category 
category_name = "Data Engineering"

courses = courses_col.find({"category": category_name})

print(f" Courses in category: {category_name}")
for course in courses:
    print(f"{course['course_id']} - {course['title']}")




#Find students enrolled in a specific course 
pipeline = [
    {
        "$match": {"course_id": "C004"}
    },
    {
        "$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "user_id",
            "as": "student_info"
        }
    },
    {
        "$unwind": "$student_info"
    },
    {
        "$match": {"student_info.role": "student"}
    },
    {
        "$project": {
            "_id": 0,
            "enrollment_id": 1,
            "user_id": 1,
            "course_id": 1,
            "student_name": {
                "$concat": [
                    "$student_info.first_name", " ", "$student_info.last_name"
                ]
            },
            "email": "$student_info.email",
            "enrolled_on": 1
        }
    }
]

students = list(enrollments_col.aggregate(pipeline))

if students:
    print(" Enrolled Students in Course C004:")
    for s in students:
        pp.pprint(s)
else:
    print(" No students enrolled in this course.")





#search courses by title (case_insensitive, partial match)
search_term = "AWS Cloud Fundamentals" 

courses = courses_col.find({
    "title": {"$regex": search_term, "$options": "i"}
})

print(f" Courses matching '{search_term}'")
for course in courses:
    print(f"{course['course_id']} - {course['title']}")




#Update a user's profile information

users_col.update_one(
    {"user_id": "U004"},
    {
        "$set": {
            "profile.bio": "Always learning. Always building.",
            "profile.avatar": "https://api.dicebear.com/6.x/thumbs/svg?seed=Nova",
            "profile.skills": ["Python", "MongoDB", "APIs"]
        }
    }
)

# Validate
user = users_col.find_one({"user_id": "U004"})
if user:
    print(" Updated Profile:")
    pp.pprint(user["profile"])
else:
    print(" User not found.")




#Mark a course as published
courses_col.update_one(
    {"course_id": "C004"},
    {"$set": {"is_published": True}}
)

# Validate
course = courses_col.find_one({"course_id": "C999"})
if course:
    print(f" Course '{course['title']}' is now published.")
else:
    print(" Course not found.")




#Update assignment grades
submissions_col.update_one(
    {"submission_id": "S004"},
    {"$set": {"grade": 85}}
)

#Validate
submission = submissions_col.find_one({"submission_id": "S004"})
if submission:
    print(f" Grade updated: {submission['grade']}")
else:
    print(" Submission not found.")




#Add tags to an existing course
courses_col.update_one(
    {"course_id": "C004"},
    {"$addToSet": {
        "tags": {
            "$each": ["interview-prep", "lifetime-access"]
        }
    }}
)

#  Validate
course = courses_col.find_one({"course_id": "C004"})
if course:
    print(f" Updated Tags for {course['title']}:")
    print(course["tags"])
else:
    print("Course not found.")





#Remove a user(soft deleting by setting isActive is false)
users_col.update_one(
    {"user_id": "U004"},
    {"$set": {"is_active": False}}
)

# Validate
user = users_col.find_one({"user_id": "U004"})
if user:
    status = "Active" if user["is_active"] else "Inactive"
    print(f" User {user['user_id']} is now marked as: {status}")
else:
    print(" User not found.")




#delete an enrollment
enrollments_col.delete_one({"enrollment_id": "E004"})

# Validate
enrollment = enrollments_col.find_one({"enrollment_id": "004"})
if not enrollment:
    print("Enrollment deleted successfully.")
else:
    print("Enrollment still exists.")




#remove a lesson from a course
lessons_col.delete_one({"lesson_id": "L004"})


lesson = lessons_col.find_one({"lesson_id": "L004"})

if not lesson:
    print(" Lesson deleted successfully.")
else:
    print(" Lesson still exists.")





#Find courses with prices between 50 and 200

courses = courses_col.find({
    "price": {"$gte": 50, "$lte": 200}
})

print(" Courses priced between $50 and $200:")
for course in courses:
    print(f"{course['course_id']} - {course['title']} (${course['price']})")



#get users who joined in the last 6 months
six_months_ago = datetime.now() - timedelta(days=180)

recent_users = users_col.find({
    "date_joined": {"$gte": six_months_ago}
})

print("Users who joined in the last 6 months:")
for user in recent_users:
    print(f"{user['user_id']} - {user['first_name']} {user['last_name']} (Joined: {user['date_joined']})")




#find courses that have specific tags using $in operators
target_tags = ["career-ready", "assignment-driven", "interactive"]

courses = courses_col.find({
    "tags": {"$in": target_tags}
})

print(" Courses with selected tags:")
for course in courses:
    print(f"{course['course_id']} - {course['title']} | Tags: {course['tags']}")



#Retrieve assignments with due dates in the next week
today = datetime.now()
next_week = today + timedelta(days=7)

upcoming_assignments = assignments_col.find({
    "due_date": {
        "$gte": today,
        "$lte": next_week
    }
})

print(" Assignments due in the next 7 days:")
for assignment in upcoming_assignments:
    print(f"{assignment['assignment_id']} - {assignment['title']} | Due: {assignment['due_date']}")




#Count total enrollment per course
pipeline = [
    {
        "$group": {
            "_id": "$course_id",
            "total_enrollments": {"$sum": 1}
        }
    },
    {
        "$sort": {"total_enrollments": -1}
    }
]

results = list(enrollments_col.aggregate(pipeline))

print(" Total enrollments per course:")
for item in results:
    print(f"Course: {item['_id']} | Enrollments: {item['total_enrollments']}")







#Calculate average course rating

pipeline = [
    {
        "$project": {
            "course_id": 1,
            "title": 1,
            "average_rating": {"$avg": "$ratings"}
        }
    },
    {
        "$sort": {"average_rating": -1}
    }
]

results = list(courses_col.aggregate(pipeline))

for course in results:
    avg = course.get('average_rating')
    if avg is not None:
        print(f"{course['course_id']} - {course['title']} | Avg Rating: {round(avg, 2)}")
    else:
        print(f"{course['course_id']} - {course['title']} | Avg Rating: Not Available")






#Group by course category
pipeline = [
    {
        "$group": {
            "_id": "$category",
            "total_courses": {"$sum": 1}
        }
    },
    {
        "$sort": {"total_courses": -1}
    }
]

results = list(courses_col.aggregate(pipeline))

print(" Total courses per category:")
for item in results:
    print(f"{item['_id']} → {item['total_courses']} courses")





#Average grade per student 
pipeline = [
    {
        "$group": {
            "_id": "$user_id",
            "average_grade": {"$avg": "$grade"}
        }
    },
    {
        "$sort": {"average_grade": -1}
    }
]

results = list(submissions_col.aggregate(pipeline))

print(" Average grade per student:")
for student in results:
    avg = student.get('average_grade')
    if avg is not None:
        print(f"Student: {student['_id']} → Avg Grade: {round(avg, 2)}")
    else:
        print(f"Student: {student['_id']} → Avg Grade: Not Available")





#Completion rate by courses
pipeline = [
    {
        "$match": {"status": "completed"}
    },
    {
        "$group": {
            "_id": "$course_id",
            "completed_count": {"$sum": 1}
        }
    },
    {
        "$lookup": {
            "from": "enrollments",
            "localField": "_id",
            "foreignField": "course_id",
            "as": "enrollments"
        }
    },
    {
        "$project": {
            "course_id": "$_id",
            "completed_count": 1,
            "total_enrolled": {"$size": "$enrollments"},
            "completion_rate": {
                "$cond": [
                    {"$eq": [{"$size": "$enrollments"}, 0]},
                    0,
                    {
                        "$multiply": [
                            {"$divide": ["$completed_count", {"$size": "$enrollments"}]},
                            100
                        ]
                    }
                ]
            }
        }
    },
    {
        "$sort": {"completion_rate": -1}
    }
]

results = list(submissions_col.aggregate(pipeline))

print(" Completion rate by course")
for item in results:
    print(f"{item['course_id']} → {round(item['completion_rate'], 2)}%")








#Top performing student
pipeline = [
    {
        "$group": {
            "_id": "$user_id",
            "average_grade": {"$avg": "$grade"},
            "total_submissions": {"$sum": 1}
        }
    },
    {
        "$sort": {"average_grade": -1}
    },
    {
        "$limit": 5  # top 5 students
    }
]

results = list(submissions_col.aggregate(pipeline))

print(" Top Performing Students:")
for student in results:
    avg = student.get('average_grade')
    if avg is not None:
        print(f"Student: {student['_id']} → Avg Grade: {round(avg, 2)} | Submissions: {student['total_submissions']}")
    else:
        print(f"Student: {student['_id']} → Avg Grade: Not Available | Submissions: {student['total_submissions']}")






#Total student taught by each instructor

Instructor analysis


pipeline = [
    {
        "$lookup": {
            "from": "courses",
            "localField": "course_id",
            "foreignField": "course_id",
            "as": "course_info"
        }
    },
    { "$unwind": "$course_info" },
    {
        "$group": {
            "_id": "$course_info.instructor_id",
            "total_students": { "$addToSet": "$user_id" }
        }
    },
    {
        "$project": {
            "instructor_id": "$_id",
            "total_students": { "$size": "$total_students" },
            "_id": 0
        }
    }
]

results = list(enrollments_col.aggregate(pipeline))


for item in results:
    print(f"Instructor: {item['instructor_id']} → Students Taught: {item['total_students']}")



#Average course rating per instructor

pipeline = [
    {
        "$group": {
            "_id": "$instructor_id",
            "average_rating": { "$avg": "$rating" }
        }
    },
    {
        "$project": {
            "instructor_id": "$_id",
            "average_rating": 1,
            "_id": 0
        }
    }
]

results = list(courses_col.aggregate(pipeline))


def safe_print(label, value, suffix=""):
    if value is not None:
        print(f"{label} → {round(value, 2)}{suffix}")
    else:
        print(f"{label} → Not Available")

for item in results:
    safe_print(item['instructor_id'], item.get('average_rating'))





#Revenue generated per instructor 

pipeline = [
    {
        "$lookup": {
            "from": "courses",
            "localField": "course_id",
            "foreignField": "course_id",
            "as": "course_info"
        }
    },
    { "$unwind": "$course_info" },
    {
        "$group": {
            "_id": "$course_info.instructor_id",
            "total_revenue": { "$sum": "$course_info.price" }
        }
    },
    {
        "$project": {
            "instructor_id": "$_id",
            "total_revenue": 1,
            "_id": 0
        }
    }
]

results = list(enrollments_col.aggregate(pipeline))


for item in results:
    safe_print(item['instructor_id'], item['total_revenue'], suffix=" USD")






#Monthly enrollment trends
#monthly enrolment trends

pipeline = [
    {
        "$group": {
            "_id": {
                "year": { "$year": "$enrolled_at" },
                "month": { "$month": "$enrolled_at" }
            },
            "total_enrollments": { "$sum": 1 }
        }
    },
    {
        "$sort": {
            "_id.year": 1,
            "_id.month": 1
        }
    }
]

results = list(enrollments_col.aggregate(pipeline))


for item in results:
    year = item["_id"]["year"]
    month = item["_id"]["month"]
    total = item["total_enrollments"]
    print(f"{year}-{str(month).zfill(2)} → {total} enrollments")





#most popular course categories
pipeline = [
    {
        "$lookup": {
            "from": "courses",
            "localField": "course_id",
            "foreignField": "course_id",
            "as": "course_info"
        }
    },
    { "$unwind": "$course_info" },
    {
        "$group": {
            "_id": "$course_info.category",
            "total_enrollments": { "$sum": 1 }
        }
    },
    {
        "$sort": { "total_enrollments": -1 }
    }
]

results = list(enrollments_col.aggregate(pipeline))


for item in results:
    print(f"Category: {item['_id']} → Enrollments: {item['total_enrollments']}")




#Student metrics engagement 


#1 Number of Courses Enrolled per Student

pipeline = [
    {
        "$group": {
            "_id": "$user_id",
            "courses_enrolled": { "$sum": 1 }
        }
    },
    {
        "$project": {
            "user_id": "$_id",
            "courses_enrolled": 1,
            "_id": 0
        }
    }
]

courses_enrolled = list(enrollments_col.aggregate(pipeline))


#2 Number of Assignments Submitted per Student
pipeline = [
    {
        "$group": {
            "_id": "$user_id",
            "assignments_submitted": { "$sum": 1 }
        }
    },
    {
        "$project": {
            "user_id": "$_id",
            "assignments_submitted": 1,
            "_id": 0
        }
    }
]

assignments_done = list(submissions_col.aggregate(pipeline))



#3 Lessons Completed



from collections import defaultdict

engagement = defaultdict(lambda: {"courses_enrolled": 0, "assignments_submitted": 0})


# Update course enrollments
for item in courses_enrolled:
    uid = item["user_id"]
    engagement[uid]["courses_enrolled"] = item["courses_enrolled"]

# Update assignment submissions
for item in assignments_done:
    uid = item["user_id"]
    engagement[uid]["assignments_submitted"] = item["assignments_submitted"]

# Print engagement per student
for user_id, metrics in engagement.items():
    print(f"User: {user_id} → Courses: {metrics['courses_enrolled']} | Submissions: {metrics['assignments_submitted']}")




#User email lookup


# Create an index on email field to speed up lookups
users_col.create_index("email")

# Test the index with a lookup
email_to_find = "destinysalazar@example.com"
user = users_col.find_one({"email": email_to_find})

if user:
    print(f" User found: {user['first_name']} {user['last_name']}")
else:
    print(" User not found.")





#Course search by title and category 
# Create compound index on title and category fields
courses_col.create_index([("title", 1), ("category", 1)])

# Example search: partial title match (case-insensitive) and exact category
title_keyword = "MongoDB for Developers"
category_filter = "Web Development"

courses = courses_col.find({
    "title": { "$regex": title_keyword, "$options": "i" },
    "category": category_filter
})

# Display results
for course in courses:
    print(f"{course['title']} → {course['category']}")






#Assignment queries by due date

# Create index on due_date for fast date-based queries
assignments_col.create_index("due_date")

# Example: Find assignments due within the next 7 days
from datetime import datetime, timedelta

today = datetime.now()
next_week = today + timedelta(days=7)

upcoming_assignments = assignments_col.find({
    "due_date": { "$gte": today, "$lte": next_week }
})

# Display results
for a in upcoming_assignments:
    print(f"{a['title']} → Due: {a['due_date'].strftime('%Y-%m-%d')}")





#Enrollment queries by student and courses 

# Create indexes on student_id and course_id
enrollments_col.create_index("user_id")
enrollments_col.create_index("course_id")

# Example: Find all enrollments of a specific student in a specific course
user_id = "U001"
course_id = "C006"

enrollments = enrollments_col.find({
    "user_id": user_id,
    "course_id": course_id
})

# Display results
for e in enrollments:
    print(f"Student {e['user_id']} is enrolled in Course {e['course_id']}")






#Analyze query performance using explain() method in pymongo 

# Example query (search course by title, case-insensitive)
query = {
    "title": { "$regex": "python", "$options": "i" }
}

# Using xplain to analyze query performance
explain_result = courses_col.find(query).explain()

# Print key insights
print("Query Execution Stats:")
print("Execution Time (ms):", explain_result["executionStats"]["executionTimeMillis"])
print("Total Documents Examined:", explain_result["executionStats"]["totalDocsExamined"])
print("Index Used:", explain_result["queryPlanner"]["winningPlan"]["inputStage"].get("indexName", "None"))



#Optimize at least 3 slow queries 
#Slow query 

courses_col.find({
    "title": { "$regex": "python", "$options": "i" },
    "category": "Data Engineering"
})


#Optimization 

# Create compound index
courses_col.create_index([("title", 1), ("category", 1)])


#Analyze

courses_col.find({
    "title": { "$regex": "python", "$options": "i" },
    "category": "Data Engineering"
}).explain()





#2. Find Assignments Due in Next 7 Days

#Slow query

assignments_col.find({
    "due_date": { "$gte": datetime.now(), "$lte": datetime.now() + timedelta(days=7) }
})


#Optimization 

# Index on due_date
assignments_col.create_index("due_date")


#Analyze

assignments_col.find({
    "due_date": { "$gte": datetime.now(), "$lte": datetime.now() + timedelta(days=7) }
}).explain()



#3. Find All Enrollments for a Student
#Slow query 

enrollments_col.find({ "student_id": "U005" })


#Optimization 

# Index on student_id
enrollments_col.create_index("student_id")

#Analyze

enrollments_col.find({ "student_id": "U005" }).explain()



#Document the performance improvements using python timing functions 

#Example: Measure and Compare Query Time (Courses by Title + Category)


import time

# Query definition
query = {
    "title": { "$regex": "python", "$options": "i" },
    "category": "Data Engineering"
}

# Measure execution time before index
start_time = time.time()
courses_col.find(query).explain()
end_time = time.time()
print(" Time without index: {:.4f} seconds".format(end_time - start_time))

# Create compound index
courses_col.create_index([("title", 1), ("category", 1)])

# Measure execution time after index
start_time = time.time()
courses_col.find(query).explain()
end_time = time.time()
print(" Time with index: {:.4f} seconds".format(end_time - start_time))





#schema validation 


#Implement validation rules for :
#Required fields
#Data type validation
#Enum value restictions
#Email format validation


db.create_collection("users_validated", validator={
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id", "email", "first_name", "last_name", "role", "date_joined", "is_active"],
        "properties": {
            "user_id": { "bsonType": "string" },
            "email": { "bsonType": "string" },
            "first_name": { "bsonType": "string" },
            "last_name": { "bsonType": "string" },
            "role": { 
                "enum": ["student", "instructor"],
                "description": "Role must be student or instructor"
            },
            "date_joined": { "bsonType": "date" },
            "is_active": { "bsonType": "bool" }
        }
    }
})





#Inserting a valid document 

db.users_validated.insert_one({
    "user_id": "U999",
    "email": "valid@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "role": "student",
    "date_joined": datetime.now(),
    "is_active": True
})





#Error handling 

#WRITING QUERIES THAT HANDLES THE FOLLOWING COMMON ERRORS::
#1 Duplicate key error
#2 Invalid data type insertion
#3 Missing required fields


from pymongo.errors import DuplicateKeyError, WriteError, WriteConcernError

try:
    db.users_validated.insert_one({
        
        "_id": ObjectId("666abcd12345678901234567"),  # May cause duplicate _id
        "user_id": "U100",
        "email": "invalidemail.com",  # invalid if regex used
        "first_name": "John",
        "last_name": "Doe",
        "role": "admin",  # Invalid enum if validation applied
        "date_joined": "2024-01-01",  # Wrong type if not converted to datetime
        # "is_active" is missing (required)
    })

except DuplicateKeyError as e:
    print("Duplicate Key Error:", e)

except WriteError as e:
    print("Write Error (Validation failed):", e)

except WriteConcernError as e:
    print(" Write Concern Error:", e)

except Exception as e:
    print(" General Error:", e)




#####BONUS CHALLENGE


#Implement text search functionality for course content 

#Step 1: Create Text Index on Course Fields

courses_col.create_index([
    ("title", "text"),
    ("description", "text"),
    ("tags", "text")
])


#Step 2: Text Search Query

def search_courses_by_text(keyword):
    results = courses_col.find({
        "$text": { "$search": keyword }
    })

    for course in results:
        print(f" {course['title']} - {course['description'][:60]}...")



#Example usage

search_courses_by_text("python ETL")




#Recommendation system using Aggregation 

#Match User’s Skills to Course Tags

def recommend_courses(user_id):
    # Step 1: Get user's skills
    user = users_col.find_one({"user_id": user_id})
    if not user:
        print(" User not found.")
        return

    user_skills = user["profile"]["skills"]

    # Step 2: Match courses using aggregation
    pipeline = [
        {
            "$match": {
                "tags": {"$in": user_skills},
                "is_published": True
            }
        },
        {
            "$addFields": {
                "matched_skills": {
                    "$size": {"$setIntersection": ["$tags", user_skills]}
                }
            }
        },
        { "$sort": { "matched_skills": -1, "price": 1 } },  # prioritize relevance + cheap
        { "$limit": 5 }  # Top 5 recommendations
    ]

    recommendations = courses_col.aggregate(pipeline)

    print(f"\n Course Recommendations for {user['first_name']} {user['last_name']}")
    for course in recommendations:
        print(f" {course['title']} (Matched Skills: {course['matched_skills']})")


#Example usage 

recommend_courses("U007")



#Design a data archiving strategy for old enrollments

#Step 1: Create Archive Collection

archived_col = db["archived_enrollments"]


#Step 2: Define the Archiving Logic

def archive_old_enrollments():
    # 6 months ago
    six_months_ago = datetime.now() - timedelta(days=180)

    # Find old enrollments
    old_enrollments = list(enrollments_col.find({
        "enrolled_on": { "$lt": six_months_ago }
    }))

    if not old_enrollments:
        print("📭 No old enrollments to archive.")
        return

    # Insert into archive
    archived_col.insert_many(old_enrollments)

    # Delete from main collection
    ids_to_delete = [doc["_id"] for doc in old_enrollments]
    enrollments_col.delete_many({ "_id": { "$in": ids_to_delete } })

    print(f" Archived {len(old_enrollments)} old enrollments.")



#Example usage

archive_old_enrollments()



#implement Geospatial queries for location based course recommendations


#Step 1: Update Courses with Geo Data

# Example: Update some existing courses
courses_col.update_many(
    {},
    [{
        "$set": {
            "location": {
                "type": "Point",
                "coordinates": [
                    random.uniform(3.30, 3.60),   # Longitude (e.g., Lagos)
                    random.uniform(6.40, 6.70)    # Latitude
                ]
            }
        }
    }]
)



#Step 2: Create 2dsphere Index

courses_col.create_index([("location", "2dsphere")])


#Step 3: Query for Nearby Courses

def recommend_nearby_courses(user_coordinates, max_distance_km=10):
    results = courses_col.find({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": user_coordinates
                },
                "$maxDistance": max_distance_km * 1000  # meters
            }
        },
        "is_published": True
    })

    print(f"\n Recommended Courses within {max_distance_km} km:")
    for course in results:
        print(f" {course['title']} - Category: {course['category']}")




#Example usage 

# Example: user near Ikeja, Lagos
user_coords = [3.35, 6.60]  # [longitude, latitude]
recommend_nearby_courses(user_coords, max_distance_km=10)

