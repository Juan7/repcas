const CartView = Vue.component('CartView', {
  template: '#cart-view',
  delimiters: ['[[', ']]'],
  data: function () {
    return {
      quotation: {},
      products: [],
      promos: [],
      scales: [],
      promoWarn: '',
      makingOrder: false,
      itemToEdit: {
        name: '',
        quantity: 0,
        price: 0,
        code: '',
        id: undefined
      },
    }
  },

  watch: {
    '$route': function () {
      if (this.$route.name === 'cart') {
        this.getData()
      }
    },

    'itemToEdit.id': function (value) {
      this.fetchScales()
      this.fetchPromotions()
    },

    'itemToEdit.quantity' () {
      this.calculatePrice()
    },
  },

  mounted: function () {
    const _this = this
    this.getData()
    $('#cartModal').on('hidden.bs.modal', function () {
      _this.promoWarn = false
    })
  },

  methods: {
    getData: function () {
      this.products = JSON.parse(localStorage.getItem('cart'))
      console.log(this.products)
    },

    makeOrder: function () {
      const apiUrl = '/accounting/api/quotations/'

      this.quotation.items = this.products
      this.quotation.items.map(item => {item.total = this.round(item.price * item.quantity)})
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
      return this.round(total)
    },

    fetchScales: function() {
      const apiUrl = '/inventory/api/product-scales/'
      const params = {'params': {'product__id': this.itemToEdit.product}}

      this.$http.get(apiUrl, params).then(response => {
        this.scales = response.body.results
        console.log(this.scales)
      }, response => {
        console.log('error')
      })
    },

    fetchPromotions: function() {
      const apiUrl = '/inventory/api/product-promotions/'
      const params = {'params': {'product__id': this.itemToEdit.product}}

      this.$http.get(apiUrl, params).then(response => {
        this.promos = response.body.results
        const childs = this.getChilds(this.itemToEdit.id)
        for (let index in this.promos) {
          this.promos[index].quantity = childs[index].quantity / this.promos[index].child_product_quantity
        }
      }, response => {
        console.log('error')
      })
    },

    calculatePrice: function () {
      const apiUrl = `/inventory/api/check-product-price/${this.itemToEdit.product}`
      const params = {'params': {'quantity': this.itemToEdit.quantity || 0 }}
      this.$http.get(apiUrl, params).then(response => {
        this.itemToEdit.price = response.body.calculated_price.toFixed(4)
        this.itemToEdit.unit_price = response.body.calculated_unit_price.toFixed(4)
      }, response => {
        console.log('error')
      })
    },
    
    deleteProduct: function(productId) {
      this.products = this.products.filter(function(product) {
        if (product.id && product.id !== productId) {
          return product
        } else if (product.parentId && product.parentId !== productId) {
          return product
        }
      })
      localStorage.setItem('cart', JSON.stringify(this.products))
    },

    round: function (num) {
      return Math.round(num * 100) / 100
    },

    getChilds: function(productId) {
      return this.products.filter(function(product) {
        return product.parentId === productId
      })
    },

    addToCart: function () {
      if (!this.isValidPromoQuantity()) {
        this.promoWarn = true
        return
      }

      const _this = this
      const oldId = this.itemToEdit.id
      this.itemToEdit = Object.assign({}, this.itemToEdit)
      this.itemToEdit.id = Date.now()
      this.products.push(this.itemToEdit)
      const validPromos = this.promos.filter(function (promo) {
        return (promo.product_quantity * promo.quantity) <= _this.itemToEdit.quantity && promo.quantity > 0
      })

      for (let i = 0; i < validPromos.length; i++) {
        this.products.push({
          name: validPromos[i].child_product.name,
          quantity: validPromos[i].quantity * validPromos[i].child_product_quantity,
          code: validPromos[i].child_product.code,
          product: validPromos[i].child_product.id,
          price: 0,
          parentId: this.itemToEdit.id
        })
      }
      this.deleteProduct(oldId)
      $('#cartModal').modal('hide')
    },

    isValidPromoQuantity: function () {
      const promos = this.promos.filter(function (promo) { return promo.quantity > 0 })
      let quantity = this.itemToEdit.quantity

      for (let promo of promos) {
        if ((promo.product_quantity * promo.quantity) > quantity) {
          return false
        }
        quantity -= promo.product_quantity * promo.quantity
      }
      return true
    }
  }
})
