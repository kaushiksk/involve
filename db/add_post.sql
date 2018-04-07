DELIMITER //

CREATE PROCEDURE add_transaction
( 
    IN in_tid VARCHAR(200),
    IN in_cid INT 
)
BEGIN
    
    INSERT INTO transactions
    (
       t_id,
       counter
    ) 
    VALUES
    (
       c_url,
       c_title,
       c_description,
       c_thumb,
       0
    );
END//

DELIMITER ;
