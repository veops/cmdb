# -*- coding:utf-8 -*- 

from __future__ import unicode_literals

QUERY_CIS_BY_VALUE_TABLE = """
    SELECT attr.name AS attr_name,
          attr.alias AS attr_alias,
          attr.value_type,
          attr.is_list,
          attr.is_password,
          c_cis.type_id,
          {0}.ci_id,
          {0}.attr_id,
          {0}.value
   FROM {0}
   INNER JOIN c_cis ON {0}.ci_id=c_cis.id
   AND {0}.`ci_id` IN ({1})
   INNER JOIN c_attributes as attr ON attr.id = {0}.attr_id
"""

#  {2}: value_table
QUERY_CIS_BY_IDS = """
    SELECT A.ci_id,
           A.type_id,
           A.attr_id,
           A.attr_name,
           A.attr_alias,
           A.value,
           A.value_type,
           A.is_list,
           A.is_password
    FROM
      ({1}) AS A {0}
       ORDER BY A.ci_id;
"""

FACET_QUERY1 = """
    SELECT {0}.value,
           count({0}.ci_id)
    FROM {0}
    INNER JOIN c_attributes AS attr ON attr.id={0}.attr_id
    WHERE attr.name="{1}"
    GROUP BY {0}.ci_id;
"""

FACET_QUERY = """
    SELECT {0}.value,
           count(distinct {0}.ci_id)
    FROM {0}
    INNER JOIN ({1}) AS F ON F.ci_id={0}.ci_id
    WHERE {0}.attr_id={2:d}
    GROUP BY {0}.value
"""

QUERY_CI_BY_ATTR_NAME = """
    SELECT {0}.ci_id
    FROM {0}
    WHERE {0}.attr_id={1:d}
      AND {0}.value {2}
"""

QUERY_CI_BY_ID = """
    SELECT c_cis.id as ci_id
    FROM c_cis
    WHERE c_cis.id={}
"""

QUERY_CI_BY_TYPE = """
    SELECT c_cis.id AS ci_id
    FROM c_cis
    WHERE c_cis.type_id in ({0})
"""

QUERY_UNION_CI_ATTRIBUTE_IS_NULL = """
    SELECT *
    FROM (
      SELECT c_cis.id AS ci_id
      FROM c_cis
      WHERE c_cis.type_id IN ({0})
    ) {3}
      LEFT JOIN (
        SELECT {1}.ci_id
        FROM {1}
        WHERE {1}.attr_id = {2}
          AND {1}.value LIKE "%"
      ) {4} USING (ci_id)
    WHERE {4}.ci_id IS NULL
"""

QUERY_CI_BY_NO_ATTR = """
SELECT *
FROM 
    (SELECT c_value_index_texts.ci_id
    FROM c_value_index_texts
    WHERE c_value_index_texts.value LIKE "{0}"
    UNION
    SELECT c_value_index_integers.ci_id
    FROM c_value_index_integers
    WHERE c_value_index_integers.value LIKE "{0}"
    UNION
    SELECT c_value_index_floats.ci_id
    FROM c_value_index_floats
    WHERE c_value_index_floats.value LIKE "{0}"
    UNION
    SELECT c_value_index_datetime.ci_id
    FROM c_value_index_datetime
    WHERE c_value_index_datetime.value LIKE "{0}") AS {1}
GROUP BY  {1}.ci_id
"""
