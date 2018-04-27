const ProductsView = Vue.component('ProductsView', {
  template: '#products-view',
  delimiters: ['[[', ']]'],
  data: function () {
    return {
      products: [],
      productId: undefined,
      cart: [],
      newItem: {
        name: '',
        quantity: 1,
        price: 0
      },
      promos: [],
      scales: [],
      filters: {}
    }
  },

  mounted: function () {
    const _this = this
    this.fetchData()
    $('#cartModal').on('hidden.bs.modal', function () {
      _this.resetData()
    })
  },
  methods: {
  	fetchData: function () { _.debounce(this.fetchProducts, 500)() },

    fetchProducts: function () {
      const apiUrl = '/inventory/api/products/'

      this.$http.get(apiUrl).then(response => {
        this.products = response.body.results;
      }, response => {
        console.log('error')
      })
    },

    resetData: function () {
      this.newItem = { quantity: 1, price: 0, name: '' }
    },

    addToCart: function () {
      if (!this.isValidPromoQuantity) { return; }

      const _this = this
      this.cart.push(this.newItem)
      const validPromos = this.promos.filter(function (promo) { return (promo.require * promo.quantity) <= _this.newItem.quantity })

      for (let i = 0; i < validPromos.length; i++) {
        this.cart.push({
          name: validPromos[i].name,
          quantity: validPromos[i].quantity,
          price: 0
        })
      }
      localStorage.setItem('cart', JSON.stringify(this.cart))
    },

    setNewItem: function (product) {
      this.newItem.price = product.price
      this.newItem.name = product.name
      this.productId = product.id
      this.promos = []
      this.scales = []
      
      this.fetchScales()
      this.fetchPromotions()
    },
      
    fetchScales: function() {
      const apiUrl = '/inventory/api/product-scales/'
      const params = {'product__id__exact': this.productId}
      
      this.$http.get(apiUrl, params).then(response => {
        this.scales = response.body.results
        console.log(this.scales)
      }, response => {
        console.log('error')
      })
    },

    fetchPromotions: function() {
      const apiUrl = '/inventory/api/product-promotions/'
      const params = {'product__id__exact': this.productId}
      
      this.$http.get(apiUrl, params).then(response => {
        this.promos = response.body.results
        console.log(this.promos)
      }, response => {
        console.log('error')
      })
    },

  },
  computed: {
    isValidPromoQuantity: function () {
      const promos = this.promos.filter(function (promo) { return promo.quantity > 0 })

      for (let i = 0; i < promos.length; i++) {
        if ((promos[i].require * promos[i].quantity) > this.newItem.quantity) {
          return false
        }
      }
      return true
    }
  }
})
