-- --------------------------------------------------
-- 1. WORKFORCE OVERVIEW BY HOTEL
-- --------------------------------------------------

SELECT
    h.HotelID,
    h.HotelName,
    h.City,
    h.Country,
    h.Region,

    COUNT(e.EmployeeNumber) AS Employees,

    SUM(
        CASE
            WHEN e.Attrition = 'Yes' THEN 1
            ELSE 0
        END
    ) AS AttritionCount,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN e.Attrition = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(e.EmployeeNumber),
        1
    ) AS AttritionRate

FROM employees AS e

JOIN hotels AS h
    ON e.HotelID = h.HotelID

GROUP BY
    h.HotelID,
    h.HotelName,
    h.City,
    h.Country,
    h.Region

ORDER BY
    AttritionRate DESC;


    -- --------------------------------------------------
-- 2. RECRUITMENT OVERVIEW BY HOTEL
-- --------------------------------------------------

SELECT
    h.HotelID,
    h.HotelName,
    h.Country,
    h.Region,

    COUNT(r.ApplicationID) AS Applications,

    SUM(
        CASE
            WHEN r.Status = 'Hired' THEN 1
            ELSE 0
        END
    ) AS Hires,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN r.Status = 'Hired' THEN 1
                ELSE 0
            END
        ) / COUNT(r.ApplicationID),
        1
    ) AS HireRate,

    ROUND(
        AVG(
            CASE
                WHEN r.Status = 'Hired'
                THEN r.TimeToHireDays
            END
        ),
        1
    ) AS AvgTimeToHireDays

FROM recruitment AS r

JOIN hotels AS h
    ON r.HotelID = h.HotelID

GROUP BY
    h.HotelID,
    h.HotelName,
    h.Country,
    h.Region

ORDER BY
    HireRate DESC;


    -- --------------------------------------------------
-- 3. TRAINING & COMPLIANCE OVERVIEW BY HOTEL
-- --------------------------------------------------

SELECT
    h.HotelID,
    h.HotelName,
    h.Country,
    h.Region,

    COUNT(t.TrainingID) AS TrainingRecords,

    SUM(
        CASE
            WHEN t.Status = 'Completed' THEN 1
            ELSE 0
        END
    ) AS CompletedTraining,

    SUM(
        CASE
            WHEN t.Status = 'Overdue' THEN 1
            ELSE 0
        END
    ) AS OverdueTraining,

    SUM(
        CASE
            WHEN t.ComplianceRisk = 1 THEN 1
            ELSE 0
        END
    ) AS ComplianceRisks,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN t.ComplianceRisk = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(t.TrainingID),
        1
    ) AS ComplianceRiskRate

FROM training AS t

JOIN employees AS e
    ON t.EmployeeNumber = e.EmployeeNumber

JOIN hotels AS h
    ON e.HotelID = h.HotelID

GROUP BY
    h.HotelID,
    h.HotelName,
    h.Country,
    h.Region

ORDER BY
    ComplianceRiskRate DESC;


    -- --------------------------------------------------
-- 4. ATTRITION RISK OVERVIEW BY HOTEL
-- --------------------------------------------------

SELECT
    h.HotelID,
    h.HotelName,
    h.Country,
    h.Region,

    COUNT(a.EmployeeNumber) AS Employees,

    SUM(
        CASE
            WHEN a.RiskBand = 'High' THEN 1
            ELSE 0
        END
    ) AS HighRiskEmployees,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN a.RiskBand = 'High' THEN 1
                ELSE 0
            END
        ) / COUNT(a.EmployeeNumber),
        1
    ) AS HighRiskRate,

    ROUND(
        AVG(a.AttritionRisk) * 100,
        1
    ) AS AvgRiskScore

FROM attrition_risk AS a

JOIN hotels AS h
    ON a.HotelID = h.HotelID

GROUP BY
    h.HotelID,
    h.HotelName,
    h.Country,
    h.Region

ORDER BY
    HighRiskRate DESC;