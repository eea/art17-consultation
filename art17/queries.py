THREATS_QUERY = """
SELECT A.level2_code                      AS code,
       C.name_corrected                   AS activity,
       Round(100 * A.pl2_num / B.pl2_tot) AS pc
FROM   ((SELECT RS4.level2_code,
               Count(RS4.pl2_ms) AS pl2_num,
               1                 AS pl2_set
        FROM   (SELECT DISTINCT RS2.country AS pl2_ms,
                                RS2.region,
                                SUBSTRING_INDEX(pressurecode, '.', 1)
                                  AS level2_code
                FROM   ({checklist_table} AS RS3
                        INNER JOIN {regions_MS_table} AS RS2
                                ON (RS3.country = RS2.country)
                                   AND (RS3.region = RS2.region)
                                   AND (RS3.{join_column} = RS2.{join_column}))
                       INNER JOIN data_pressures_threats AS RS1
                               ON RS3.regionhash = RS1.{regionhash_column}
                WHERE  (((RS3.{subject_column}) = '{subject}')
                         AND ((UPPER(presence)) IN
                           ('1', 'SR TAX', 'LR', 'OP', 'EX'))
                         AND ((RS1.type_pressure) = '{pressure_type}' )
                         AND ((RS1.rankingcode) = 'H'))) AS RS4
        GROUP  BY RS4.level2_code) AS A
        INNER JOIN (SELECT Count(RS2.region) AS pl2_tot,
                           1                 AS pl2_set
                    FROM  {regions_MS_table} AS RS2
                           INNER JOIN {checklist_table} AS RS3
                                   ON (RS3.{join_column} = RS2.{join_column})
                                      AND (RS3.region = RS2.region)
                                      AND (RS3.country = RS2.country)
                    WHERE  (RS2.country <> 'GR' )
                           AND (RS3.{subject_column} = '{subject}')
                           AND (UPPER(RS3.presence) IN
                             ('1', 'SR TAX', 'LR', 'OP', 'EX'))) AS B
                ON A.pl2_set = B.pl2_set)
       LEFT JOIN lu_threats AS C
              ON A.level2_code = C.code
ORDER  BY Round(100 * A.pl2_num / B.pl2_tot) DESC
LIMIT 10;
"""

COVERAGE_QUERY_HABITAT = """
SELECT  A.country, A.region,
 IF(
    NOT IFNULL(A.coverage_surface_area, 0)=0,
    IF(
      NOT IFNULL(A.natura2000_area_max, 0),
      IF(
        SQRT(A.natura2000_area_min*A.natura2000_area_max)/A.coverage_surface_area>1,
        '100*',
        Round(100*SQRT(A.natura2000_area_min*A.natura2000_area_max)/A.coverage_surface_area)
      ),
      IF(
        A.natura2000_area_min/A.coverage_surface_area>1,
        '100*',
        Round(100*A.natura2000_area_min/A.coverage_surface_area)
      )
    ),
    'na'
  ) pc

FROM data_habitats_regions_MS_level AS A
INNER JOIN data_habitats_check_list AS B
               ON ( A.country = B.country )
                  AND ( A.region = B.region )
                  AND ( A.habitatcode = B.habitatcode )
WHERE  ( upper(B.presence) IN ( '1', 'SR TAX', 'LR', 'OP', 'EX' ) )
       AND A.habitatcode = '{subject}'
       AND A.country <> 'GR'
ORDER BY country;
"""

COVERAGE_QUERY_SPECIES = """
SELECT A.country, A.region,
IF(A.natura2000_population_unit = A.population_size_unit,
   IF(NOT A.population_maximum_size IS null AND NOT IFNULL(A.population_maximum_size, 0)=0,
      IF(NOT A.population_minimum_size IS null AND NOT IFNULL(A.population_minimum_size, 0)=0,
         IF(NOT A.natura2000_population_max IS null,
            IF(NOT A.natura2000_population_min IS null,
               IF(SQRT(A.natura2000_population_min*A.natura2000_population_max)/SQRT(A.population_minimum_size*A.population_maximum_size)>1,
                  '100*',
                  Round(100*SQRT(A.natura2000_population_min*A.natura2000_population_max)/SQRT(A.population_minimum_size*A.population_maximum_size))),
               'na'),
            IF(NOT A.natura2000_population_min IS null,
               IF(A.natura2000_population_min/SQRT(A.population_minimum_size*A.population_maximum_size)>1,
                  '100*',
                  Round(100*A.natura2000_population_min/SQRT(A.population_minimum_size*A.population_maximum_size))),
               'na')),
         'na'),
       IF(NOT A.population_minimum_size IS null AND NOT IFNULL(A.population_minimum_size, 0)=0,
          IF(NOT A.natura2000_population_max IS null,
             IF(NOT A.natura2000_population_min IS null,
                IF(SQRT(A.natura2000_population_min*A.natura2000_population_max)/A.population_minimum_size>1,
                   '100*',
                   Round(100*SQRT(A.natura2000_population_min*A.natura2000_population_max)/A.population_minimum_size)),
                'na'),
             IF(NOT A.natura2000_population_min IS null,
                IF(A.natura2000_population_min/A.population_minimum_size>1,
                   '100*',
                   Round(100*A.natura2000_population_min/A.population_minimum_size)),
                'na')),
          'na')),
   IF(A.natura2000_population_unit = A.population_alt_size_unit,
      IF(NOT A.population_alt_maximum_size IS null AND NOT IFNULL(A.population_alt_maximum_size, 0)=0,
         IF(NOT A.population_alt_minimum_size IS null AND NOT IFNULL(A.population_alt_minimum_size, 0)=0,
            IF(NOT A.natura2000_population_max IS null,
               IF(NOT A.natura2000_population_min IS null,
                  IF(SQRT(A.natura2000_population_min*A.natura2000_population_max)/SQRT(A.population_alt_minimum_size*A.population_alt_maximum_size)>1,
                     '100*',
                     Round(100*SQRT(A.natura2000_population_min*A.natura2000_population_max)/SQRT(A.population_alt_minimum_size*A.population_alt_maximum_size))),
                  'na'),
               IF(NOT A.natura2000_population_min IS null,
                  IF(A.natura2000_population_min/SQRT(A.population_alt_minimum_size*A.population_alt_maximum_size)>1,
                     '100*',
                     Round(100*A.natura2000_population_min/SQRT(A.population_alt_minimum_size*A.population_alt_maximum_size))),
                  'na')),
            'na'),
         IF(NOT A.population_alt_minimum_size IS null AND NOT IFNULL(A.population_alt_minimum_size, 0)=0,
            IF(NOT A.natura2000_population_max IS null,
               IF(NOT A.natura2000_population_min IS null,
                  IF(SQRT(A.natura2000_population_min*A.natura2000_population_max)/A.population_alt_minimum_size>1,
                     '100*',
                     Round(100*SQRT(A.natura2000_population_min*A.natura2000_population_max)/A.population_alt_minimum_size)),
                  'na'),
               IF(NOT A.natura2000_population_min IS null,
                  IF(A.natura2000_population_min/A.population_alt_minimum_size>1,
                     '100*',
                     Round(100*A.natura2000_population_min/A.population_alt_minimum_size)),
                  'na')),
            'na')),
      'na'
)) AS pc
FROM   data_species_regions_MS_level AS A
       INNER JOIN data_species_check_list AS B
               ON ( A.speciesname = B.speciesname )
                  AND ( A.region = B.region )
                  AND ( A.country = B.country )
WHERE  ( Ucase(B.presence) IN ( '1', 'SR TAX', 'LR', 'OP', 'EX' ) )
       AND B.assessment_speciesname = '{subject}'
       AND A.country <> 'GR'
ORDER BY country;
"""

MEASURES_QUERY = """
SELECT C.name AS activity,
       Round(100 * A.pl2_num / B.pl2_tot) AS pc
  FROM ((SELECT RS1.measurecode AS level2_code,
       COUNT(RS2.region) AS pl2_num,
       1 AS pl2_set
  FROM (data_species_check_list AS RS3
        INNER JOIN data_species_regions_MS_level AS RS2
            ON (RS3.country = RS2.country) AND (RS3.region = RS2.region) AND (RS3.speciesname = RS2.speciesname))
        INNER JOIN data_measures RS1
            ON (RS1.species_regionhash =
                 RS2.regionhash)
 WHERE ((UPPER(presence)) In ('1','SR TAX','LR','OP','EX')) AND UPPER(RS3.annex_II) like 'Y%%' AND (RS3.assessment_speciesname = '{subject}')
  GROUP BY RS1.measurecode) AS A
       INNER JOIN
       (SELECT COUNT(RS2.region) AS pl2_tot,
       1 AS pl2_set
  FROM (data_species_check_list AS RS3
        INNER JOIN data_species_regions_MS_level AS RS2
            ON (RS3.country = RS2.country) AND (RS3.region = RS2.region) AND (RS3.speciesname = RS2.speciesname))
       INNER JOIN data_measures RS1
            ON (RS1.species_regionhash =
                 RS2.regionhash)
 WHERE ((UPPER(presence)) In ('1','SR TAX','LR','OP','EX')) AND UPPER(RS3.annex_II) like 'Y%%' AND (RS3.assessment_speciesname = '{subject}')) AS B
          ON (A.pl2_set = B.pl2_set))
       LEFT JOIN lu_measures AS C
          ON (C.code = A.level2_code)
ORDER BY 100 * A.pl2_num / B.pl2_tot DESC LIMIT 10;
"""
