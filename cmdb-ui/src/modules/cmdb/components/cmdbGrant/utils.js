export const getCurrentRowStyle = ({ row }, addedRids) => {
    const idx = addedRids.findIndex(item => item.rid === row.rid)
    return idx > -1 ? 'background-color:#E0E7FF!important' : ''
}
