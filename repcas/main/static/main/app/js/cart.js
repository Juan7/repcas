const CartView = Vue.component('CartView', {
  template: '#cart-view',
  delimiters: ['[[', ']]'],
  data: function () {
    return {
      products: [],
      agents: [],
      agentId: undefined,
      makingOrder: false
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
    },
    makeOrder: function (argument) {
      const apiUrl = '/accounts/api/make-order/'
      const order = {
        agent_id: this.agentId,
        products: this.products
      }
      
      this.makingOrder = true
      this.$http.post(apiUrl, order).then(response => {
        localStorage.setItem('cart', JSON.stringify([]))
        this.makingOrder = false
        alert('En buena hora, pedido realizado.')
        this.router.push({ name: 'products' })
      }, response => {
        this.makingOrder = false
        alert('ocurrio un error inesperado, contactese con el admin')
        console.log(response)
      })
    }
  }
})
