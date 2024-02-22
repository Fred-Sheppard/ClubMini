-- -- INSERT statements with at least 3 samples
INSERT INTO app_roles (name)
VALUES ('Coordinator'),
       ('Student');

INSERT INTO app_users (role_id, name, email, password)
VALUES (1, 'John Doe', 'john.doe@example.com', 'hashed_password'),
       (2, 'Jane Smith', 'jane.smith@example.com', 'hashed_password'),
       (1, 'Mary Jones', 'mary.jones@example.com', 'hashed_password');

INSERT INTO app_accountrequests (email, role_id)
VALUES ('new_coordinator@example.com', 1),
       ('new_admin@example.com', 1),
       ('new_student@example.com', 2);

INSERT INTO app_clubs (club_id, name, description, accepting_members)
VALUES (1, 'Coding Club', 'Learn and share your coding skills', TRUE),
       (2, 'Photography Club', 'Capture the world through your lens', FALSE),
       (3, 'Book Club', 'Discuss and analyze your favorite books', TRUE);

INSERT INTO app_clubmembers (user_id, club_id)
VALUES (2, 1),
       (3, 2),
       (1, 3);

INSERT INTO app_clubrequests (user_id, club_id)
VALUES (1, 2),
       (2, 3),
       (3, 1);

INSERT INTO app_events (title, description, club_id, event_time, venue)
VALUES ('Intro to Python', 'Learn the basics of Python programming', 1, '2024-03-02 18:00:00', 'Room 201'),
       ('Photo Walk in the Park', 'Capture the beauty of nature', 2, '2024-03-10 10:00:00',
        'Meet at Main Park Entrance'),
       ('Book Club Meeting', 'Discuss the latest bestseller', 3, '2024-03-15 19:00:00', 'Library Auditorium');

INSERT INTO app_eventrequests (event_id, user_id)
VALUES (1, 2),
       (2, 3),
       (3, 1);

-- CREATE views (if needed)
-- CREATE VIEW coordinators AS
-- ...

-- CREATE VIEW students AS
-- ...
