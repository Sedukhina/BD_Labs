BEGIN;
    CREATE TABLE IF NOT EXISTS Registration_Types(Type_ID SERIAL, Type_Name VARCHAR);
    INSERT INTO Registration_Types(Type_Name) SELECT DISTINCT regtypename FROM Odata;
    ALTER TABLE Odata ADD COLUMN Registration_Type INT;
    UPDATE Odata SET Registration_Type = Registration_Types.Type_ID FROM Registration_Types WHERE Odata.regtypename = Registration_Types.Type_Name;
    ALTER TABLE Odata DROP COLUMN regtypename;
COMMIT;

BEGIN;
    CREATE TABLE IF NOT EXISTS Class_Profiles(Profile_ID SERIAL, Profile_name VARCHAR);
    INSERT INTO Class_Profiles(Profile_name) SELECT DISTINCT classprofilename FROM odata;
    ALTER TABLE Odata ADD COLUMN Class_Profile INT;
    UPDATE Odata SET Class_Profile = Class_Profiles.Profile_ID FROM Class_Profiles WHERE Odata.classprofilename =  Class_Profiles.Profile_name;
    ALTER TABLE Odata DROP COLUMN classprofilename;

    CREATE TABLE IF NOT EXISTS Class_Languages(Lang_ID SERIAL, Language VARCHAR);
    INSERT INTO Class_Languages(Language) SELECT DISTINCT classlangname FROM odata;
    ALTER TABLE Odata ADD COLUMN Class_Language INT;
    UPDATE Odata SET Class_Language = Class_Languages.Lang_ID FROM Class_Languages WHERE Odata.classlangname =  Class_Languages.Language;
    ALTER TABLE Odata DROP COLUMN classlangname;

    CREATE TABLE IF NOT EXISTS Sex_Types(Type_ID SERIAL, Sex_Type VARCHAR);
    INSERT INTO Sex_Types(Sex_Type) SELECT DISTINCT sextypename FROM odata;
    ALTER TABLE Odata ADD COLUMN Sex_Type INT;
    UPDATE Odata SET Sex_Type = Sex_Types.Type_ID FROM Sex_Types WHERE Odata.sextypename =  Sex_Types.Sex_Type;
    ALTER TABLE Odata DROP COLUMN sextypename;
COMMIT;

