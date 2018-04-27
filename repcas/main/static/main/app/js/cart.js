const CartView = Vue.component('CartView', {
  template: '#cart-view',
  delimiters: ['[[', ']]'],
  data: function () {
    return {
      products: []
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
    }
  }
})
