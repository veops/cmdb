/* eslint-disable */
export function intersection(thisSet, otherSet) {
    //初始化一个新集合，用于表示交集。
    var interSectionSet = new Set()
    var values = Array.from(thisSet)
    for (var i = 0; i < values.length; i++) {

        if (otherSet.has(values[i])) {
            interSectionSet.add(values[i])
        }
    }

    return interSectionSet
}

export function union(thisSet, otherSet) {
    var unionSet = new Set()
    var values = Array.from(thisSet)
    for (var i = 0; i < values.length; i++) {
        unionSet.add(values[i])
    }
    values = Array.from(otherSet)
    for (var i = 0; i < values.length; i++) {
        unionSet.add(values[i])
    }

    return unionSet
}

export function difference(thisSet, otherSet) {
    var differenceSet = new Set()
    var values = Array.from(thisSet)
    for (var i = 0; i < values.length; i++) {

        if (!otherSet.has(values[i])) {
            differenceSet.add(values[i])
        }
    }

    return differenceSet
}
