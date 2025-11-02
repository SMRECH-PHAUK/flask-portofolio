erDiagram
    Student ||--o{ Enrollment : enrolls
    Student ||--o{ TuitionPayment : pays
    Professor ||--o{ Course : teaches
    Course ||--o{ Enrollment : has
    Course ||--o{ TuitionPayment : for

    Student {
        string id PK
        string name
        string email UK
        string major
    }

    Professor {
        string id PK
        string name
        string email UK
        string department
    }

    Course {
        int id PK
        string name
        string code UK
        int credits
        string professor_id FK
    }

    Enrollment {
        int id PK
        string student_id FK
        int course_id FK
        string grade
    }

    TuitionPayment {
        int id PK
        string student_id FK
        int course_id FK
        float amount_paid
        datetime payment_date
        string status
    }