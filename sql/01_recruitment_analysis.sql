
-- Recruitment applications by source

SELECT
    Source,
    COUNT(*) AS Applications
FROM recruitment
GROUP BY Source
ORDER BY Applications DESC;

-- Recruitment performance by source

SELECT
    Source,
    COUNT(*) AS Applications,

    SUM(
        CASE
            WHEN Status = 'Hired' THEN 1
            ELSE 0
        END
    ) AS Hires,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN Status = 'Hired' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        1
    ) AS HireRate

FROM recruitment

GROUP BY Source

ORDER BY HireRate DESC;


-- Recruitment activity by hotel

SELECT
    h.HotelName,
    h.Country,
    COUNT(r.ApplicationID) AS Applications

FROM recruitment AS r

JOIN hotels AS h
    ON r.HotelID = h.HotelID

GROUP BY
    h.HotelName,
    h.Country

ORDER BY Applications DESC;

-- Recruitment performance by region

SELECT
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
    ) AS AvgTimeToHire

FROM recruitment AS r

JOIN hotels AS h
    ON r.HotelID = h.HotelID

GROUP BY h.Region

ORDER BY HireRate DESC;