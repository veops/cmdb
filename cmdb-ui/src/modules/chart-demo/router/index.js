import { BasicLayout } from '@/layouts'

export default () => [
  {
    path: '/chart-demo',
    name: 'chart-demo',
    component: BasicLayout,
    redirect: '/chart-demo/diagram',
    meta: { title: 'Chart Demo', icon: 'gridSvg', selectedIcon: 'gridSvg' },
    children: [
      {
        path: '/chart-demo/gds',
        name: 'chart_demo_gds',
        meta: { title: 'Topo GDS', icon: 'ops_move_icon', selectedIcon: 'ops_move_icon' },
        component: () => import('@/modules/chart-demo/views/GDSView')
      },
      // {
      //   path: '/chart-demo/diagram',
      //   name: 'chart_demo_diagram',
      //   meta: { title: 'Diagram Demo', icon: 'ops_move_icon', selectedIcon: 'ops_move_icon' },
      //   component: () => import('@/modules/chart-demo/views/DiagramDemoView')
      // },
      // {
      //   path: '/chart-demo/network',
      //   name: 'chart_demo_network',
      //   meta: { title: 'Network Diagram', icon: 'ops_move_icon', selectedIcon: 'ops_move_icon' },
      //   component: () => import('@/modules/chart-demo/views/NetworkDiagramView')
      // }
    ]
  }
]
