import _ from 'lodash'

export function deepCompare({
  obj1,
  obj2,
  directDeepKeys = [],
  ignoreKeys = [],
}) {
  const diffs = []

  const formatValue = (val) => {
    if (val === null) return 'null'
    if (val === undefined) return 'undefined'
    if (typeof val === 'object') {
      return JSON.stringify(val)
    }
    return String(val)
  }

  function compare(obj1, obj2, path = '') {
    if (typeof obj1 !== 'object' || typeof obj2 !== 'object' || obj1 === null || obj2 === null) {
      if (obj1 !== obj2) {
        diffs.push({
          path,
          value1: formatValue(obj1),
          value2: formatValue(obj2)
        })
      }
      return
    }

    const keys1 = new Set(Object.keys(obj1))
    const keys2 = new Set(Object.keys(obj2))
    const allKeys = new Set([...keys1, ...keys2])

    allKeys.forEach(key => {
      if (ignoreKeys.includes(key)) return

      const newPath = path ? `${path}.${key}` : key

      if (directDeepKeys.includes(key)) {
        if (!_.isEqual(obj1[key], obj2[key])) {
          diffs.push({
            path: newPath,
            value1: formatValue(obj1[key]),
            value2: formatValue(obj2[key])
          })
        }
        return
      }

      if (!keys1.has(key)) {
        diffs.push({ path: newPath, value1: undefined, value2: formatValue(obj2[key]) })
      } else if (!keys2.has(key)) {
        diffs.push({ path: newPath, value1: formatValue(obj1[key]), value2: undefined })
      } else {
        compare(obj1[key], obj2[key], newPath)
      }
    })
  }

  compare(obj1, obj2)
  return diffs
}
