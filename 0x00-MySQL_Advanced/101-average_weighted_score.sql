-- A SQL script that Create a stored procedure `ComputeAverageWeightedScoreForUsers` that 
-- computes and stores the average weighted score for all students

delimiter $$
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
-- Update the users table with the computed average weighted scores
 UPDATE users AS u
    JOIN (
        -- Subquery to calculate the weighted average score for each user
        SELECT 
            u.id AS user_id, 
            SUM(c.score * p.weight) / SUM(p.weight) AS weight_avg
        FROM 
            users AS u
        JOIN 
            corrections AS c ON u.id = c.user_id
        JOIN 
            projects AS p ON c.project_id = p.id
        GROUP BY 
            u.id
    ) AS weighted_scores
    ON u.id = weighted_scores.user_id
    SET u.average_score = weighted_scores.weight_avg;

END;$$
delimiter
;