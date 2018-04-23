const InvoicesView = Vue.component('InvoicesView', {
  template: '#invoices-view',
  delimiters: ['[[', ']]'],
  data: function () {
    return {
      invoices: []
    }
  },
  mounted: function () {
    $('#invoices').DataTable()
    this.fetchData()
    console.log('moment', moment)
  },
  methods: {
    fetchData: function () { _.debounce(this.fetchInvoices, 500)() },

    fetchInvoices: function () {
      const apiUrl = '/accounting/api/invoices/'
      this.$http.get(apiUrl).then(response => {
        this.invoices = response.body.results;
        console.log(this.invoices)
      }, response => {
        console.log('error')
        // error callback
      })
    }
  }
})
