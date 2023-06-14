BEGIN;
    CREATE TABLE IF NOT EXISTS EO_Types(Type_ID SERIAL, Type_Name VARCHAR);
    INSERT INTO EO_Types(Type_Name) SELECT DISTINCT eotypename FROM Odata;
    ALTER TABLE Odata ADD COLUMN EO_Type INT;
    UPDATE Odata SET EO_Type = EO_Types.Type_ID FROM EO_Types WHERE Odata.eotypename = EO_Types.Type_Name;
    ALTER TABLE Odata DROP COLUMN eotypename;

    CREATE TABLE IF NOT EXISTS EO_Parents(Parent_ID SERIAL, Parent_Name VARCHAR);
    INSERT INTO EO_Parents(Parent_Name) SELECT DISTINCT eoparent FROM Odata;
    ALTER TABLE Odata ADD COLUMN EO_Parent INT;
    UPDATE Odata SET EO_Parent = EO_Parents.Parent_ID FROM EO_Parents WHERE Odata.eoparent = EO_Parents.Parent_Name;
    ALTER TABLE Odata DROP COLUMN eoparent;

    CREATE TABLE IF NOT EXISTS Educational_Organizations(EO_ID SERIAL, Name VARCHAR UNIQUE, Territory_ID INT, Type INT, Parent INT); 
    INSERT INTO Educational_Organizations(Name, Territory_ID, Type, Parent) SELECT DISTINCT EOName, EO_Territory_ID, EO_Type, EO_Parent FROM Odata ON CONFLICT do nothing;
    ALTER TABLE Odata ADD EO_ID INT;
    UPDATE Odata SET EO_ID = Educational_Organizations.EO_ID FROM Educational_Organizations WHERE Odata.EOName = Educational_Organizations.Name;
    ALTER TABLE Odata DROP COLUMN EO_REGION_ID, DROP COLUMN EO_TERRITORY_ID, DROP COLUMN EO_TYPE, DROP COLUMN EO_PARENT, DROP COLUMN EONAME;
COMMIT;