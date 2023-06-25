BEGIN;
    CREATE TABLE IF NOT EXISTS Test_Statuses(Status_ID SERIAL, Status VARCHAR);
    INSERT INTO Test_Statuses(Status) SELECT DISTINCT status FROM Test_Results;
    ALTER TABLE Test_Results ADD COLUMN STATUS_ID INT;
    UPDATE Test_Results SET STATUS_ID = Test_Statuses.Status_ID FROM Test_Statuses WHERE Test_Results.status = Test_Statuses.Status;
    ALTER TABLE Test_Results DROP COLUMN STATUS;

    CREATE TABLE IF NOT EXISTS Subjects(Subject_ID SERIAL, Subject VARCHAR);
    INSERT INTO Subjects(Subject) SELECT DISTINCT Subject FROM Test_Results;
    ALTER TABLE Test_Results ADD COLUMN Subject_ID INT;
    UPDATE Test_Results SET Subject_ID = Subjects.Subject_ID FROM Subjects WHERE Test_Results.Subject = Subjects.Subject;
    ALTER TABLE Test_Results DROP COLUMN Subject;

    ALTER TABLE Test_Results ADD COLUMN Language_id INT;
    UPDATE Test_Results SET Language_id = Class_Languages.Lang_ID FROM Class_Languages WHERE Test_Results.lang = Class_Languages.Language;
    ALTER TABLE Test_Results DROP COLUMN lang;

    ALTER TABLE Test_Results ADD COLUMN EO_TERRITORY_ID INT;
    UPDATE Test_Results SET EO_TERRITORY_ID = TERRITORIES.TERRITORY_ID FROM TERRITORIES INNER JOIN AREAS ON TERRITORIES.AREA_ID = AREAS.AREA_ID INNER JOIN REGIONS ON AREAS.Region_ID = Regions.Region_ID WHERE Test_Results.EO = TERRITORIES.TERRITORY_NAME AND Test_Results.EO_REG = REGNAME;
    ALTER TABLE Test_Results DROP COLUMN EO_AREA,  DROP COLUMN EO_REG,  DROP COLUMN EO_TER;

    ALTER TABLE Test_Results ADD COLUMN EO_ID INT;
    INSERT INTO Educational_Organizations(Name, Territory_ID) SELECT DISTINCT EO, EO_TERRITORY_ID from Test_Results WHERE EO IS NOT NULL ON CONFLICT do nothing;
    UPDATE Test_Results SET EO_ID = Educational_Organizations.EO_ID FROM Educational_Organizations WHERE Test_Results.EO = Educational_Organizations.Name AND Test_Results.EO IS NOT NULL;
    ALTER TABLE Test_Results DROP COLUMN EO, DROP COLUMN EO_TERRITORY_ID;

    DROP TABLE Odata;
COMMIT;
