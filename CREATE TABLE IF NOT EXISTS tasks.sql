CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done INTEGER DEFAULT 0
);

SELECT * FROM tasks;
SELECT * FROM tasks WHERE done = 0;
SELECT COUNT(*) FROM tasks WHERE done = 0;

INSERT INTO tasks (title) VALUES ('Coding session');

DELETE FROM tasks WHERE id = 1;

SELECT done FROM tasks WHERE id = 1;

UPDATE tasks SET done = 1 WHERE id = 1;

UPDATE tasks SET done = 1 - done WHERE id = 1;