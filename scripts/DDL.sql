-- roles
CREATE TABLE roles
(
    role_id       INTEGER PRIMARY KEY NOT NULL,
    name          VARCHAR(31)         NOT NULL,
    date_inserted DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- users
CREATE TABLE users
(
    user_id         INTEGER PRIMARY KEY NOT NULL,
    role            INTEGER             NOT NULL,
    name            VARCHAR(31)         NOT NULL,
    email           VARCHAR(31)         NOT NULL,
    password        CHAR(256)           NOT NULL,
    contact_details VARCHAR(1023),
    date_inserted   DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated    DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role) REFERENCES roles (role_id)
);

-- account_requests
CREATE TABLE account_requests
(
    a_request_id  INTEGER PRIMARY KEY NOT NULL,
    email         VARCHAR(31) UNIQUE  NOT NULL,
    role_id       INT                 NOT NULL,
    date_inserted DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles (role_id)
);

-- clubs
CREATE TABLE clubs
(
    club_id           INTEGER PRIMARY KEY NOT NULL,
    name              VARCHAR(31)         NOT NULL,
    description       VARCHAR(1023)       NOT NULL,
    accepting_members BOOLEAN             NOT NULL,
    image             BLOB,
    date_inserted     DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id) REFERENCES users (user_id)
);

-- club_members
CREATE TABLE club_members
(
    user_id       integer not null,
    club_id       integer not null,
    date_inserted DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated  DATETIME DEFAULT CURRENT_TIMESTAMP,
    foreign key (user_id) references users (user_id) on delete cascade,
    foreign key (club_id) references clubs (club_id) on delete cascade
);

-- club_requests
CREATE TABLE club_requests
(
    user_id       integer not null,
    club_id       integer not null,
    date_inserted DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated  DATETIME DEFAULT CURRENT_TIMESTAMP,
    foreign key (user_id) references users (user_id) on delete cascade,
    foreign key (club_id) references clubs (club_id) on delete cascade
);

-- events
CREATE TABLE events
(
    event_id      INTEGER PRIMARY KEY AUTOINCREMENT not null,
    title         VARCHAR(31)                       NOT NULL,
    description   VARCHAR(1023),
    club_id       INTEGER                           NOT NULL,
    event_time    CHAR(23)                          not null,
    venue         VARCHAR(63)                       not null,
    date_inserted DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id) REFERENCES clubs (club_id)
);

-- event_requests
CREATE TABLE event_requests
(
    event_id      INTEGER NOT NULL,
    user_id       INTEGER NOT NULL,
    date_inserted DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_updated  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

-- CREATE view coordinators as
-- select users.*, c.name as "club_name"
-- from users
--          join clubs c on users.user_id = c.club_id;
--
-- CREATE VIEW students AS
-- SELECT *
-- FROM users
-- WHERE user_id NOT IN (SELECT user_id FROM coordinators);
--
