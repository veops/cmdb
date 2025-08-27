<template>
  <div>
    <NetworkTopology :nodes="topologyNodes" :links="topologyLinks" />
  </div>
</template>

<script>
import NetworkTopology from './NetworkTopology.vue'

export default {
  name: 'FabricTopology',
  components: {
    NetworkTopology
  },
  data() {
    return {
      topologyNodes: [
        // Groups
        { key: 'SPINE', isGroup: true },
        { key: 'LEAF', isGroup: true },
        { key: 'APIC', isGroup: true },

        // SPINE nodes
        { key: 'SPINE-01', label: 'SPINE-01', subtitle: 'ACI', type: 'spine', color: '#9ec5fe', group: 'SPINE' },
        { key: 'SPINE-02', label: 'SPINE-02', subtitle: 'ACI', type: 'spine', color: '#9ec5fe', group: 'SPINE' },

        // LEAF nodes (10 nodes như mẫu)
        { key: 'LEAF-01', label: 'LEAF-01', subtitle: 'ACI', type: 'leaf', color: '#bde0fe', group: 'LEAF' },
        { key: 'LEAF-02', label: 'LEAF-02', subtitle: 'ACI', type: 'leaf', color: '#bde0fe', group: 'LEAF' },
        { key: 'LEAF-03', label: 'LEAF-03', subtitle: 'ACI', type: 'leaf', color: '#bde0fe', group: 'LEAF' },
        { key: 'LEAF-04', label: 'LEAF-04', subtitle: 'ACI', type: 'leaf', color: '#bde0fe', group: 'LEAF' },
        { key: 'LEAF-05', label: 'LEAF-05', subtitle: 'ACI', type: 'leaf', color: '#bde0fe', group: 'LEAF' },
        { key: 'LEAF-06', label: 'LEAF-06', subtitle: 'ACI', type: 'leaf', color: '#bde0fe', group: 'LEAF' },
        { key: 'LEAF-07', label: 'LEAF-07', subtitle: 'ACI', type: 'leaf', color: '#bde0fe', group: 'LEAF' },
        { key: 'LEAF-08', label: 'LEAF-08', subtitle: 'ACI', type: 'leaf', color: '#bde0fe', group: 'LEAF' },
        { key: 'LEAF-09', label: 'LEAF-09', subtitle: 'ACI', type: 'leaf', color: '#bde0fe', group: 'LEAF' },
        { key: 'LEAF-10', label: 'LEAF-10', subtitle: 'ACI', type: 'leaf', color: '#bde0fe', group: 'LEAF' },

        // APIC nodes
        { key: 'APIC-01', label: 'APIC-01', subtitle: 'ACI', type: 'apic', color: '#d6f7dd', group: 'APIC' },
        { key: 'APIC-02', label: 'APIC-02', subtitle: 'ACI', type: 'apic', color: '#d6f7dd', group: 'APIC' },
        { key: 'APIC-03', label: 'APIC-03', subtitle: 'ACI', type: 'apic', color: '#d6f7dd', group: 'APIC' }
      ],
      topologyLinks: [
        // SPINE-01 connections (highlighted in blue)
        { from: 'SPINE-01', to: 'LEAF-01', label: 'E1/59', isHighlighted: true },
        { from: 'SPINE-01', to: 'LEAF-02', label: 'E1/59', isHighlighted: true },
        { from: 'SPINE-01', to: 'LEAF-03', label: 'E1/23-32' },
        { from: 'SPINE-01', to: 'LEAF-04', label: 'E1/23-32' },
        { from: 'SPINE-01', to: 'LEAF-05', label: 'E1/23-32' },
        { from: 'SPINE-01', to: 'LEAF-06', label: 'E1/23-32' },
        { from: 'SPINE-01', to: 'LEAF-07', label: 'E1/23-32' },
        { from: 'SPINE-01', to: 'LEAF-08', label: 'E1/23-32' },
        { from: 'SPINE-01', to: 'LEAF-09', label: 'E1/23-32' },
        { from: 'SPINE-01', to: 'LEAF-10', label: 'E1/23-32' },

        // SPINE-02 connections (highlighted in blue)
        { from: 'SPINE-02', to: 'LEAF-01', label: 'E1/60', isHighlighted: true },
        { from: 'SPINE-02', to: 'LEAF-02', label: 'E1/60', isHighlighted: true },
        { from: 'SPINE-02', to: 'LEAF-03', label: 'E1/23-32' },
        { from: 'SPINE-02', to: 'LEAF-04', label: 'E1/23-32' },
        { from: 'SPINE-02', to: 'LEAF-05', label: 'E1/23-32' },
        { from: 'SPINE-02', to: 'LEAF-06', label: 'E1/23-32' },
        { from: 'SPINE-02', to: 'LEAF-07', label: 'E1/23-32' },
        { from: 'SPINE-02', to: 'LEAF-08', label: 'E1/23-32' },
        { from: 'SPINE-02', to: 'LEAF-09', label: 'E1/23-32' },
        { from: 'SPINE-02', to: 'LEAF-10', label: 'E1/23-32' },

        // LEAF to APIC connections (highlighted in blue)
        { from: 'LEAF-01', to: 'APIC-01', label: 'E1/1', isHighlighted: true },
        { from: 'LEAF-02', to: 'APIC-02', label: 'E1/2', isHighlighted: true },
        { from: 'LEAF-03', to: 'APIC-03', label: 'E1/3', isHighlighted: true }
      ]
    }
  }
}
</script>
