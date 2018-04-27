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
        quantity: 0,
        price: 0
      },
      promos: [],
      scales: [],
      filters: {
        'name__icontains': undefined,
        'code__icontains': undefined
      }
    }
  },

  watch: {
    '$route': function () {
      if (this.$route.name === 'products') {
        this.resetData()
        this.fetchData()
        this.setCartData()
      }
    },
      
    'filters.name__icontains': function () {
      this.filters.code__icontains = this.filters.name__icontains
      this.fetchData()
    },

    'newItem.quantity' () {
      this.calculatePrice()
    },
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

      const params = { params: this.filters }
      this.$http.get(apiUrl, params).then(response => {
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
      this.newItem.quantity = 1
      this.productId = product.id
      this.promos = []
      this.scales = []
      
      this.fetchScales()
      this.fetchPromotions()
    },
      
    fetchScales: function() {
      const apiUrl = '/inventory/api/product-scales/'
      const params = {'params': {'product__id__exact': this.productId}}
      
      this.$http.get(apiUrl, params).then(response => {
        this.scales = response.body.results
        console.log(this.scales)
      }, response => {
        console.log('error')
      })
    },

    fetchPromotions: function() {
      const apiUrl = '/inventory/api/product-promotions/'
      const params = {'params': {'product__id__exact': this.productId}}
      
      this.$http.get(apiUrl, params).then(response => {
        this.promos = response.body.results
        for (let promo of this.promos) {
          promo.quantity = 0
        }
      }, response => {
        console.log('error')
      })
    },
      
    calculatePrice: function () {
      const apiUrl = `/inventory/api/check-product-price/${this.productId}`
      const params = {'params': {'quantity': this.newItem.quantity}}
      this.$http.get(apiUrl, params).then(response => {
        this.newItem.price = response.body.calculated_price
      }, response => {
        console.log('error')
      })
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
