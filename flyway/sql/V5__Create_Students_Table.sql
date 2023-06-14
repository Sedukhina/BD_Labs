BEGIN;
    CREATE TABLE IF NOT EXISTS Students(Student_ID SERIAL, OUTID VARCHAR, Birth INT, YEAR INT, Territory_ID INT, Registration_Type INT, class_profile INT, class_language INT, sex_type INT, eo_id INT); 
    INSERT INTO Students(OUTID, Birth, YEAR, Territory_ID, Registration_Type, class_profile, class_language, sex_type, eo_id)  SELECT DISTINCT OUTID, Birth, Year, Territory_ID, Registration_Type, class_profile, class_language, sex_type, eo_id FROM Odata;
    ALTER TABLE Odata ADD Student_ID INT;
    UPDATE Odata SET Student_ID = Students.Student_ID FROM Students WHERE Odata.outid = Students.outid;
    ALTER TABLE Odata DROP COLUMN OUTID, DROP COLUMN Birth, DROP COLUMN Territory_ID, DROP COLUMN Registration_Type, DROP COLUMN class_profile, DROP COLUMN class_language, DROP COLUMN sex_type, DROP COLUMN eo_id;
COMMIT;
