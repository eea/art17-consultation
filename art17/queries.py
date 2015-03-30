THREATS_QUERY = """
SELECT A.level2_code                      AS code,
       C.name_corrected                   AS activity,
       Round(100 * A.pl2_num / B.pl2_tot) AS pc
FROM   ((SELECT RS4.level2_code,
               Count(RS4.pl2_ms) AS pl2_num,
               1                 AS pl2_set
        FROM   (SELECT DISTINCT RS2.country AS pl2_ms,
                                RS2.region,
                                SUBSTRING_INDEX(pressurecode, '.', 1) AS level2_code
                FROM   (data_habitats_check_list AS RS3
                        INNER JOIN data_habitats_regions_MS_level AS RS2
                                ON ( RS3.country = RS2.country )
                                   AND ( RS3.region = RS2.region )
                                   AND ( RS3.habitatcode = RS2.habitatcode ))
                       INNER JOIN data_pressures_threats AS RS1
                               ON RS3.regionhash = RS1.habitat_regionhash
                WHERE  ((( RS2.habitatcode ) = '{subject}')
                         AND ((UPPER(presence)) IN ('1', 'SR TAX', 'LR', 'OP', 'EX'))
                         AND ((RS1.type_pressure) = '{pressure_type}' )
                         AND ((RS1.rankingcode) = 'H'))) AS RS4
        GROUP  BY RS4.level2_code) AS A
        INNER JOIN (SELECT Count(RS2.region) AS pl2_tot,
                           1                 AS pl2_set
                    FROM   data_habitats_regions_MS_level AS RS2
                           INNER JOIN data_habitats_check_list AS RS3
                                   ON ( RS3.habitatcode = RS2.habitatcode )
                                      AND ( RS3.region = RS2.region )
                                      AND ( RS3.country = RS2.country )
                    WHERE  (RS2.country <> 'GR' )
                           AND (RS2.habitatcode = '{subject}')
                           AND (UPPER(RS3.presence) IN ('1', 'SR TAX', 'LR', 'OP', 'EX'))) AS B
                ON A.pl2_set = B.pl2_set)
       LEFT JOIN lu_threats AS C
              ON A.level2_code = C.code
ORDER  BY Round(100 * A.pl2_num / B.pl2_tot) DESC
LIMIT 10;
"""
