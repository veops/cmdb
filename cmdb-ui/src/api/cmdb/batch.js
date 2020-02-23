import XLSX from 'xlsx'
import { axios } from '@/utils/request'

export function processFile (fileObj) {
  const promise = new Promise(function (resolve) {
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
  return promise
}

export function uploadData (ciId, data) {
  data.ci_type = ciId
  return axios({
    url: '/v0.1/ci',
    method: 'PUT',
    data: data
  })
}

export function writeCsv (columns) {
  const { Parser } = require('json2csv')
  const fields = columns
  const opts = { fields }
  const p = new Parser(opts)
  return p.parse([])
}

export function writeExcel (columns, name) {
  const worksheet = XLSX.utils.aoa_to_sheet([columns])
  const newWorkBoot = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(newWorkBoot, worksheet, name)
  const s = XLSX.write(newWorkBoot, { type: 'array' })
  console.log(s)
  return s
}

// Determines whether an array element is empty
export function any (ArrayList) {
  for (let i = 0; i < ArrayList.length; i++) {
    if (ArrayList[i]) {
      return true
    }
  }
  return false
}

export function filterNull (twoDimArray) {
  console.log(twoDimArray)
  const newArray = []
  twoDimArray.forEach(item => {
    if (any(item)) {
      newArray.push(item)
    }
  })
  return newArray
}
