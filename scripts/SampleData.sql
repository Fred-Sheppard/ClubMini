-- -- INSERT statements with at least 3 samples
INSERT INTO app_roles (name)
VALUES ('Coordinator'),
       ('Student');

INSERT INTO app_users (role_id, name, email, password, contact_details)
VALUES (1, 'Admin', 'admin@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+1234567890'),

       (1, 'John Doe', 'john.doe@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+1987654321'),

       (2, 'Jane Smith', 'jane.smith@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+1555123456'),

       (1, 'Mary Jones', 'mary.jones@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+12223334444'),

       (2, 'Alice Johnson', 'alice.johnson@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+18887776666'),

       (2, 'Bob Williams', 'bob.williams@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+14443332222'),

       (2, 'Emily Brown', 'emily.brown@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+16667778888'),

       (1, 'Michael Wilson', 'michael.wilson@example.com',
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+19998887777');

INSERT INTO app_accountrequests (name, email, role_id, password, contact_details)
VALUES ('Jeremy', 'new_coordinator@example.com', 1,
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+19998887777'),
       ('Niall', 'some_student@example.com', 2,
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+16667778888'),
       ('Jack','new_student@example.com', 2,
        'pbkdf2_sha256$720000$D6bRqUkBTWMkIc4kMD7jmT$BtAI4S+jmOhlsFR+ADbbZS3ul1Rq5tqRLPURV5VuIJc=',
        '+14443332222');

INSERT
INTO app_clubs (club_id, name, description, accepting_members, image)
VALUES (2, 'Coding Club', 'Learn and share your coding skills', TRUE),
       (4, 'Photography Club', 'Capture the world through your lens', FALSE),
       (8, 'Weightlifting Club', 'Train and compete in SBD and Olympic Lifts', TRUE, https://www.garage-gyms.com/wp-content/uploads/2014/11/dmitry-klokov-barbell.jpg);

INSERT INTO app_clubmembers (user_id, club_id)
VALUES (3, 2),
       (5, 4),
       (6, 8);

INSERT INTO app_clubrequests (user_id, club_id)
VALUES (7, 2),
       (8, 1);

INSERT INTO app_events (title, description, club_id, event_time, venue)
VALUES ('Intro to Python', 'Learn the basics of Python programming', 2, '2024-03-02 18:00:00', 'Room 201'),
       ('Photo Walk in the Park', 'Capture the beauty of nature', 4, '2024-03-10 10:00:00',
        'Meet at Main Park Entrance'),
       ('Book Club Meeting', 'Discuss the latest bestseller', 8, '2024-03-15 19:00:00', 'Library Auditorium');

INSERT INTO app_eventrequests (user_id, event_id)
VALUES (6, 1),
       (7, 3),
       (3, 2);