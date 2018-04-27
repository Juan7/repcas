const ProductsView = Vue.component('ProductsView', {
  template: '#products-view',
  delimiters: ['[[', ']]'],
  data: function () {
    return {
      products: [],
      cart: [],
      newItem: {
        name: '',
        quantity: 1,
        price: 0
      },
      promos: [
        {
          id: 1,
          require: 5,
          product_name: 'tomates',
          quantity: 0
        },
        {
          id: 2,
          require: 3,
          product_name: 'plato',
          quantity: 0
        }
      ]
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
