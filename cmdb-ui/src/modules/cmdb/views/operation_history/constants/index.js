export const COLUMN_WIDTHS = {
  DATETIME: 160,
  USER: 120,
  OPERATION: 100,
  CI_TYPE: 150,
  INSTANCE: 150,
  ATTRIBUTE: 120,
  OLD_VALUE: 200,
  NEW_VALUE: 200
}

export const OPERATE_TYPE_COLORS = {
  ADD: 'green',
  UPDATE: 'orange',
  DELETE: 'red'
}

export const PAGINATION_CONFIG = {
  DEFAULT_PAGE_SIZE: 50,
  PAGE_SIZE_OPTIONS: [50, 100, 200, 500]
}

export const EXPORT_CONFIG = {
  TYPES: ['xlsx', 'csv'],
  MERGE: true,
  COL_GROUP: true
}

export const DATE_FORMAT = 'YYYY-MM-DD HH:mm:ss'

export const TIME_DEFAULT_VALUE = {
  hideDisabledOptions: true,
  defaultValue: ['00:00:00', '23:59:59']
}
