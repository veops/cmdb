<template>
  <div class="w-full">
    <h2>Network Diagram</h2>
    <NetworkDiagram :nodes="diagramNodes" :links="diagramLinks" />

    <h2 style="margin-top: 40px">Fabric Topology</h2>
    <FabricTopology />

    <h2 style="margin-top: 40px">MX204 Edge Topology</h2>
    <MX204EdgeTopology />

    <h2 style="margin-top: 40px">Example Topology</h2>
    <ExampleTopology />
  </div>
</template>

<script>
import ExampleTopology from '../components/ExampleTopology'
import FabricTopology from '../components/FabricTopology'
import MX204EdgeTopology from '../components/MX204EdgeTopology'
import NetworkDiagram from '../components/NetworkDiagram'

export default {
  name: 'GDSView',
  components: {
    NetworkDiagram,
    FabricTopology,
    MX204EdgeTopology,
    ExampleTopology
  },
  data() {
    return {
      diagramNodes: [
        // Groups
        { key: 'LEAF', isGroup: true, category: 'band', text: 'LEAF', loc: '0 120', size: '1180 90' },
        { key: 'DMZ', isGroup: true, category: 'area', text: 'DMZ' },
        { key: 'CORE', isGroup: true, category: 'area', text: 'CORE' },

        // INTERNET EDGE cluster (phải, phía trên LEAF)
        { key: 'INTERNET', category: 'label', text: 'INTERNET', loc: '520 -60' },
        { key: 'EDGE', category: 'label', text: 'INTERNET EDGE', loc: '520 -10' },
        { key: 'LB', category: 'net', text: 'LB', loc: '470 40', size: '90 54' },
        { key: 'VPN', category: 'net', text: 'VPN ROUTER', loc: '570 40', size: '120 54' },

        // DMZ area members (trái, trên LEAF)
        { key: 'DMZ-SRV', category: 'default', text: 'DMZ SERVER', group: 'DMZ', loc: '-430 -100', size: '120 64' },
        { key: 'WEB-SRV', category: 'default', text: 'WEB SERVER', group: 'DMZ', loc: '-300 -100', size: '120 64' },
        { key: 'WAF', category: 'security', text: 'WAF DMZ', group: 'DMZ', loc: '-150 60', size: '120 54' },
        { key: 'IPS', category: 'security', text: 'IPS', group: 'DMZ', loc: '-150 10', size: '120 54' },
        {
          key: 'FW-DMZ',
          category: 'security',
          text: 'FIREWALL DMZ PALO ALTO',
          group: 'DMZ',
          loc: '-60 -40',
          size: '160 64',
        },

        // CORE area members (giữa dưới LEAF)
        { key: 'JUMP', category: 'default', text: 'JUMP SERVER', group: 'CORE', loc: '-260 220', size: '120 64' },
        { key: 'CORE-SRV', category: 'default', text: 'CORE', group: 'CORE', loc: '-160 220', size: '120 64' },
        {
          key: 'FW-CORE',
          category: 'security',
          text: 'FIREWALL CORE CHECKPOINT',
          group: 'CORE',
          loc: '160 190',
          size: '190 64',
        },

        // WAN (phải, ngang LEAF)
        { key: 'WAN', category: 'net', text: 'WAN', loc: '760 120', size: '120 54' },
      ],
      diagramLinks: [
        // INTERNET EDGE flows
        { from: 'INTERNET', to: 'EDGE' },
        { from: 'EDGE', to: 'LB' },
        { from: 'EDGE', to: 'VPN' },
        { from: 'LB', to: 'LEAF' },
        { from: 'VPN', to: 'LEAF' },

        // DMZ chain
        { from: 'DMZ-SRV', to: 'WAF' },
        { from: 'WEB-SRV', to: 'WAF' },
        { from: 'WAF', to: 'IPS' },
        { from: 'IPS', to: 'FW-DMZ' },
        { from: 'FW-DMZ', to: 'LEAF' },

        // CORE chain
        { from: 'LEAF', to: 'FW-CORE' },
        { from: 'FW-CORE', to: 'CORE-SRV' },
        { from: 'FW-CORE', to: 'JUMP' },

        // LEAF to WAN
        { from: 'LEAF', to: 'WAN' },
      ],
    }
  },
}
</script>

<style scoped>
/* Styles can be removed since they're now in the NetworkDiagram component */
</style>
