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
        price: 0,
        code: ''
      },
      promos: [],
      promoWarn: '',
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
      this.newItem = { quantity: 1, price: 0, name: '', code: '' }
    },

    addToCart: function () {
      if (!this.isValidPromoQuantity()) {
        this.promoWarn = true
        return
      }

      const _this = this
      this.cart.push(this.newItem)
      const validPromos = this.promos.filter(function (promo) {
        return (promo.product_quantity * promo.quantity) <= _this.newItem.quantity && promo.quantity > 0
      })

      for (let i = 0; i < validPromos.length; i++) {
        console.log('validPromos', validPromos)
        this.cart.push({
          name: validPromos[i].child_product.name,
          quantity: validPromos[i].quantity * validPromos[i].child_product_quantity,
          code: validPromos[i].child_product.code,
          product: validPromos[i].product.id,
          price: 0
        })
      }
      this.setCartData()
      $('#cartModal').modal('hide')
    },

    setNewItem: function (product) {
      this.newItem.price = '...'
      this.newItem.product = product.id
      this.newItem.name = product.name
      this.newItem.code = product.code
      this.newItem.quantity = 1
      this.productId = product.id
      this.promos = []
      this.scales = []

      this.fetchScales()
      this.fetchPromotions()
      this.calculatePrice()
    },

    fetchScales: function() {
      const apiUrl = '/inventory/api/product-scales/'
      const params = {'params': {'product__id': this.productId}}

      this.$http.get(apiUrl, params).then(response => {
        this.scales = response.body.results
        console.log(this.scales)
      }, response => {
        console.log('error')
      })
    },

    fetchPromotions: function() {
      const apiUrl = '/inventory/api/product-promotions/'
      const params = {'params': {'product__id': this.productId}}

      this.$http.get(apiUrl, params).then(response => {
        this.promos = response.body.results
        for (let promo of this.promos) {
          promo.quantity = 0
        }
        // this.$set(this, 'promos', this.promos)
      }, response => {
        console.log('error')
      })
    },

    calculatePrice: function () {
      const apiUrl = `/inventory/api/check-product-price/${this.productId}`
      const params = {'params': {'quantity': this.newItem.quantity || 0 }}
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
    },

    isValidPromoQuantity: function () {

      const promos = this.promos.filter(function (promo) { return promo.quantity > 0 })
      let quantity = this.newItem.quantity

      for (let promo of promos) {
        if ((promo.product_quantity * promo.quantity) > quantity) {
          return false
        }
        quantity -= promo.product_quantity
      }
      return true
    }

  }
})
