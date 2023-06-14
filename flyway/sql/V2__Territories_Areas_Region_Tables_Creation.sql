BEGIN;
    CREATE TABLE IF NOT EXISTS Regions(Region_ID SERIAL, REGNAME VARCHAR); 
    INSERT INTO Regions(REGNAME) SELECT DISTINCT REGNAME FROM Odata;
    ALTER TABLE Odata ADD Region_ID INT;
    UPDATE Odata SET Region_ID = Regions.Region_ID FROM Regions WHERE Odata.REGNAME = Regions.REGNAME ;
    ALTER TABLE Odata DROP COLUMN REGNAME;

    ALTER TABLE Odata ADD eo_region_id INT;
    UPDATE Odata SET eo_region_id = Regions.region_id FROM Regions WHERE Odata.eoregname = Regions.regname;
    ALTER TABLE Odata DROP COLUMN eoregname;

    CREATE TABLE IF NOT EXISTS Areas(Area_ID SERIAL, AreaName VARCHAR, Region_ID INT); 
    INSERT INTO Areas(AREANAME, Region_ID) SELECT DISTINCT AREANAME, Region_ID FROM Odata;
    ALTER TABLE Odata ADD COLUMN Area_ID INT;
    UPDATE Odata SET Area_ID = Areas.Area_ID FROM Areas WHERE Odata.AreaName = Areas.AreaName AND Odata.Region_ID = Areas.Region_ID;
    ALTER TABLE Odata DROP COLUMN AreaName, DROP COLUMN Region_ID;

    CREATE TABLE IF NOT EXISTS Territories(Territory_ID SERIAL, Territory_Name VARCHAR, Territory_Type VARCHAR, Area_ID INT); 
    INSERT INTO Territories(Territory_Name, Territory_Type, Area_ID) SELECT DISTINCT tername, tertypename, Area_ID FROM Odata;
    ALTER TABLE Odata ADD Territory_ID INT;
    UPDATE Odata SET Territory_ID = Territories.Territory_ID FROM Territories WHERE Odata.tername = Territories.Territory_Name AND Odata.Area_ID = Territories.Area_ID;
    ALTER TABLE Odata DROP COLUMN tername, DROP COLUMN tertypename, DROP COLUMN Area_ID;

    ALTER TABLE Odata ADD COLUMN EO_TERRITORY_ID INT;
    UPDATE Odata SET EO_TERRITORY_ID = TERRITORIES.TERRITORY_ID FROM TERRITORIES INNER JOIN AREAS ON TERRITORIES.AREA_ID = AREAS.AREA_ID WHERE Odata.eotername = TERRITORIES.TERRITORY_NAME AND Odata.eo_region_id = region_id;
    ALTER TABLE Odata DROP COLUMN eotername,  DROP COLUMN eoareaname;

    CREATE TABLE IF NOT EXISTS Territory_Types(Type_ID SERIAL, Type_Name VARCHAR);
    INSERT INTO Territory_Types(Type_Name) SELECT DISTINCT Territory_Type FROM Territories;
    UPDATE Territories SET Territory_Type = Territory_Types.Type_ID FROM Territory_Types WHERE Territories.Territory_Type = Territory_Types.Type_Name;
COMMIT;