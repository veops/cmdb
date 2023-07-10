export const colorList = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']

export const category_1_bar_options = (data) => {
    return {
        grid: {
            top: 15,
            left: 'left',
            right: 0,
            bottom: 0,
            containLabel: true,
        },
        xAxis: {
            type: 'category',
            data: Object.keys(data)
        },
        yAxis: {
            type: 'value',
            splitLine: {
                show: false
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        series: [
            {
                data: Object.keys(data).map((key, index) => {
                    return {
                        value: data[key],
                        itemStyle: { color: colorList[0] }
                    }
                }),
                type: 'bar',
                label: {
                    show: true,
                    position: 'top',
                    fontSize: 10,
                    formatter(data) {
                        return `${data.value || ''}`
                    }
                },
            }
        ]
    }
}

export const category_1_pie_options = (data) => {
    return {
        grid: {
            top: 10,
            left: 'left',
            right: 0,
            bottom: 0,
            containLabel: true,
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            type: 'scroll',
            formatter: function (name) {
                return `${name}：${data[name]}`
            }
        },
        series: [
            {
                type: 'pie',
                radius: '90%',
                data: Object.keys(data).map(key => {
                    return { value: data[key], name: key }
                }),
                label: {
                    show: false,
                },
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    }
}

export const category_2_bar_options = (data) => {
    const xAxisData = Object.keys(data.detail)
    const _legend = []
    xAxisData.forEach(key => {
        _legend.push(...Object.keys(data.detail[key]))
    })
    const legend = [...new Set(_legend)]
    return {
        grid: {
            top: 15,
            left: 'left',
            right: 0,
            bottom: 20,
            containLabel: true,
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        legend: {
            orient: 'horizontal',
            bottom: '0',
            type: 'scroll',
            data: legend
        },
        xAxis: [
            {
                type: 'category',
                axisTick: { show: false },
                data: xAxisData
            }
        ],
        yAxis: [
            {
                type: 'value',
                splitLine: {
                    show: false
                }
            }
        ],
        series: legend.map(le => {
            return {
                name: le,
                type: 'bar',
                barGap: 0,
                emphasis: {
                    focus: 'series'
                },
                data: xAxisData.map(x => {
                    return data.detail[x][le] || 0
                }),
                label: {
                    show: true,
                    position: 'top',
                    fontSize: 10,
                    formatter(data) {
                        return `${data.value || ''}`
                    }
                },
            }
        })
    }
}
