const CartView = Vue.component('CartView', {
  template: '#cart-view',
  delimiters: ['[[', ']]'],
  data: function () {
    return {
      products: [],
      agents: [],
      agentId: undefined
    }
  },

  watch: {
    '$route': function () {
      if (this.$route.name === 'cart') {
        this.getData()
      }
    },
  },

  mounted: function () {
    this.getData()
  },

  methods: {
    getData: function () {
      this.products = JSON.parse(localStorage.getItem('cart'))
      this.getAgents()
    },
      
    getAgents: function () {
      const apiUrl = '/accounts/api/agent/'
      const params = {'params': {}}
      
      this.$http.get(apiUrl, params).then(response => {
        this.agents = response.body.results
        if (this.agents.length) {
          this.agentId = this.agents[0].id
        }
      }, response => {
        console.log('error')
      })
    }
  }
})
