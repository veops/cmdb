/* eslint-disable no-useless-constructor */
import { TreeNode } from 'butterfly-dag'

import $ from 'jquery'

class BaseNode extends TreeNode {
    constructor(opts) {
        super(opts)
    }

    draw = (opts) => {
        const container = $(`<div class="${opts.id.startsWith('Root') ? 'root' : ''} ci-detail-relation-topo-node"></div>`)
            .css('top', opts.top)
            .css('left', opts.left)
            .attr('id', opts.id)
        let icon
        if (opts.options.icon) {
            icon = $(`<svg class="icon" style="color:${opts.options.icon.split('$$')[1]}" width="1em" height="1em" fill="currentColor" aria-hidden="true" focusable="false" class=""><use data-v-5bd421da="" xlink:href="#${opts.options.icon.split('$$')[0]}"></use></svg>`)
        } else {
            icon = $(`<span class="icon icon-default">${opts.options.name[0].toUpperCase()}</span>`)
        }

        const titleContent = $(`<div title=${opts.options.title} class="title">${opts.options.title}</div>`)
        const uniqueDom = $(`<div class="unique">${opts.options.unique_alias || opts.options.unique_name}：${opts.options.unique_value}<div>`)
        container.append(icon)
        container.append(titleContent)
        container.append(uniqueDom)

        if (opts.options.side && !opts.options.children.length) {
            const addIcon = $(`<i aria-label="图标: plus-square" class="anticon anticon-plus-square add-icon-${opts.options.side}"><svg viewBox="64 64 896 896" data-icon="plus-square" width="1em" height="1em" fill="currentColor" aria-hidden="true" focusable="false" class=""><path d="M328 544h152v152c0 4.4 3.6 8 8 8h48c4.4 0 8-3.6 8-8V544h152c4.4 0 8-3.6 8-8v-48c0-4.4-3.6-8-8-8H544V328c0-4.4-3.6-8-8-8h-48c-4.4 0-8 3.6-8 8v152H328c-4.4 0-8 3.6-8 8v48c0 4.4 3.6 8 8 8z"></path><path d="M880 112H144c-17.7 0-32 14.3-32 32v736c0 17.7 14.3 32 32 32h736c17.7 0 32-14.3 32-32V144c0-17.7-14.3-32-32-32zm-40 728H184V184h656v656z"></path></svg></i>`)
            container.append(addIcon)
            addIcon.on('click', () => {
                if (opts.options.side === 'left') {
                    this.emit('events', {
                        type: 'custom:clickLeft',
                        data: { ...this }
                    })
                }
                if (opts.options.side === 'right') {
                    this.emit('events', {
                        type: 'custom:clickRight',
                        data: { ...this }
                    })
                }
            })
        }

        return container[0]
    }
}

export default BaseNode
