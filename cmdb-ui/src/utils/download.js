import moment from 'moment'
import XLSX from 'xlsx'
import XLSXS from 'xlsx-js-style'

export const downloadTxt = ({ text, title }) => {
    const dom = document.createElement('a')
    dom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text))
    dom.setAttribute('download', `${title}.txt`)
    if (document.createEvent) {
        var event = document.createEvent('MouseEvents')
        event.initEvent('click', true, true)
        dom.dispatchEvent(event)
    } else {
        dom.click()
    }
}

export const downloadExcel = (data, fileName = `${moment().format('YYYY-MM-DD HH:mm:ss')}.xls`) => {
    // STEP 1: Create a new workbook
    const wb = XLSXS.utils.book_new()
    // STEP 2: Create data rows and styles
    const rowArray = data
    // STEP 3: Create worksheet with rows; Add worksheet to workbook
    const ws = XLSXS.utils.aoa_to_sheet(rowArray)
    XLSXS.utils.book_append_sheet(wb, ws, fileName)

    let maxColumnNumber = 1 // 默认最大列数
    rowArray.forEach(item => { if (item.length > maxColumnNumber) { maxColumnNumber = item.length } })
    // 合并  #将第一行标题列合并
    // const merges = ['A1:' + String.fromCharCode(64 + parseInt(maxColumnNumber)) + '1']
    const merges = ['A1:' + createCellPos(maxColumnNumber - 1) + '1']
    const wsMerge = []
    merges.map((item) => {
        wsMerge.push(
            XLSXS.utils.decode_range(item)
        )
    })

    ws['!merges'] = wsMerge

    // 添加列宽
    ws['!cols'] = (rowArray[1].map(item => {
        return { width: 22 }
    }))
    // 添加行高
    ws['!rows'] = [{ 'hpt': 80 }]
    // STEP 4: Write Excel file to browser  #导出
    XLSXS.writeFile(wb, fileName + '.xlsx')
}

export const excel2Array = (fileObj) => {
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

export const createCellPos = (n) => {
    const ordA = 'A'.charCodeAt(0)
	const ordZ = 'Z'.charCodeAt(0)
    const len = ordZ - ordA + 1
    let s = ''
     while (n >= 0) {
		s = String.fromCharCode(n % len + ordA) + s
		n = Math.floor(n / len) - 1
	}
	return s
}
