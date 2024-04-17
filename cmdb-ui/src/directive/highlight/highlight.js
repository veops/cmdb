import './highlight.less'

const highlight = (el, binding) => {
    if (binding.value.value) {
        let testValue = `${binding.value.value}`
        if (['(', ')', '$'].includes(testValue)) {
            testValue = `\\${testValue}`
        }
        const regex = new RegExp(`(${testValue})`, 'gi')
        el.innerHTML = el.innerText.replace(regex, `<span class='${binding.value.class ?? 'ops-text-highlight'}'>$1</span>`)
    }
}

export default highlight
