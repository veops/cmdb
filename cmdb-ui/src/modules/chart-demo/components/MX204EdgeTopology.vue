<template>
  <div>
    <NetworkTopology :nodes="topologyNodes" :links="topologyLinks" />
  </div>
</template>

<script>
import NetworkTopology from './NetworkTopology.vue'

export default {
  name: 'MX204EdgeTopology',
  components: {
    NetworkTopology
  },
  data() {
    return {
      topologyNodes: [
        // Groups
        { key: 'INTERNET', isGroup: true, loc: '600 50' },
        { key: 'EDGE', isGroup: true, loc: '600 200' },
        { key: 'ACCESS', isGroup: true, loc: '600 350' },

        // Internet Layer
        { key: 'INTERNET-CLOUD', label: 'INTERNET', subtitle: 'Cloud', type: 'internet', color: '#e0f2fe', group: 'INTERNET', loc: '600 80' },
        { key: 'FPT', label: 'FPT', subtitle: 'ASN:18403, IP: 58.187.147.1/29', type: 'isp', color: '#fff3cd', group: 'INTERNET', loc: '400 120' },
        { key: 'CMC', label: 'CMC', subtitle: 'ASN:45903, IP: 113.20.97.249/29', type: 'isp', color: '#fff3cd', group: 'INTERNET', loc: '800 120' },
        { key: 'VIETTEL', label: 'Viettel', subtitle: 'ASN:7552, IP: 125.234.176.153/30', type: 'isp', color: '#fff3cd', group: 'INTERNET', loc: '200 120' },

        // DDoS Protection Layer
        { key: 'DDOS-01', label: 'DDOS', subtitle: 'FPT Protection', type: 'ddos', color: '#f8d7da', group: 'INTERNET', loc: '400 160' },
        { key: 'DDOS-02', label: 'DDOS', subtitle: 'CMC Protection', type: 'ddos', color: '#f8d7da', group: 'INTERNET', loc: '800 160' },

        // Edge Router Layer
        { key: 'MX204-EDGE-01', label: 'MX204-EDGE-01', subtitle: 'Edge Router', type: 'edge', color: '#d1ecf1', group: 'EDGE', loc: '450 240' },
        { key: 'MX204-EDGE-02', label: 'MX204-EDGE-02', subtitle: 'Edge Router', type: 'edge', color: '#d1ecf1', group: 'EDGE', loc: '750 240' },

        // Access Layer
        { key: 'MX-LEAF-01', label: 'LEAF-01', subtitle: 'Access Switch', type: 'access', color: '#d4edda', group: 'ACCESS', loc: '400 400' },
        { key: 'MX-LEAF-02', label: 'LEAF-02', subtitle: 'Access Switch', type: 'access', color: '#d4edda', group: 'ACCESS', loc: '800 400' },
        { key: 'C9300-01', label: 'C9300-01', subtitle: 'Management Switch', type: 'mgmt', color: '#e2e3e5', group: 'ACCESS', loc: '300 320' },
        { key: 'C9300-02', label: 'C9300-02', subtitle: 'Management Switch', type: 'mgmt', color: '#e2e3e5', group: 'ACCESS', loc: '900 320' }
      ],
      topologyLinks: [
        // Internet to DDoS connections
        { from: 'INTERNET-CLOUD', to: 'DDOS-01', label: 'G1-OUT FPT', isHighlighted: true },
        { from: 'INTERNET-CLOUD', to: 'DDOS-02', label: 'G3-OUT CMC', isHighlighted: true },

        // DDoS to Edge connections
        { from: 'DDOS-01', to: 'MX204-EDGE-01', label: 'Xe-0/1/3 (.4)', isHighlighted: true },
        { from: 'DDOS-01', to: 'MX204-EDGE-01', label: 'Xe-0/1/2 (.154)', isHighlighted: true },
        { from: 'DDOS-02', to: 'MX204-EDGE-02', label: 'Xe-0/1/3 (.250)', isHighlighted: true },
        { from: 'DDOS-02', to: 'MX204-EDGE-02', label: 'Xe-0/1/2', isHighlighted: true },

        // Edge to Management connections
        { from: 'MX204-EDGE-01', to: 'C9300-01', label: 'Gi1/0/42 (MGMT)', isHighlighted: false },
        { from: 'MX204-EDGE-02', to: 'C9300-02', label: 'Gi2/0/42 (MGMT)', isHighlighted: false },

        // Edge to Leaf connections (ae0 aggregation)
        { from: 'MX204-EDGE-01', to: 'MX-LEAF-01', label: 'Xe-0/1/0 (ae0)', isHighlighted: true },
        { from: 'MX204-EDGE-01', to: 'MX-LEAF-01', label: 'Xe-0/1/1 (ae0)', isHighlighted: true },
        { from: 'MX204-EDGE-01', to: 'MX-LEAF-02', label: 'Xe-0/1/0 (ae0)', isHighlighted: true },
        { from: 'MX204-EDGE-01', to: 'MX-LEAF-02', label: 'Xe-0/1/1 (ae0)', isHighlighted: true },

        { from: 'MX204-EDGE-02', to: 'MX-LEAF-02', label: 'Xe-0/1/0 (ae0)', isHighlighted: true },
        { from: 'MX204-EDGE-02', to: 'MX-LEAF-02', label: 'Xe-0/1/1 (ae0)', isHighlighted: true },
        { from: 'MX204-EDGE-02', to: 'MX-LEAF-01', label: 'Xe-0/1/0 (ae0)', isHighlighted: true },
        { from: 'MX204-EDGE-02', to: 'MX-LEAF-01', label: 'Xe-0/1/1 (ae0)', isHighlighted: true },

        // Leaf to Edge return connections
        { from: 'MX-LEAF-01', to: 'MX204-EDGE-01', label: 'E1/14 (ae0)', isHighlighted: true },
        { from: 'MX-LEAF-01', to: 'MX204-EDGE-01', label: 'E1/15 (ae0)', isHighlighted: true },
        { from: 'MX-LEAF-01', to: 'MX204-EDGE-02', label: 'E1/14 (ae0)', isHighlighted: true },
        { from: 'MX-LEAF-01', to: 'MX204-EDGE-02', label: 'E1/15 (ae0)', isHighlighted: true },

        { from: 'MX-LEAF-02', to: 'MX204-EDGE-02', label: 'E1/14 (ae0)', isHighlighted: true },
        { from: 'MX-LEAF-02', to: 'MX204-EDGE-02', label: 'E1/15 (ae0)', isHighlighted: true },
        { from: 'MX-LEAF-02', to: 'MX204-EDGE-01', label: 'E1/14 (ae0)', isHighlighted: true },
        { from: 'MX-LEAF-02', to: 'MX204-EDGE-01', label: 'E1/15 (ae0)', isHighlighted: true }
      ]
    }
  }
}
</script>
