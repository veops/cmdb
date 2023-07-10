import XLSX from 'xlsx'
import { axios } from '@/utils/request'

export function processFile(fileObj) {
  return new Promise(function (resolve) {
    const reader = new FileReader()
    reader.readAsBinaryString(fileObj)
    reader.onload = function (e) {
      const data = e.target.result
      const workbook = XLSX.read(data, { type: 'binary' })
      const sheet = workbook.Sheets[workbook.SheetNames[0]]
      const lt = XLSX.utils.sheet_to_json(sheet, { header: 1 })
      resolve(lt)
    }
  })
}

export function uploadData(ciId, data) {
  data.ci_type = ciId
  data.exist_policy = 'replace'
  return axios({
    url: '/v0.1/ci',
    method: 'POST',
    data,
    isShowMessage: false
  })
}

export function writeCsv(columns) {
  const { Parser } = require('json2csv')
  const opts = { columns }
  const p = new Parser(opts)
  return p.parse([])
}

export function writeExcel(columns, name) {
  const worksheet = XLSX.utils.aoa_to_sheet([columns])
  const newWorkBoot = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(newWorkBoot, worksheet, name)
  const s = XLSX.write(newWorkBoot, { type: 'array' })
  console.log(s)
  return s
}

// 判断一个数组元素是否都为空的
export function any(ArrayList) {
  let flag = false
  for (let i = 0; i < ArrayList.length; i++) {
    if (ArrayList[i]) {
      flag = true
      return flag
    }
  }
  return false
}

// 去除一个二维数组 底下为空的部分
export function filterNull(twoDimArray) {
  console.log(twoDimArray)
  const newArray = []
  for (let i = 0; i < twoDimArray.length; i++) {
    if (any(twoDimArray[i])) {
      newArray.push(twoDimArray[i])
    }
  }
  return newArray
}
