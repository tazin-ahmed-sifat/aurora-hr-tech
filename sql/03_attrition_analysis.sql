-- --------------------------------------------------
-- ATTRITION RISK BY HOTEL
-- --------------------------------------------------

SELECT
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