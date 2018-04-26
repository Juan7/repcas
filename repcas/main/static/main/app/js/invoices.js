const InvoicesView = Vue.component('InvoicesView', {
  template: '#invoices-view',
  delimiters: ['[[', ']]'],
  data: function () {
    return {
      invoices: [],
      filters: {
        'is_payed': false,
        'number__icontains': undefined,
        'client__name__icontains': undefined
      }
    }
  },
  watch: {
    'filters.is_payed': function () {
      this.fetchData()
    },

    'filters.number__icontains': function () {
      this.filters.client__name__icontains = this.filters.number__icontains
      this.fetchData()
    }
  },
  mounted: function () {
    this.fetchData()
  },
  methods: {
    fetchData: function () { _.debounce(this.fetchInvoices, 500)() },

    fetchInvoices: function () {
      const apiUrl = '/accounting/api/invoices/'

      const params = { params: this.filters }

      this.$http.get(apiUrl, params).then(response => {
        this.invoices = response.body.results;
        console.log(this.invoices)
      }, response => {
        console.log('error')
        // error callback
      })
    }
  }
})
