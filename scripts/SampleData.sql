-- -- INSERT statements with at least 3 samples
INSERT INTO app_roles (name, date_inserted, date_updated)
VALUES ('Coordinator', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
       ('Student', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_users (role_id, name, email, password, contact_details, date_inserted, date_updated)
VALUES (1, 'Admin', 'admin@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+1234567890', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

       (1, 'John Doe', 'john.doe@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+1987654321', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

       (2, 'Jane Smith', 'jane.smith@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+1555123456', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

       (1, 'Mary Jones', 'mary.jones@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+12223334444', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

       (2, 'Alice Johnson', 'alice.johnson@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+18887776666', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

       (2, 'Bob Williams', 'bob.williams@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+14443332222', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

       (2, 'Emily Brown', 'emily.brown@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+16667778888', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

       (1, 'Michael Wilson', 'michael.wilson@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+19998887777', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_accountrequests (name, email, role_id, password, contact_details, date_inserted, date_updated)
VALUES ('Jeremy', 'new_coordinator@example.com', 1,
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+19998887777', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
       ('Niall', 'some_student@example.com', 2,
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+16667778888', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
       ('Jack', 'new_student@example.com', 2,
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+14443332222', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_clubs (club_id, name, description, image, accepting_members, date_inserted, date_updated)
VALUES (2, 'Coding Club',
        'Welcome to our Coding Club, where creativity meets technology! Whether youre a beginner or an experienced coder our inclusive community fosters collaboration and learning.',
        'https://cdn-wordpress-info.futurelearn.com/wp-content/uploads/Coding_Blog_Header_1500x750.jpg.optimal.jpg',
        TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
       (4, 'Photography Club',
        'Step into the captivating world of photography with our club! Discover the artistry behind the lens as we explore techniques, styles, and visual storytelling together.',
        'https://petapixel.com/assets/uploads/2022/05/photographers-with-cameras-800x420.jpg', FALSE, CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP),
       (8, 'Book Club',
        'Welcome to our Book Club, where pages come alive with discussion and discovery! Dive into captivating stories, explore diverse genres, and share your literary insights in a welcoming environment.',
        'https://www.thegoodbook.co.uk/downloads/bookclub.jpg', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_clubmembers (user_id, club_id, date_inserted, date_updated)
VALUES (3, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
       (5, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
       (6, 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_clubrequests (user_id, club_id, date_inserted, date_updated)
VALUES (7, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
       (8, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_events (title, description, club_id, event_time, venue, date_inserted, date_updated)
VALUES ('Intro to Python', 'Learn the basics of Python programming', 2, '2024-03-02 18:00:00', 'Room 201',
        CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
       ('Photo Walk in the Park', 'Capture the beauty of nature', 4, '2024-03-10 10:00:00',
        'Meet at Main Park Entrance', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
       ('Book Club Meeting', 'Discuss the latest bestseller', 8, '2024-03-15 19:00:00', 'Library Auditorium',
        CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_eventrequests (user_id, event_id, date_inserted, date_updated)
VALUES (6, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
       (7, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
       (3, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);