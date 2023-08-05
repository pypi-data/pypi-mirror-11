/*
 * Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
package monasca.api.infrastructure.persistence.vertica;

import monasca.api.domain.model.metric.MetricDefinitionRepo;
import monasca.api.domain.model.metric.MetricName;
import monasca.api.infrastructure.persistence.DimensionQueries;
import monasca.api.resource.exception.Exceptions;
import monasca.common.model.metric.MetricDefinition;

import org.apache.commons.codec.DecoderException;
import org.apache.commons.codec.binary.Hex;
import org.skife.jdbi.v2.DBI;
import org.skife.jdbi.v2.Handle;
import org.skife.jdbi.v2.Query;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.inject.Inject;
import javax.inject.Named;

public class MetricDefinitionVerticaRepoImpl implements MetricDefinitionRepo {

  private static final Logger
      logger =
      LoggerFactory.getLogger(MetricDefinitionVerticaRepoImpl.class);

  private static final String
      FIND_METRIC_DEFS_SQL =
      "SELECT defDims.id as defDimsId, def.name, dims.name as dName, dims.value AS dValue "
      + "FROM MonMetrics.Definitions def, MonMetrics.DefinitionDimensions defDims "
      // Outer join needed in case there are no dimensions for a definition.
      + "LEFT OUTER JOIN MonMetrics.Dimensions dims ON dims.dimension_set_id = defDims"
      + ".dimension_set_id "
      + "WHERE def.id = defDims.definition_id "
      + "AND defDims.id IN (%s) "
      + "ORDER BY defDims.id ASC ";

  private static final String
      METRIC_DEFINITIONS_SUB_SELECT =
      "SELECT defDimsSub.id "
      + "FROM  MonMetrics.Definitions defSub, MonMetrics.DefinitionDimensions defDimsSub"
      + "%s " // Dimensions inner join goes here if dimensions specified.
      + "WHERE defDimsSub.definition_id = defSub.id "
      + "AND defSub.tenant_id = :tenantId "
      + "%s " // Name goes here.
      + "%s " // Offset goes here.
      + "ORDER BY defdimsSub.id ASC %s"; // Limit goes here.

  private static final String
      FIND_METRIC_NAMES_SQL =
      "SELECT distinct def.id, def.name "
      + "FROM MonMetrics.Definitions def "
      + "WHERE def.id IN (%s) "
      + "ORDER BY def.id ASC ";

  private static final String
      METRIC_NAMES_SUB_SELECT =
      "SELECT defSub.id "
      + "FROM  MonMetrics.Definitions defSub, MonMetrics.DefinitionDimensions defDimsSub"
      + "%s " // Dimensions inner join goes here if dimensions specified.
      + "WHERE defDimsSub.definition_id = defSub.id "
      + "AND defSub.tenant_id = :tenantId "
      + "%s " // Offset goes here.
      + "ORDER BY defSub.id ASC %s"; // Limit goes here.

  private static final String TABLE_TO_JOIN_DIMENSIONS_ON = "defDimsSub";

  private final DBI db;

  @Inject
  public MetricDefinitionVerticaRepoImpl(@Named("vertica") DBI db) {

    this.db = db;

  }

  @Override
  public List<MetricName> findNames(
      String tenantId, Map<String,
      String> dimensions,
      String offset,
      int limit) throws Exception {

    List<Map<String, Object>> rows = executeMetricNamesQuery(tenantId, dimensions, offset, limit);

    List<MetricName> metricNameList = new ArrayList<>(rows.size());

    for (Map<String, Object> row : rows) {

      byte[] defId = (byte[]) row.get("id");

      String name = (String) row.get("name");

      MetricName metricName = new MetricName(Hex.encodeHexString(defId), name);

      metricNameList.add(metricName);

    }

    return metricNameList;

  }

  private List<Map<String, Object>> executeMetricNamesQuery(
      String tenantId,
      Map<String, String> dimensions,
      String offset,
      int limit) {

    String offsetPart = "";

    if (offset != null && !offset.isEmpty()) {

      offsetPart = " and defSub.id > :offset ";

    }

    // Can't bind limit in a nested sub query. So, just tack on as String.
    String limitPart = " limit " + Integer.toString(limit + 1);

    String
        defSubSelect =
        String.format(METRIC_NAMES_SUB_SELECT,
                      MetricQueries.buildJoinClauseFor(dimensions, TABLE_TO_JOIN_DIMENSIONS_ON),
                      offsetPart, limitPart);

    String sql = String.format(FIND_METRIC_NAMES_SQL, defSubSelect);

    try (Handle h = db.open()) {

      Query<Map<String, Object>> query = h.createQuery(sql).bind("tenantId", tenantId);

      if (offset != null && !offset.isEmpty()) {

        logger.debug("binding offset: {}", offset);

        try {

          query.bind("offset", Hex.decodeHex(offset.toCharArray()));

        } catch (DecoderException e) {

          throw Exceptions.badRequest("failed to decode offset " + offset, e);
        }

      }

      DimensionQueries.bindDimensionsToQuery(query, dimensions);

      return query.list();
    }
  }

  @Override
  public List<MetricDefinition> find(
      String tenantId,
      String name,
      Map<String, String> dimensions,
      String offset,
      int limit) {

    List<Map<String, Object>>
        rows =
        executeMetricDefsQuery(tenantId, name, dimensions, offset, limit);

    List<MetricDefinition> metricDefs = new ArrayList<>(rows.size());

    byte[] currentDefDimId = null;

    Map<String, String> dims = null;

    for (Map<String, Object> row : rows) {

      byte[] defDimId = (byte[]) row.get("defdimsid");

      String metricName = (String) row.get("name");

      String dimName = (String) row.get("dname");

      String dimValue = (String) row.get("dvalue");

      if (defDimId == null || !Arrays.equals(currentDefDimId, defDimId)) {

        currentDefDimId = defDimId;

        dims = new HashMap<>();

        if (dimName != null && dimValue != null) {

          dims.put(dimName, dimValue);

        }

        MetricDefinition m = new MetricDefinition(metricName, dims);
        m.setId(Hex.encodeHexString(defDimId));
        metricDefs.add(m);


      } else {

        dims.put(dimName, dimValue);

      }
    }

    return metricDefs;
  }

  private List<Map<String, Object>> executeMetricDefsQuery(
      String tenantId,
      String name,
      Map<String, String> dimensions,
      String offset,
      int limit) {

    String namePart = "";

    if (name != null && !name.isEmpty()) {

      namePart = " and defSub.name = :name ";

    }

    String offsetPart = "";

    if (offset != null && !offset.isEmpty()) {

      offsetPart = " and defdimsSub.id > :offset ";

    }

    // Can't bind limit in a nested sub query. So, just tack on as String.
    String limitPart = " limit " + Integer.toString(limit + 1);

    String
        defSubSelect =
        String.format(METRIC_DEFINITIONS_SUB_SELECT,
                      MetricQueries.buildJoinClauseFor(dimensions, TABLE_TO_JOIN_DIMENSIONS_ON),
                      namePart, offsetPart, limitPart);

    String sql = String.format(FIND_METRIC_DEFS_SQL, defSubSelect);

    try (Handle h = db.open()) {

      Query<Map<String, Object>> query = h.createQuery(sql).bind("tenantId", tenantId);

      if (name != null && !name.isEmpty()) {

        logger.debug("binding name: {}", name);

        query.bind("name", name);

      }

      if (offset != null && !offset.isEmpty()) {

        logger.debug("binding offset: {}", offset);

        try {

          query.bind("offset", Hex.decodeHex(offset.toCharArray()));

        } catch (DecoderException e) {

          throw Exceptions.badRequest("failed to decode offset " + offset, e);
        }

      }

      DimensionQueries.bindDimensionsToQuery(query, dimensions);

      return query.list();
    }
  }
}
