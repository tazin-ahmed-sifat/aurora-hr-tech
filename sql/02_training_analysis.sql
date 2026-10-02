-- Compliance risk by Aurora hotel

SELECT
    h.HotelName,
    h.Country,
    h.Region,

    COUNT(t.TrainingID) AS TrainingRecords,

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
    ) AS RiskRate

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

ORDER BY RiskRate DESC;