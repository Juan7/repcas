const CartView = Vue.component('CartView', {
  template: '#cart-view',
  delimiters: ['[[', ']]'],
  data: function () {
    return {
      quotation: {},
      products: [],
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
    },

    makeOrder: function () {
      const apiUrl = '/accounting/api/quotations/'

      this.quotation.items = this.products
      this.quotation.items.map(item => {item.total = item.price * item.quantity})
      this.quotation.total = this.getTotal()

      this.makingOrder = true
      this.$http.post(apiUrl, this.quotation).then(response => {
        localStorage.setItem('cart', JSON.stringify([]))
        this.makingOrder = false
        alert('En buena hora, pedido realizado.')
        this.$router.push({ name: 'products' })
      }, response => {
        this.makingOrder = false
        alert('ocurrio un error inesperado, contactese con el admin')
        console.log(response)
      })
    },

    getTotal: function() {
      let total = 0
      for (let product of this.products) {
        total += product.total
      }
      return total
    },
  }
})
