-- JOIN: Show tickets with employee and assigned engineer details
SELECT
    t.id AS ticket_id,
    t.title,
    t.status,
    t.priority,
    e.name AS employee_name,
    en.name AS engineer_name
FROM tickets t
JOIN employees e ON t.employee_id = e.id
LEFT JOIN engineers en ON t.engineer_id = en.id
ORDER BY t.id;


-- CTE: Count tickets by employee
WITH employee_ticket_counts AS (
    SELECT
        employee_id,
        COUNT(*) AS ticket_count
    FROM tickets
    GROUP BY employee_id
)
SELECT
    e.id,
    e.name,
    etc.ticket_count
FROM employee_ticket_counts etc
JOIN employees e ON etc.employee_id = e.id
ORDER BY etc.ticket_count DESC;


-- Window Function: Rank tickets by priority for each employee
SELECT
    t.id,
    t.employee_id,
    t.title,
    t.priority,
    ROW_NUMBER() OVER (
        PARTITION BY t.employee_id
        ORDER BY
            CASE t.priority
                WHEN 'HIGH' THEN 1
                WHEN 'MEDIUM' THEN 2
                WHEN 'LOW' THEN 3
                ELSE 4
            END,
            t.created_at
    ) AS ticket_rank
FROM tickets t;


-- Transaction: Assign an engineer and update ticket status atomically
BEGIN;

UPDATE tickets
SET
    engineer_id = 1,
    status = 'ASSIGNED',
    updated_at = CURRENT_TIMESTAMP
WHERE id = 1;

INSERT INTO ticket_updates (
    ticket_id,
    engineer_id,
    comment,
    old_status,
    new_status
)
VALUES (
    1,
    1,
    'Ticket assigned to engineer',
    'OPEN',
    'ASSIGNED'
);

COMMIT;