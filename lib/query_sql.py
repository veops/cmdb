# -*- coding:utf-8 -*- 


QUERY_HOSTS_BY_APP = """
    SELECT *
    FROM cis
    INNER JOIN ci_relations AS cr ON cis.`ci_id`=cr.`second_ci`
    WHERE cr.`first_ci` = {0:d} LIMIT {1:d}, {2:d};
"""

QUERY_HOSTS_NUM_BY_PROJECT = """
    SELECT cr.first_ci_id,
          count(DISTINCT cr.second_ci_id)
    FROM ci_relations AS cr
    WHERE cr.first_ci_id IN {0}
    GROUP BY cr.first_ci_id
"""

QUERY_HOSTS_NUM_BY_BU = """
    SELECT B.first_ci_id,
           count(DISTINCT cr.second_ci_id)
    FROM
      (SELECT A.first_ci_id,
              cr.second_ci_id
       FROM
         (SELECT cr.first_ci_id,
                 cis.ci_id
          FROM cis
          INNER JOIN ci_relations AS cr ON cis.ci_id=cr.second_ci_id
          WHERE cr.first_ci_id IN {0}) AS A
       INNER JOIN ci_relations AS cr ON cr.first_ci_id=A.ci_id) AS B
    INNER JOIN ci_relations AS cr ON B.second_ci_id=cr.first_ci_id
    GROUP BY B.first_ci_id
"""

QUERY_HOSTS_NUM_BY_PRODUCT = """
    SELECT A.first_ci_id,
           count(DISTINCT cr.second_ci_id)
    FROM
      (SELECT cr.first_ci_id,
              cis.ci_id
       FROM cis
       INNER JOIN ci_relations AS cr ON cis.ci_id=cr.second_ci_id
       WHERE cr.first_ci_id IN {0}) AS A
    INNER JOIN ci_relations AS cr ON cr.first_ci_id=A.ci_id
    GROUP BY A.first_ci_id;
"""

QUERY_CIS_BY_VALUE_TABLE = """
    SELECT attr.attr_name,
                  attr.attr_alias,
                  attr.value_type,
                  attr.is_multivalue,
                  cis.type_id,
                  {0}.ci_id,
                  {0}.attr_id,
                  {0}.value
           FROM {0}
           INNER JOIN cis ON {0}.ci_id=cis.ci_id
           AND {0}.`ci_id` IN ({1})
           INNER JOIN ci_attributes as attr ON attr.attr_id = {0}.attr_id
"""

QUERY_CIS_BY_IDS = """
    SELECT A.ci_id,
           A.type_id,
           A.attr_id,
           A.attr_name,
           A.attr_alias,
           A.value,
           A.value_type,
           A.is_multivalue
    FROM
      ({2}) AS A {1}
       ORDER BY A.ci_id;
"""

FACET_QUERY1 = """
    SELECT {0}.value,
           count({0}.ci_id)
    FROM {0}
    INNER JOIN ci_attributes AS attr ON attr.attr_id={0}.attr_id
    WHERE attr.attr_name="{1}"
    GROUP BY {0}.ci_id;
"""

FACET_QUERY = """
    SELECT {0}.value,
           count({0}.ci_id)
    FROM {0}
    INNER JOIN ({1}) AS B ON B.ci_id={0}.ci_id
    WHERE {0}.attr_id={2:d}
    GROUP BY {0}.ci_id
"""

QUERY_CI_BY_ATTR_NAME = """
    SELECT {0}.ci_id
    FROM {0}
    WHERE {0}.attr_id={1:d}
      AND {0}.value {2}
"""

QUERY_CI_BY_TYPE = """
    SELECT cis.ci_id
    FROM cis
    WHERE cis.type_id in ({0})
"""