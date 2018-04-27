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

  watch: {
    '$route': function () {
      if (this.$route.name === 'products') {
        this.resetData()
        this.fetchData()
        this.setCartData()
      }
    }
  },

  mounted: function () {
    const _this = this
    this.resetData()
    this.fetchData()
    this.setCartData()

    $('#cartModal').on('hidden.bs.modal', function () { _this.clearCartModal() })
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
      Object.assign(this.$data, this.$options.data())
    },

    clearCartModal: function () {
      this.newItem = { quantity: 1, price: 0, name: '' }
    },

    addToCart: function () {
      if (!this.isValidPromoQuantity) { return; }

      const _this = this
      this.cart.push(this.newItem)
      const validPromos = this.promos.filter(function (promo) {
        return (promo.require * promo.quantity) <= _this.newItem.quantity  && promo.quantity > 0
      })

      for (let i = 0; i < validPromos.length; i++) {
        this.cart.push({
          name: validPromos[i].product_name,
          quantity: validPromos[i].quantity,
          price: 0
        })
      }
      this.setCartData()
      $('#cartModal').modal('hide')
    },

    setNewItem: function (product) {
      this.newItem.price = product.price
      this.newItem.name = product.name
    },

    setCartData: function () {
      let cartData = JSON.parse(localStorage.getItem('cart'))
      if (!cartData) {
        cartData = []
      }
      let cart = cartData.concat(this.cart)
      localStorage.setItem('cart', JSON.stringify(cart))
      this.cart = []
    }

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
