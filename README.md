## mongodb-eduhub-project
A MongoDB-based analytics project for managing and analyzing online education platform data using PyMongo.


#### Project Setup Instructions
1. Install MongoDB  
   - Download and install MongoDB Community Edition from [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)  
     
2. Set Up the Database  
   - Open MongoDB Compass or connect via Mongo shell  
   - Create a database named: eduhub_db  
   - Import the collections: users, courses, enrollments, lessons, assignments, submissions, etc.  
   - You can import sample data using Compass or mongoimport command.

3. Set Up Your Python Environment  
   - Create a virtual environment (optional but recommended):  
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate 
   - Install dependencies:  
     pip install pymongo
     
4. Open and Run Code in VSCode or Jupyter Notebook  
   - Open eduhub_queries.py (or your Jupyter notebook version)
   - Make sure your MongoDB server is running
   - Run each section to:
     - Create indexes
     - Perform aggregations
     - Handle errors
     - Analyze performance

5. (Optional) Use Jupyter Notebook  
   - Launch Jupyter in VSCode:


  
#### Database Schema Documentation
It uses a document-based schema in MongoDB to manage educational content and interactions between students and instructors.


####altuserschema collection
Stores both students and instructors.

```json

user_schema = {
    “_id”: “ObjectId (auto-generated)”,
    “userId”: “string (unique)”,
    “email”: “string (unique, required)”,
    “firstName”: “string (required)”,
    “lastName”: “string (required)”,
    “role”: “string (enum: [‘student’, ‘instructor’])”,
    “dateJoined”: “datetime”,
    “profile”: {
        “bio”: “string”,
        “avatar”: “string”,
        “skills”: [“string”]
    },
    “isActive”: “boolean”
}



### altcourseschema collection

course_schema = {
    “_id”: “ObjectId (auto-generated)”,
    “courseId”: “string (unique)”,
    “title”: “string (required)”,
    “description”: “string”,
    “instructorId”: “string (reference to users)”,
    “category”: “string”,
    “level”: “string (enum: [‘beginner’, ‘intermediate’, ‘advanced’])”,
    “duration”: “number (in hours)”,
    “price”: “number”,
    “tags”: [“string”],
    “createdAt”: “datetime”,
    “updatedAt”: “datetime”,
    “isPublished”: “boolean”


#### Query Explanations

This section explains key MongoDB queries used in the project and their purpose.
1. User Email Lookup
db.users.find_one({"email": "john@example.com"})

Purpose: Quickly find a user by their email.  
Optimization: Indexed the email field to ensure fast lookups.


2. Search Courses by Title and Category
db.courses.find({"title": "Python Basics", "category": "Programming"})

Purpose: Allows users to search for courses based on their title and category.  
Optimization: Compound index on title and category.

3. Find Assignments by Due Date
db.assignments.find({"due_date": {"$lt": ISODate("2025-07-01")}})

Purpose: Retrieve upcoming or overdue assignments.  
Optimization: Index on due_date to speed up range queries.

4. Total Students per Instructor
Aggregation to count unique students per instructor

Purpose: Measure reach of each instructor's courses.  
Method: Join enrollments and courses, then group by instructor_id.


5. Revenue Per Instructor
Aggregation summing up price paid for all enrollments

Purpose: Calculate total earnings for each instructor.  
Method: Join enrollments with courses, then sum pricePaid.


6. Monthly Enrollment Trends
Group by year and month from enrollment date

Purpose: Visualize enrollment activity over time.  
Method: $year, $month, and $group aggregation.


7. Most Popular Course Categories
Group enrollments by course category and sort by count

Purpose: Identify top-performing course categories.


8. Student Engagement
Average number of submissions per student

Purpose: Track how actively students participate in assignments.


9. Lesson Completion Rate
Group completions by student

Purpose: Understand how many lessons students are finishing.


10. Active vs Inactive Students
Based on days since last submission

Purpose: Distinguish engaged students from inactive ones using activity timestamps.

---

Each query is optimized for performance with proper indexing and structured aggregation. These operations power the analytics dashboard and ensure smooth data access for both users and instructors.






#### Performance Analysis Results

Query 1: Find User by Email

Before Optimization:
- No index on the email field
- Full collection scan (COLLSCAN) observed using .explain()
- Slow response time when collection grew large

Optimization Applied:
```python
db.users.create_index([("email", 1)], unique=True)

After optimization 

• IXSCAN used instead of COLLSCAN
 • Query time reduced significantly



Query 2: Search Courses by Title and Category

Before Optimization
db.courses.find({"title": "Mongo Basics", "category": "Database"})

After Optimization
db.courses.create_index([("title", 1), ("category", 1)])

Result:
 • Query performance improved
 • Execution plan shows efficient use of compound index


Query 3: Filter Assignments by Due Date

Before Optimization
db.assignments.find({"due_date": {"$lt": datetime(2025, 7, 1)}})

After Optimization
db.assignments.create_index([("due_date", 1)])

Result:
 • Better response time for due-date range filters
 • Suitable for dashboards and deadline-based alerts


Performance Measurement Method
 • Used .explain() in PyMongo to analyze query plans
 • Used Python time module to measure response times

import time
start = time.time()
db.users.find_one({"email": "john@example.com"})
end = time.time()
print("Query time:", end - start, "seconds")


Conclusion:
Adding indexes drastically improved query speed and reduced system load. Each index was tied to actual query patterns for efficiency.





#### Challenges Faced & Solutions

1. Data Consistency Between Collections
- Challenge: Ensuring relationships (like student–enrollment–course–assignment) remained valid across multiple collections.
- Solution:  
  - Used consistent _id references between collections.
  - Enforced schema design where student_id, course_id, etc. were clearly linked to users, courses.

2. Handling Duplicate Entries
- Challenge: Inserting users with existing emails caused DuplicateKeyError.
- Solution:  
  - Created unique index on email field.  
  - Used try...except blocks in Python to catch and handle the error gracefully.

3. Data Validation Issues
- Challenge: Accidental insertion of wrong data types (e.g., string instead of `datetime`) or missing required fields.
- Solution:  
  - Defined strict schema validation rules for each collection.  
  - Handled errors with pymongo.errors.WriteError.

4. Slow Query Performance
- Challenge: Queries became slower as data volume increased.
- Solution:  
  - Used .explain() to identify performance bottlenecks.  
  - Created indexes on email, due_date, title, category, student_id and course_id to speed up queries.

5. Understanding Aggregation Pipelines
- Challenge: Writing correct and efficient $lookup, $group, and $project stages in aggregation pipelines.
- Solution:  
  - Broke down complex queries into steps.  
  - Tested each stage incrementally using MongoDB Compass and Jupyter Notebook.

6. Exporting Results for Documentation
- Challenge: MongoDB Compass does not easily export full query results in desired format.
- Solution:  
  - Used PyMongo in Python to fetch and export data.  
  - Documented outputs clearly in .md files and Python scripts.

7. Working in Jupyter Notebook (VSCode)
- Challenge: Display formatting (markdown, bold text, font sizes) wasn't intuitive.
- Solution:  
  - Used Markdown cells for explanations.  
  - Used HTML tags where needed to adjust text formatting.
