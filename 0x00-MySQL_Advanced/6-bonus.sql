-- script that creates a stored procedure AddBonus that adds a new correction for a student
DELIMITER |
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
	SET @id = (SELECT id FROM projects WHERE name = project_name);
	IF @id IS NULL THEN
		INSERT INTO projects (name) VALUES(project_name);
		SET @id = LAST_INSERT_ID();
	END IF;
	INSERT INTO corrections(user_id, project_id, score) VALUES (user_id, @id, score);
END;
|
DELIMITER ;