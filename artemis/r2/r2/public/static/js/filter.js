r.filter = {}

r.filter.init = function() {
    var detailsEl = $('.filtered-details')
    if (detailsEl.length) {
        var multi = new r.filter.Filter({
            path: detailsEl.data('path')
        })
        detailsEl.find('.branches a').each(function(i, e) {
            multi.branches.add({name: $(e).data('name')})
        })
        multi.fetch({
            error: _.bind(r.multi.mine.create, r.multi.mine, multi, {wait: true})
        })

        var detailsView = new r.multi.BranchList({
            model: multi,
            itemView: r.filter.FilteredBranchItem,
            el: detailsEl
        }).render()
    }
}

r.filter.Filter = r.multi.MultiArtemis.extend({
    url: function() {
        return r.utils.joinURLs('/api/filter', this.id)
    }
})

r.filter.FilteredBranchItem = r.multi.MultiBranchItem.extend({
    render: function() {
        this.$el.append(this.template({
            sr_name: this.model.get('name')
        }))
        return this
    }
})
