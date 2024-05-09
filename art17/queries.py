THREATS_QUERY = """

SELECT    A.level2_code                   AS code,
          C.name_corrected                AS activity,
          Round(100*A.pl2_num/B.pl2_tot)  AS pc
FROM ((SELECT   RS4.level2_code,
                COUNT(RS4.pl2_ms)   AS pl2_num,
                1                   AS pl2_set
       FROM     (SELECT DISTINCT RS2.country AS pl2_ms,
                        RS2.region,
                        RS2.{join_column},
                        split_part(pressurecode, '.', 1) AS level2_code
                 FROM ({checklist_table} AS RS3
                        INNER JOIN {regions_MS_table} AS RS2
                                ON (RS3.country = RS2.country)
                                  AND (RS3.region = RS2.region)
                                  AND (RS3.{join_column} = RS2.{join_column}))
                        INNER JOIN data_pressures_threats AS RS1
                                ON RS3.regionhash = RS1.{regionhash_column}
                 WHERE (((RS2.country<>'GR') And (RS3.{subject_column}) = '{subject}')
                      AND (RS2.use_for_statistics = True)
                      AND (Not (RS1.pressurecode) In ('U','X'))
                      AND ((RS1.type_pressure)='{pressure_type}')
                      AND ((RS1.rankingcode)='H')))  AS RS4
       GROUP BY RS4.level2_code)  AS A
       INNER JOIN   (SELECT COUNT(T.region) AS pl2_tot,
                            1               AS pl2_set
                     FROM   (SELECT DISTINCT RS2.country AS pl2_ms,
                                    RS2.region,
                                    RS2.{join_column},
                                    split_part(pressurecode, '.', 1) AS level2_code
                             FROM ({checklist_table} AS RS3
                             INNER JOIN {regions_MS_table} AS RS2
                                     ON (RS3.country = RS2.country)
                                        AND (RS3.region = RS2.region)
                                        AND (RS3.{join_column} = RS2.{join_column}))
                             INNER JOIN data_pressures_threats AS RS1
                                     ON RS3.regionhash = RS1.{regionhash_column}
                             WHERE (((RS2.country<>'GR')
                                    And (RS3.{subject_column}) = '{subject}')
                                    AND (RS2.use_for_statistics = True)
                                    AND (Not (RS1.pressurecode) In ('U','X'))
                                    AND ((RS1.type_pressure)='{pressure_type}')
                                    AND ((RS1.rankingcode)='H'))) AS T)  AS B
              ON A.pl2_set = B.pl2_set)
       LEFT JOIN lu_threats AS C
              ON A.level2_code = C.code
ORDER BY Round(100*A.pl2_num/B.pl2_tot) DESC, A.level2_code ASC
LIMIT 10
"""

COVERAGE_QUERY_HABITAT = """
SELECT  A.country, A.region,
CASE 
   WHEN (NOT COALESCE(A.coverage_surface_area, 0)=0) THEN
      CASE
         WHEN (NOT COALESCE(A.natura2000_area_max, 0)=0) THEN
            CASE
               WHEN (A.natura2000_area_min IS NOT NULL) THEN
                  CASE
                     WHEN (A.natura2000_area_min=0) THEN 'x'
                     ELSE
                        CASE
                           WHEN (SQRT(A.natura2000_area_min * A.natura2000_area_max) / A.coverage_surface_area > 1) THEN '100*'
                           ELSE Round(100 * SQRT(A.natura2000_area_min * A.natura2000_area_max) / A.coverage_surface_area)::varchar(255)
                        END
                  END
               ELSE 'x'
            END
         ELSE
            CASE
               WHEN (A.natura2000_area_min IS NOT NULL) THEN
                  CASE
                     WHEN (A.natura2000_area_min / A.coverage_surface_area > 1) THEN '100*'
                     ELSE
                        CASE
                           WHEN (A.natura2000_area_min=0) THEN '0'
                           ELSE Round(100 * A.natura2000_area_min / A.coverage_surface_area)::varchar(255)
                        END
                  END
               ELSE 'x'
            END
      END
   ELSE 'x'
END AS pc
FROM data_habitats_regions_ms_level AS A
INNER JOIN data_habitats_check_list AS B
               ON ( A.country = B.country )
                  AND ( A.region = B.region )
                  AND ( A.habitatcode = B.habitatcode )
WHERE  A.use_for_statistics = true
       AND A.habitatcode = '{subject}'
       AND A.country <> 'GR'
ORDER BY country;
"""

COVERAGE_QUERY_SPECIES = """
SELECT A.country, A.region,
CASE
   WHEN (A.natura2000_population_unit IS NOT NULL AND A.natura2000_population_unit = A.population_size_unit) THEN
      CASE
         WHEN (NOT COALESCE(A.population_maximum_size, 0)=0) THEN
            CASE
               WHEN (A.population_minimum_size IS NOT NULL) THEN
                  CASE
                     WHEN (NOT COALESCE(A.natura2000_population_max, 0)=0) THEN
                        CASE  
                           WHEN (A.natura2000_population_min IS NOT NULL) THEN
                              CASE
                                 WHEN (SQRT(A.natura2000_population_min * A.natura2000_population_max) / SQRT(A.population_minimum_size * A.population_maximum_size) > 1) THEN '100*'
                                 ELSE Round(100 * SQRT(A.natura2000_population_min * A.natura2000_population_max) / SQRT(A.population_minimum_size * A.population_maximum_size))::varchar(255)
                              END
                           ELSE 'x'
                        END
                     ELSE
                        CASE
                           WHEN (A.natura2000_population_min IS NOT NULL) THEN
                              CASE
                                 WHEN (A.natura2000_population_min=0 AND A.natura2000_population_max IS NOT NULL) THEN '0'
                                 ELSE
                                    CASE
                                       WHEN (A.natura2000_population_min / SQRT(A.population_minimum_size * A.population_maximum_size) > 1) THEN '100*'
                                       ELSE Round(100 * A.natura2000_population_min / SQRT(A.population_minimum_size * A.population_maximum_size))::varchar(255)
                                    END
                              END
                           ELSE 'x'
                        END
                  END
               ELSE 'x'
            END
         ELSE
            CASE
               WHEN (A.population_minimum_size IS NOT NULL) THEN
                  CASE
                     WHEN (NOT COALESCE(A.natura2000_population_max, 0)=0) THEN
                        CASE
                           WHEN (A.natura2000_population_min IS NOT NULL) THEN
                              CASE
                                 WHEN (A.population_maximum_size IS NOT NULL) THEN 'x'
                                 ELSE
                                    CASE
                                       WHEN (SQRT(A.natura2000_population_min * A.natura2000_population_max) / A.population_minimum_size > 1) THEN '100*'
                                       ELSE Round(100 * SQRT(A.natura2000_population_min * A.natura2000_population_max) / A.population_minimum_size)::varchar(255)
                                    END
                              END
                           ELSE 'x'
                        END
                     ELSE
                        CASE
                           WHEN (A.natura2000_population_min IS NOT NULL) THEN
                              CASE
                                 WHEN (A.population_minimum_size=0 AND A.natura2000_population_min=0) THEN 'x'
                                 ELSE
                                    CASE
                                       WHEN (A.natura2000_population_min / A.population_minimum_size > 1) THEN '100*'
                                       ELSE Round(100 * A.natura2000_population_min / A.population_minimum_size)::varchar(255)
                                    END
                              END
                           ELSE 'x'
                        END
                  END
               ELSE 'x'
            END
      END
   ELSE
      CASE
         WHEN (A.natura2000_population_unit IS NOT NULL AND A.natura2000_population_unit = A.population_alt_size_unit) THEN
            CASE
               WHEN (NOT COALESCE(A.population_alt_maximum_size, 0)=0) THEN
                  CASE
                     WHEN (A.population_alt_minimum_size IS NOT NULL) THEN
                        CASE
                           WHEN (NOT COALESCE(A.natura2000_population_max, 0)=0) THEN
                              CASE
                                 WHEN (A.natura2000_population_min IS NOT NULL) THEN
                                    CASE
                                       WHEN (SQRT(A.natura2000_population_min * A.natura2000_population_max) / SQRT(A.population_alt_minimum_size * A.population_alt_maximum_size) > 1) THEN '100*'
                                       ELSE Round(100 * SQRT(A.natura2000_population_min * A.natura2000_population_max) / SQRT(A.population_alt_minimum_size * A.population_alt_maximum_size))::varchar(255)
                                    END
                                 ELSE 'x'
                              END
                           ELSE
                              CASE
                                 WHEN (A.natura2000_population_min IS NOT NULL) THEN
                                    CASE
                                       WHEN (A.natura2000_population_min=0 AND A.natura2000_population_max IS NOT NULL) THEN '0'
                                       ELSE
                                          CASE
                                             WHEN (A.natura2000_population_min / SQRT(A.population_alt_minimum_size * A.population_alt_maximum_size) > 1) THEN '100*'
                                             ELSE Round(100 * A.natura2000_population_min / SQRT(A.population_alt_minimum_size * A.population_alt_maximum_size))::varchar(255)
                                          END
                                    END
                                 ELSE 'x'
                              END
                        END
                     ELSE 'x'
                  END
               ELSE
                  CASE
                     WHEN (A.population_alt_minimum_size IS NOT NULL) THEN
                        CASE
                           WHEN (NOT COALESCE(A.natura2000_population_max, 0)=0) THEN
                              CASE
                                 WHEN (A.natura2000_population_min IS NOT NULL) THEN
                                    CASE
                                       WHEN (A.population_alt_maximum_size IS NOT NULL) THEN 'x'
                                       ELSE  
                                          CASE
                                             WHEN (A.population_alt_minimum_size=0) THEN 'x'
                                             ELSE
                                                CASE
                                                   WHEN (SQRT(A.natura2000_population_min * A.natura2000_population_max) / A.population_alt_minimum_size > 1) THEN '100*'
                                                   ELSE Round(100 * SQRT(A.natura2000_population_min * A.natura2000_population_max) / A.population_alt_minimum_size)::varchar(255)
                                                END
                                          END
                                    END
                                 ELSE 'x'
                              END
                           ELSE
                              CASE
                                 WHEN (A.natura2000_population_min IS NOT NULL) THEN
                                    CASE
                                       WHEN (A.population_alt_minimum_size=0 AND A.natura2000_population_min=0) THEN 'x'
                                       ELSE
                                          CASE
                                             WHEN (A.natura2000_population_min / A.population_alt_minimum_size > 1) THEN '100*'
                                             ELSE Round(100 * A.natura2000_population_min / A.population_alt_minimum_size)::varchar(255)
                                          END
                                    END
                                 ELSE 'x'
                              END
                        END
                     ELSE 'x'
                  END
            END
         ELSE 'x'
      END
END AS pc
FROM   data_species_regions_MS_level AS A
       INNER JOIN data_species_check_list AS B
               ON ( A.{join_column} = B.{join_column} )
                  AND ( A.region = B.region )
                  AND ( A.country = B.country )
WHERE B.{subject_column} = '{subject}'
      AND A.use_for_statistics = True
      AND A.country <> 'GR'
ORDER BY country;
"""

MEASURES_QUERY = """
SELECT C.code,
       C.name AS activity,
       Round(100 * A.pl2_num / B.pl2_tot) AS pc
FROM ((SELECT RS1.measurecode AS level2_code,
       COUNT(RS2.region) AS pl2_num,
       1 AS pl2_set
FROM ({checklist_table} AS RS3
        INNER JOIN {regions_MS_table} AS RS2
            ON (RS3.country = RS2.country) AND (RS3.region = RS2.region) AND (RS3.{join_column} = RS2.{join_column}))
        INNER JOIN data_measures RS1
            ON (RS1.{regionhash_column} = RS2.regionhash)
WHERE (RS2.use_for_statistics = True)
         {extra}
         AND (RS3.{subject_column} = '{subject}')
         AND (RS1.rankingcode = 'H')
         AND NOT (RS1.measurecode LIKE '1%%')
GROUP BY RS1.measurecode) AS A
INNER JOIN
       (SELECT COUNT(RS2.region) AS pl2_tot,
                 1 AS pl2_set
        FROM ({checklist_table} AS RS3
        INNER JOIN {regions_MS_table} AS RS2
            ON (RS3.country = RS2.country) AND (RS3.region = RS2.region) AND (RS3.{join_column} = RS2.{join_column}))
        INNER JOIN data_measures RS1
            ON (RS1.{regionhash_column} = RS2.regionhash)
        WHERE (RS2.use_for_statistics = True)
              {extra}
              AND (RS3.{subject_column} = '{subject}')
              AND (RS1.rankingcode = 'H')
              AND NOT (RS1.measurecode LIKE '1%%')) AS B
       ON (A.pl2_set = B.pl2_set))
LEFT JOIN lu_measures AS C
       ON (C.code = A.level2_code)
ORDER BY 100 * A.pl2_num / B.pl2_tot DESC, A.level2_code ASC
LIMIT 10;
"""

N2K_QUERY = """
   SELECT DISTINCT Max(A.annex_II) LIKE 'Y%%' AS cond
   FROM data_species_check_list A
   WHERE A.assessment_speciesname = '{subject}'
   GROUP BY A.assessment_speciesname;
"""


ANNEX_QUERY = """
  SELECT
      CASE
         WHEN Max(A.annex_II) LIKE 'Y%%' THEN 'II'
         ELSE ''
         END AS annex_II,
      CASE
         WHEN Max(A.annex_IV) LIKE 'Y%%' THEN 'IV'
         ELSE ''
         END AS annex_IV,
      CASE
         WHEN Max(A.annex_V) LIKE 'Y%%' THEN 'V'
         ELSE ''
         END AS annex_V
  FROM data_species_check_list A
  WHERE A.assessment_speciesname = '{subject}'
  GROUP BY A.assessment_speciesname;
"""

MAP_QUERY = """
  SELECT DISTINCT A.assessment_speciescode AS code
  FROM data_species_check_list A
  WHERE A.assessment_speciesname='{subject}';
"""
