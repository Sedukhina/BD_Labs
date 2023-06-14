CREATE TABLE IF NOT EXISTS Test_Results(Test_ID SERIAL, Student_ID INT, Subject VARCHAR, Lang VARCHAR, DPA_level VARCHAR, Status VARCHAR, Ball100 Numeric(6,2), Ball12 Numeric(6,2), Ball Numeric(6,2), AdaptScale Numeric(6,2), Subtest bool, EO VARCHAR, EO_Reg VARCHAR,  EO_Area VARCHAR, EO_Ter VARCHAR);

ALTER TABLE Odata ADD COLUMN Ukr_Subtest BOOL;
UPDATE Odata SET Ukr_Subtest = TRUE WHERE ukrsubtest = 'Так';
UPDATE Odata SET Ukr_Subtest = FALSE WHERE ukrsubtest = 'Ні';

INSERT INTO Test_Results(Student_ID, Subject, Status, Ball100, Ball12, Ball, AdaptScale, EO, EO_Reg,  EO_Area, EO_Ter) 
SELECT Student_ID, ukrtest, UKRTestStatus, ukrball100, ukrball12, ukrball, ukrAdaptScale, ukrptName, ukrptRegName, ukrptAreaName, ukrptTerName FROM Odata WHERE ukrtest IS NOT NULL;

INSERT INTO Test_Results(Student_ID, Subject, Status, Ball100, Ball12, Ball, AdaptScale, Subtest, EO, EO_Reg,  EO_Area, EO_Ter) 
SELECT Student_ID, UMLtest, UMLTestStatus, UMLball100, UMLball12, UMLball, UMLAdaptScale, Ukr_Subtest, UMLptName, UMLptRegName, UMLptAreaName, UMLptTerName FROM Odata WHERE UMLtest IS NOT NULL;

INSERT INTO Test_Results(Student_ID, Subject, Status, Ball100, Ball12, Ball, lang, EO, EO_Reg,  EO_Area, EO_Ter) 
SELECT Student_ID, HISTtest, HISTTestStatus, HISTball100, HISTball12, HISTball, HISTlang, HISTptName, HISTptRegName, HISTptAreaName, HISTptTerName FROM Odata WHERE HISTtest IS NOT NULL;

INSERT INTO Test_Results(Student_ID, Subject, Status, Ball100, Ball12, Ball, lang, EO, EO_Reg,  EO_Area, EO_Ter) 
SELECT Student_ID, MATHtest, MATHTestStatus, MATHball100, MATHball12, MATHball, MATHlang, MATHptName, MATHptRegName, MATHptAreaName, MATHptTerName FROM Odata WHERE MATHtest IS NOT NULL;

INSERT INTO Test_Results(Student_ID, Subject, Status, Ball12, Ball, lang, EO, EO_Reg,  EO_Area, EO_Ter) 
SELECT Student_ID, MATHSTtest, MATHSTTestStatus, MATHSTball12, MATHSTball, MATHSTlang, MATHSTptName, MATHSTptRegName, MATHSTptAreaName, MATHSTptTerName FROM Odata WHERE MATHSTtest IS NOT NULL;

INSERT INTO Test_Results(Student_ID, Subject, Status, Ball100, Ball12, Ball, lang, EO, EO_Reg,  EO_Area, EO_Ter) 
SELECT Student_ID, PHYStest, PHYSTestStatus, PHYSball100, PHYSball12, PHYSball, PHYSlang, PHYSptName, PHYSptRegName, PHYSptAreaName, PHYSptTerName FROM Odata  WHERE PHYStest IS NOT NULL;

INSERT INTO Test_Results(Student_ID, Subject, Status, Ball100, Ball12, Ball, lang, EO, EO_Reg,  EO_Area, EO_Ter) 
SELECT Student_ID, CHEMtest, CHEMTestStatus, CHEMball100, CHEMball12, CHEMball, CHEMlang, CHEMptName, CHEMptRegName, CHEMptAreaName, CHEMptTerName FROM Odata  WHERE CHEMtest IS NOT NULL;

INSERT INTO Test_Results(Student_ID, Subject, Status, Ball100, Ball12, Ball, lang, EO, EO_Reg,  EO_Area, EO_Ter) 
SELECT Student_ID, BIOtest, BIOTestStatus, BIOball100, BIOball12, BIOball, BIOlang, BIOptName, BIOptRegName, BIOptAreaName, BIOptTerName FROM Odata  WHERE BIOtest IS NOT NULL;

INSERT INTO Test_Results(Student_ID, Subject, Status, Ball100, Ball12, Ball, lang, EO, EO_Reg,  EO_Area, EO_Ter) 
SELECT Student_ID, GEOtest, GEOTestStatus, GEOball100, GEOball12, GEOball, GEOlang, GEOptName, GEOptRegName, GEOptAreaName, GEOptTerName FROM Odata  WHERE GEOtest IS NOT NULL;

INSERT INTO Test_Results(Student_ID, Subject, Status, Ball100, Ball12, Ball, DPA_level, EO, EO_Reg,  EO_Area, EO_Ter) 
SELECT Student_ID, ENGtest, ENGTestStatus, ENGball100, ENGball12, ENGball, EngDPAlevel, ENGptName, ENGptRegName, ENGptAreaName, ENGptTerName FROM Odata  WHERE ENGtest IS NOT NULL;

INSERT INTO Test_Results(Student_ID, Subject, Status, Ball100, Ball12, Ball, DPA_level, EO, EO_Reg,  EO_Area, EO_Ter) 
SELECT Student_ID, FRAtest, FRATestStatus, FRAball100, FRAball12, FRAball, FRADPAlevel, FRAptName, FRAptRegName, FRAptAreaName, FRAptTerName FROM Odata  WHERE FRAtest IS NOT NULL;

INSERT INTO Test_Results(Student_ID, Subject, Status, Ball100, Ball12, Ball, DPA_level, EO, EO_Reg,  EO_Area, EO_Ter) 
SELECT Student_ID, DEUtest, DEUTestStatus, DEUball100, DEUball12, DEUball, DEUDPAlevel, DEUptName, DEUptRegName, DEUptAreaName, DEUptTerName FROM Odata  WHERE DEUtest IS NOT NULL;

INSERT INTO Test_Results(Student_ID, Subject, Status, Ball100, Ball12, Ball, DPA_level, EO, EO_Reg,  EO_Area, EO_Ter) 
SELECT Student_ID, SPAtest, SPATestStatus, SPAball100, SPAball12, SPAball, SPADPAlevel, SPAptName, SPAptRegName, SPAptAreaName, SPAptTerName FROM Odata  WHERE SPAtest IS NOT NULL;
