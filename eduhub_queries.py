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
collection = db["users"]
collection1 = db["courses"]
collection2 = db["enrollments"]
collection3 = db["lessons"]
collection4 = db["assignments"]
collection5 = db["submissions"]
collection6 = db["altuserschema"]
collection7 = db["altcourseschema"]



#CREATE USER SCHEMA
# Preselected values
roles = ["student", "instructor"]

bio = [
    "Passionate about lifelong learning and sharing knowledge.",
    "Loves to solve problems through technology and data.",
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
    user = {
        "_id": ObjectId(),
        "user_id": f"U{str(i).zfill(3)}",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "date_joined": fake.date_time_between(start_date="-1y", end_date="now"),
        "role": random.choice(roles),
        "profile": {
            "bio": random.choice(bio),
            "avatar": random.choice(avatar),
            "skills": random.sample(skills, k=3),

        "is_active": random.choice([True, False])
        }
    }
    users_schema.append(user)



#insert user_schema into mongo compass
collection6.insert_many(users_schema)
print("documents inserted")



#list database and collections
print (client.list_database_names())
print (db.list_collection_names())



#find_one method to verify schema
sample = collection6.find_one()
print ("\nSample document:")
print (sample)




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
    course = {
        "_id": ObjectId(),
        "course_id": f"C{str(i).zfill(3)}",
        "title": random.choice(titles),
        "description": random.choice(descriptions),
        "instructor_id": random.choice(instructor_ids),
        "category": random.choice(categories),
        "level": random.choice(levels),
        "duration": random.randint(5, 60),  # hours
        "price": random.choice([0, 3000, 5000, 10000, 20000]), 
        "tags": random.sample(tags, k=3),
        "created_at": fake.date_time_between(start_date="-6M", end_date="now"),
        "updated_at": datetime.now(),
        "is_published": random.choice([True, False])
    }
    course_schema.append(course)




#Insert course schema inti mongodb compass
collection7.insert_many(course_schema)
print("documents inserted")



#use find one method to verify the validity of course_schema collection
new = collection7.find_one()
new



#Insert sample data
#20 users (mix of students and instructors)
coll_users = []
coll_roles = (["student"] * 15 + ["instructor"] * 5)

for role in coll_roles:
    coll_user = {
        "name": fake.name(),
        "email": fake.email(),
        "role": role,
        "created_at": datetime.now()
    }
    coll_users.append(coll_user)

# Insert into MongoDB
db["users"].insert_many(coll_users)



#8 courses across different categories
course_titles = [
    "Python for Beginners", "Data Engineering with Python", "MongoDB for Developers",
    "Big Data Processing with Spark", "Machine Learning with scikit-learn",
    "Deep Learning with TensorFlow", "AWS Cloud Fundamentals", "Docker for Developers",
    "Kubernetes for Developers", "Git & GitHub for Collaboration"
]

coll_courses = []

for course_title in course_titles[:8]:  # Pick first 8
    course1 = {
        "title": course_title,
        "description": fake.paragraph(),
    }
    coll_courses.append(course1)
# Insert into MongoDB
db["courses"].insert_many(coll_courses)




#15 enrollments
# Get inserted users and courses from MongoDB
enr_users = list(db["users"].find({}))
enr_courses = list(db["courses"].find({}))

# Filter only student users
student_ids = [user["_id"] for user in enr_users if user["role"] == "student"]
course_ids = [course["_id"] for course in enr_courses]

enrollments = []

for _ in range(15):
    enrollment = {
        "student_id": random.choice(student_ids),
        "course_id": random.choice(course_ids),
        "enrolled_on": datetime.now()
    }
    enrollments.append(enrollment)
# Insert into MongoDB
db["enrollments"].insert_many(enrollments)




#25 lessons
lessons = []

# Get existing courses from the DB
lesson_courses = list(db["courses"].find({}))

for _ in range(25):
    lesson = {
        "course_id": random.choice(lesson_courses)["_id"],
        "title": random.choice(titles)
        ,
        "content": fake.paragraph(nb_sentences=5),
        "created_at": datetime.now()
    }
    lessons.append(lesson)
# Insert into MongoDB
db["lessons"].insert_many(lessons)



#10 assignments
assignments = []

# Get lessons from DB
assn_lessons = list(db["lessons"].find({}))

for _ in range(10):
    assn_lesson = random.choice(assn_lessons)
    assignment = {
        "lesson_id": lesson["_id"],
        "title": random.choice(titles),
        "instructions": fake.paragraph(nb_sentences=3),
        "due_date": fake.future_datetime(end_date="+10d")
    }
    assignments.append(assignment)

# Insert into MongoDB
db["assignments"].insert_many(assignments)




#12 assignment submissions
subm_assignments = list(db["assignments"].find({}))
subm_users = list(db["users"].find({"role": "student"}))

submissions = []

for _ in range(12):
    submission = {
        "assignment_id": random.choice(subm_assignments)["_id"],
        "sub_student_id": random.choice(subm_users)["_id"],
        "sub_submitted_on": datetime.now(),
        "content": fake.paragraph(nb_sentences=4),
        "grade": random.choice(["A", "B", "C", "D", "F"])
    }
    submissions.append(submission)

# Insert into MongoDB
db["submissions"].insert_many(submissions)




#CRUD OPERATIONS

#add a new student user

new_student = {
    "name": "Tobi Lawal",
    "email": "tobi.lawal@student.com",
    "role": "student",
    "created_at": datetime.utcnow()
}

student_result = db.altuserschema.insert_one(new_student)
student_id = student_result.inserted_id
print("New student ID:", student_id)




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




#enroll a student in a course
if instructor:
    new_enrollment = {
        "user_id": student_id,
        "course_id": course_id,
        "enrolled_at": datetime.utcnow()
    }

    enroll_result = db.enrollments.insert_one(new_enrollment)
    print("Enrollment ID:", enroll_result.inserted_id)




if instructor:
    new_lesson = {
        "course_id": course_id,
        "title": "Relational vs NoSQL Databases",
        "content": "Differences, use cases, and trade-offs.",
        "duration_minutes": 40,
        "created_at": datetime.utcnow()
    }

    lesson_result = db.lessons.insert_one(new_lesson)
    print("Lesson ID:", lesson_result.inserted_id)



#find all active students
active_students = list(db.altuserschema.find({"role": "student"}))
for student in active_students:
    print(student)



#retrieve course details with instructor information

course_with_instructor = list(db.courses.aggregate([
    {
        "$lookup": {
            "from": "altuserschema",
            "localField": "instructor_id",
            "foreignField": "_id",
            "as": "instructor"
        }
    },
    {
        "$unwind": "$instructor"
    }
]))
for courses in course_with_instructor:
    print(courses)



#get all courses in a specific category
category_name = "Data Engineering" 
courses_in_category = list(db.altcourseschema.find({"category": category_name}))
for cat_course in courses_in_category:
    print(cat_course)



#find students enrolled in a specific course
course_id = ObjectId("684721e7f4edaac75f735fd8")
# Step 1: Find all enrollments for that course
enrollments = db.enrollments.find({"course_id": course_id})
# Step 2: Get all user IDs from the enrollments
student_ids = [enr["user_id"] for enr in enrollments]
# Step 3: Fetch student user details
students = list(db.enrollments.find({"_id": {"$in": student_ids}}))
for student in students:
    print(student)



#search courses by title (case_insensitive, partial match)

search_term = "web development"
matching_courses = list(db.altuserschema.find({
    "title": {"$regex": search_term, "$options": "i"}
}))
for title_course in matching_courses:
    print(title_course)




#Update a user's profile information
user_id = ObjectId('68471a8cf4edaac75f735f2d')

update_data = {
    "name": "Updated Name",
    "email": "updated.email@example.com"
}

result = db.altcourseschema.update_one(
    {"_id": user_id},
    {"$set": update_data}
)

print("Modified count:", result.modified_count)




#Mark a course as published
course_id = ObjectId("68471a8cf4edaac75f735f2c")

result = db.altcourseschema.update_one(
    {"_id": course_id},
    {"$set": {"is_published": True}}
)

print("Course published:", result.modified_count)




#Mark a course as published
course_id = ObjectId("68471a8cf4edaac75f735f2c")

result = db.altcourseschema.update_one(
    {"_id": course_id},
    {"$set": {"is_published": True}}
)

print("Course published:", result.modified_count)



#Update assignment grades
assignment_id = ObjectId("68471a8cf4edaac75f735f32")

result = db.altcourseschema.update_one(
    {"_id": assignment_id},
    {"$set": {"grade": 85}}  # update to any score
)
print("Assignment grade updated:", result.modified_count)




#Add tags to an existing course
course_id = ObjectId("68471a8cf4edaac75f735f33")

result = db.altcourseschema.update_one(
    {"_id": course_id},
    {"$addToSet": {"tags": {"$each": ["mongodb", "backend", "nosql"]}}}
)

print("Tags added:", result.modified_count)





#Remove a user(soft deleting by setting isActive is false)
user_id = ObjectId("68471a62f4edaac75f735ec5")

result = db.altuserschema.update_one(
    {"_id": user_id},
    {"$set": {"isActive": False}}
)

print("User soft-deleted:", result.modified_count)





#delete an enrollment
enrollment_id = ObjectId("68471a62f4edaac75f735ec6")

result = db.altuserschema.delete_one({"_id": enrollment_id})

print("Enrollment deleted:", result.deleted_count)




#remove a lesson from a course
lesson_id = ObjectId("684722abf4edaac75f735fe7")

result = db.lessons.delete_one({"_id": lesson_id})

print("Lesson deleted:", result.deleted_count)





#Find courses with prices between 50 and 200
#Here, i instead used prices between 3000 ans 20000 because that was the prices i inputed at the start of my code

courses_in_range = list(db.altcourseschema.find({
    "price": {"$gte": 3000, "$lte": 20000}
}))

for rang_course in courses_in_range:
    print(rang_course)



#get users who joined in the last 6 months
six_months_ago = datetime.utcnow() - timedelta(days=180)

recent_users = list(db.altuserschema.find({
    "created_at": {"$gte": six_months_ago}
}))

for user_rec in recent_users:
    print(user_rec)



#find courses that have specific tags using $in operators
tags_to_find = ["project-based", "career-ready", "hands-on", "real-world",]

matched_courses = list(db.altcourseschema.find({
    "tags": {"$in": tags_to_find}
}))

for tag_course in matched_courses:
    print(tag_course)



#Retrieve assignments with due dates in the next week
now = datetime.utcnow()
next_week = now + timedelta(days=7)

upcoming_assignments = list(db.assignments.find({
    "due_date": {"$gte": now, "$lte": next_week}
}))

for ret_assignment in upcoming_assignments:
    print(ret_assignment)




#Count total enrollment per course
pipeline = [
    {
        "$group": {
            "_id": "$course_id",
            "total_enrollments": {"$sum": 1}
        }
    },
    {
        "$lookup": {
            "from": "courses",
            "localField": "_id",
            "foreignField": "_id",
            "as": "course_info"
        }
    },
    {
        "$unwind": "$course_info"
    },
    {
        "$project": {
            "course_name": "$course_info.name",
            "total_enrollments": 1
        }
    }
]

result = list(db.enrollments.aggregate(pipeline))
for doc in result:
    print(doc)





#Calculate average course rating
pipeline = [
    {
        "$project": {
            "name": 1,
            "average_rating": {"$avg": "$ratings"}
        }
    }
]

result = list(db.courses.aggregate(pipeline))
for doc in result:
    print(doc)



#Group by course category
pipeline = [
    {
        "$group": {
            "_id": "$category",
            "courses": {"$push": "$name"},
            "count": {"$sum": 1}
        }
    },
    {
        "$project": {
            "category": "$_id",
            "courses": 1,
            "count": 1,
            "_id": 0
        }
    }
]

result = list(db.courses.aggregate(pipeline))
for doc in result:
    print(doc)



#Average grade per student 
pipeline = [
    {
        "$group": {
            "_id": "$student_id",
            "average_grade": {"$avg": "$grade"}
        }
    },
    {
        "$lookup": {
            "from": "users",
            "localField": "_id",
            "foreignField": "_id",
            "as": "student_info"
        }
    },
    {
        "$unwind": "$student_info"
    },
    {
        "$project": {
            "student_name": "$student_info.name",
            "average_grade": 1
        }
    }
]

result = list(db.submissions.aggregate(pipeline))
for doc in result:
    print(doc)



#Completion rate by courses
pipeline = [
    {
        "$lookup": {
            "from": "assignments",
            "localField": "assignment_id",
            "foreignField": "_id",
            "as": "assignment_info"
        }
    },
    {
        "$unwind": "$assignment_info"
    },
    {
        "$group": {
            "_id": "$assignment_info.course_id",
            "total_submissions": {"$sum": 1},
            "unique_students": {"$addToSet": "$student_id"},
            "total_assignments": {"$addToSet": "$assignment_info._id"}
        }
    },
    {
        "$project": {
            "course_id": "$_id",
            "num_students": {"$size": "$unique_students"},
            "num_assignments": {"$size": "$total_assignments"},
            "total_submissions": 1,
            "completion_rate": {
                "$divide": [
                    "$total_submissions",
                    {"$multiply": [{"$size": "$unique_students"}, {"$size": "$total_assignments"}]}
                ]
            }
        }
    }
]

comp_result = list(db.assignments.aggregate(pipeline))
for doc in result:
    print(doc)



#Top performing student
pipeline = [
    {
        "$lookup": {
            "from": "courses",
            "localField": "courseId",
            "foreignField": "_id",
            "as": "course"
        }
    },
    {
        "$unwind": "$course"
    },
    {
        "$group": {
            "_id": "$course.instructorId",
            "students": { "$addToSet": "$studentId" },
            "totalRevenue": { "$sum": "$pricePaid" },
            "courseIds": { "$addToSet": "$course._id" }
        }
    },
    {
        "$project": {
            "instructorId": "$_id",
            "totalStudents": { "$size": "$students" },
            "totalRevenue": 1,
            "courseIds": 1,
            "_id": 0
        }
    },
    {
        "$lookup": {
            "from": "courses",
            "localField": "courseIds",
            "foreignField": "_id",
            "as": "courses"
        }
    },
    {
        "$addFields": {
            "avgRating": { "$avg": "$courses.averageRating" }
        }
    },
    {
        "$project": {
            "instructorId": 1,
            "totalStudents": 1,
            "totalRevenue": 1,
            "avgRating": 1
        }
    }
]

# Run the aggregation
results = db.enrollments.aggregate(pipeline)

# Print results
for doc in results:
    print(doc)




#Total student taught by each instructor


pipeline = [
    {
        "$lookup": {
            "from": "courses",
            "localField": "courseId",
            "foreignField": "_id",
            "as": "lok_course"
        }
    },
    {
        "$unwind": "$lok_course"
    },
    {
        "$group": {
            "_id": "$lok_course.instructorId",
            "students": { "$addToSet": "$studentId" },
            "totalRevenue": { "$sum": "$pricePaid" },
            "courseIds": { "$addToSet": "$course._id" }
        }
    },
    {
        "$project": {
            "instructorId": "$_id",
            "totalStudents": { "$size": "$students" },
            "totalRevenue": 1,
            "courseIds": 1,
            "_id": 0
        }
    },
    {
        "$lookup": {
            "from": "courses",
            "localField": "courseIds",
            "foreignField": "_id",
            "as": "lok_courses"
        }
    },
    {
        "$addFields": {
            "avgRating": { "$avg": "$lok_courses.averageRating" }
        }
    },
    {
        "$project": {
            "instructorId": 1,
            "totalStudents": 1,
            "totalRevenue": 1,
            "avgRating": 1
        }
    }
]

# Run the aggregation
lok_results = db.altcourseschema.aggregate(pipeline)

# Print results
for doc in lok_results:
    print(doc)



#Average course rating per instructor
pipeline = [
    {
        "$group": {
            "_id": "$instructor_id",
            "avgRating": { "$avg": "$rating" }
        }
    },
    {
        "$project": {
            "instructor_id": "$_id",
            "avgRating": { "$round": ["$avgRating", 2] },
            "_id": 0
        }
    }
]

results = db.courses.aggregate(pipeline)

for doc in results:
    print(doc)



#Revenue generated per instructor
pipeline = [
    {
        "$lookup": {
            "from": "courses",
            "localField": "course_id",       # Matches enrollment.course_id
            "foreignField": "_id",           # Matches course._id
            "as": "course"
        }
    },
    {
        "$unwind": "$course"
    },
    {
        "$group": {
            "_id": "$course.instructor_id",
            "revenue": { "$sum": "$course.price" }
        }
    },
    {
        "$project": {
            "instructor_id": "$_id",
            "revenue": 1,
            "_id": 0
        }
    }
]

results = db.enrollments.aggregate(pipeline)

for doc in results:
    print(doc)




#Monthly enrollment trends
pipeline = [
    {
        "$group": {
            "_id": {
                "year": { "$year": "$enrolled_at" },
                "month": { "$month": "$enrolled_at" }
            },
            "totalEnrollments": { "$sum": 1 }
        }
    },
    {
        "$sort": {
            "_id.year": 1,
            "_id.month": 1
        }
    }
]

results = db.enrollments.aggregate(pipeline)

for doc in results:
    print(doc)




#Most popular course categories


pipeline = [
    {
        "$lookup": {
            "from": "courses",
            "localField": "course_id",        # or "courseId", if that's your field
            "foreignField": "_id",
            "as": "course"
        }
    },
    {
        "$unwind": "$course"
    },
    {
        "$group": {
            "_id": "$course.category",
            "enrollments": { "$sum": 1 }
        }
    },
    {
        "$sort": { "enrollments": -1 }
    },
    {
        "$limit": 5
    }
]

results = db.enrollments.aggregate(pipeline)

for doc in results:
    print(doc)




#Student engagement metrics


pipeline = [
    {
        "$group": {
            "_id": "$student_id",
            "submissionsCount": { "$sum": 1 }
        }
    },
    {
        "$group": {
            "_id": None,
            "avgSubmissionsPerStudent": { "$avg": "$submissionsCount" }
        }
    },
    {
        "$project": {
            "_id": 0,
            "avgSubmissionsPerStudent": 1
        }
    }
]

results = db.submissions.aggregate(pipeline)

for doc in results:
    print(doc)




#Extras
#Active vs inactive
now = datetime.utcnow()  # Current datetime to compare against

pipeline = [
    {
        "$group": {
            "_id": "$student_id",
            "lastActivity": { "$max": "$submitted_at" }
        }
    },
    {
        "$project": {
            "daysSinceLastActivity": {
                "$divide": [
                    { "$subtract": [now, "$lastActivity"] },
                    1000 * 60 * 60 * 24  # ms to days
                ]
            }
        }
    },
    {
        "$group": {
            "_id": {
                "isActive": { "$lt": ["$daysSinceLastActivity", 30] }
            },
            "count": { "$sum": 1 }
        }
    },
    {
        "$project": {
            "_id": 0,
            "status": {
                "$cond": {
                    "if": "$_id.isActive",
                    "then": "Active",
                    "else": "Inactive"
                }
            },
            "count": 1
        }
    }
]

results = db.submissions.aggregate(pipeline)

for doc in results:
    print(doc)



#User email lookup
db.users.create_index(
    [("email", 1)],
    unique=True
)




#Courses search by title and category
db.courses.create_index([
    ("title", 1),
    ("category", 1)
])



#Assignment queries by due date
db.assignments.create_index(
    [("due_date", 1)]
)



#Enrollemt queries by student and courses

db.enrollments.create_index([
    ("student_id", 1),
    ("course_id", 1)
])



#Analyze query performance using explain() method in PyMongo
from pprint import pprint
query = { "email": "john@example.com" }

# Use explain to analyze the query execution
explain_result = db.users.find(query).explain()

# Pretty print the output
pprint(explain_result)





#Query 1: Find User by Email (Slow without Index)

db.users.find_one({"email": "john@example.com"})
#Result
db.users.create_index([("email", 1)], unique=True)




#Query 2 :Search Courses by Title and Category

query2 = { "title": "Intro to Python", "category": "Programming" }
#optimization
db.courses.create_index([("title", 1), ("category", 1)])



#Query 3: Filter Assignments by Due Date

db.assignments.find({"due_date": {"$lt": datetime(2025, 7, 1)}})
#Fixing
db.assignments.create_index([("due_date", 1)])




#Document the performance improvements using python timing functions
import time

start = time.time()
list(db.assignments.find({"due_date": {"$lt": datetime(2025, 7, 1)}}))
end = time.time()

print(f"Query took: {end - start:.4f} seconds")



#Duplicate key error

from pymongo import MongoClient, errors 

users = db.users
try:
    users.insert_one({
        "name": "John Doe",
        "email": "john@example.com",  # already exists
        "role": "student",
        "created_at": datetime.utcnow()
    })
except errors.DuplicateKeyError:
    print("Error: Email already exists.")



users = db.users
try:
    users.insert_one({
        "name": "Alice",
        "email": "alice@example.com",
        "role": "instructor",
        "created_at": "2025-06-10"  # should be a datetime object
    })
except errors.WriteError as e:
    print(f"Data type error: {e}")



#missing required fields
users = db.users

try:
    users.insert_one({
        "name": "Missing Email"
        # email, role, created_at are missing
    })
except errors.WriteError as e:
    print(f"Missing required field: {e}")