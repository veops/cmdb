export const category_1_bar_options = (data, options) => {
    // 计算一级分类
    const xData = Object.keys(data)
    // 计算共有多少二级分类
    const secondCategory = {}
    Object.keys(data).forEach(key => {
        if (Object.prototype.toString.call(data[key]) === '[object Object]') {
            Object.keys(data[key]).forEach(key1 => {
                secondCategory[key1] = Array.from({ length: xData.length }).fill(0)
            })
        } else {
            secondCategory['其他'] = Array.from({ length: xData.length }).fill(0)
        }
    })
    Object.keys(secondCategory).forEach(key => {
        xData.forEach((x, idx) => {
            if (data[x][key]) {
                secondCategory[key][idx] = data[x][key]
            }
            if (typeof data[x] === 'number') {
                secondCategory['其他'][idx] = data[x]
            }
        })
    })
    return {
        color: options.chartColor.split(','),
        grid: {
            top: 15,
            left: 'left',
            right: 10,
            bottom: 20,
            containLabel: true,
        },
        legend: {
            data: Object.keys(secondCategory),
            bottom: 0,
            type: 'scroll',
        },
        xAxis: options.barDirection === 'y' ? {
            type: 'category',
            axisTick: { show: false },
            data: xData
        }
            : {
                type: 'value',
                splitLine: {
                    show: false
                }
            },
        yAxis: options.barDirection === 'y' ? {
            type: 'value',
            splitLine: {
                show: false
            }
        } : {
            type: 'category',
            axisTick: { show: false },
            data: xData
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        series: Object.keys(secondCategory).map(key => {
            return {
                name: key,
                type: 'bar',
                stack: options?.barStack ?? 'total',
                barGap: 0,
                emphasis: {
                    focus: 'series'
                },
                data: secondCategory[key]
            }
        })
    }
}

export const category_1_line_options = (data, options) => {
    const xData = Object.keys(data)
    return {
        color: options.chartColor.split(','),
        grid: {
            top: 15,
            left: 'left',
            right: 10,
            bottom: 20,
            containLabel: true,
        },
        tooltip: {
            trigger: 'axis'
        },
        xAxis: {
            type: 'category',
            data: xData
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                data: xData.map(item => data[item]),
                type: 'line',
                smooth: true,
                showSymbol: false,
                areaStyle: options?.isShadow ? {
                    opacity: 0.5,
                    color: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0, color: options.chartColor.split(',')[0] // 0% 处的颜色
                        }, {
                            offset: 1, color: '#ffffff' // 100% 处的颜色
                        }],
                        global: false // 缺省为 false
                    }
                } : null
            }
        ]
    }
}

export const category_1_pie_options = (data, options) => {
    return {
        color: options.chartColor.split(','),
        grid: {
            top: 10,
            left: 'left',
            right: 10,
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

export const category_2_bar_options = (data, options, chartType) => {
    const xAxisData = Object.keys(data.detail)
    const _legend = []
    xAxisData.forEach(key => {
        _legend.push(...Object.keys(data.detail[key]))
    })
    const legend = [...new Set(_legend)]
    return {
        color: options.chartColor.split(','),
        grid: {
            top: 15,
            left: 'left',
            right: 10,
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
        xAxis: options.barDirection === 'y' || chartType === 'line' ? {
            type: 'category',
            axisTick: { show: false },
            data: xAxisData
        }
            : {
                type: 'value',
                splitLine: {
                    show: false
                }
            },
        yAxis: options.barDirection === 'y' || chartType === 'line' ? {
            type: 'value',
            splitLine: {
                show: false
            }
        } : {
            type: 'category',
            axisTick: { show: false },
            data: xAxisData
        },
        series: legend.map((le, index) => {
            return {
                name: le,
                type: chartType,
                barGap: 0,
                emphasis: {
                    focus: 'series'
                },
                stack: chartType === 'line' ? '' : options?.barStack ?? 'total',
                data: xAxisData.map(x => {
                    return data.detail[x][le] || 0
                }),
                smooth: true,
                showSymbol: false,
                label: {
                    show: false,
                },
                areaStyle: chartType === 'line' && options?.isShadow ? {
                    opacity: 0.5,
                    color: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0, color: options.chartColor.split(',')[index % 8] // 0% 处的颜色
                        }, {
                            offset: 1, color: '#ffffff' // 100% 处的颜色
                        }],
                        global: false // 缺省为 false
                    }
                } : null
            }
        })
    }
}

export const category_2_pie_options = (data, options) => {
    console.log(1111, options)
    const _legend = []
    Object.keys(data.detail).forEach(key => {
        Object.keys(data.detail[key]).forEach(key2 => {
            _legend.push({ value: data.detail[key][key2], name: `${key}-${key2}` })
        })
    })
    return {
        color: options.chartColor.split(','),
        grid: {
            top: 15,
            left: 'left',
            right: 10,
            bottom: 20,
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
                const _find = _legend.find(item => item.name === name)
                return `${name}：${_find.value}`
            }
        },
        series: [
            {
                type: 'pie',
                radius: '90%',
                data: _legend,
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
