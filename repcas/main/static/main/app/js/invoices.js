const InvoicesView = Vue.component('InvoicesView', {
  template: '#invoices-view',
  delimiters: ['[[', ']]'],
  data: function () {
    return {
      title: 'invoices'
    }
  },
  mounted: function () {
    $('#invoices').DataTable()
  },
  methods: {
    check() {
    }
  }
})
